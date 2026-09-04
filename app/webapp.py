from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from pydantic import BaseModel, Field, model_validator
try:
    from dotenv import load_dotenv
except ImportError:  # Dependencies may still be installing during package checks.
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False

from .ezviz import EzvizClient, EzvizError
from .demo_ui import DEMO_HTML
from .multimodal import MultimodalReviewConfig
from .realtime import RealtimeDetectorConfig
from .stream_service import CameraStreamService, probe_video_source


PROJECT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT / ".env")
PACKAGED_CHECKPOINTS = PROJECT / "weights/stgcnpp"
PACKAGED_YOLO = PROJECT / "weights/yolo26n-pose.pt"
PACKAGED_PREFALL = PROJECT / "weights/prefall"
DEFAULT_CHECKPOINTS = (
    PACKAGED_CHECKPOINTS
    if PACKAGED_CHECKPOINTS.is_dir()
    else PROJECT / "results/benchmark_e300_full"
)
DEFAULT_YOLO = PACKAGED_YOLO if PACKAGED_YOLO.is_file() else PROJECT / "yolo26n-pose.pt"
DEFAULT_PREFALL = (
    PACKAGED_PREFALL
    if PACKAGED_PREFALL.is_dir()
    else PROJECT / "outputs/prevfall_rtmpose_stgcnpp_300e_b128"
)


app = FastAPI(
    title="Fall Detection Camera Service",
    version="0.1.0",
    description="EZVIZ/direct-stream ingestion and skeleton fall-detection API",
)
streams = CameraStreamService(
    RealtimeDetectorConfig(
        route=os.getenv("FALL_ROUTE", "yolo_stgcnpp"),
        checkpoints_root=Path(os.getenv(
            "FALL_CHECKPOINTS_ROOT", str(DEFAULT_CHECKPOINTS)
        )),
        yolo_model=Path(os.getenv("FALL_YOLO_MODEL", str(DEFAULT_YOLO))),
        device=os.getenv("FALL_DEVICE", "cuda"),
        threshold=float(os.getenv("FALL_THRESHOLD", "0.5")),
        confirm_windows=int(os.getenv("FALL_CONFIRM_WINDOWS", "3")),
        prefall_enabled=os.getenv("PREFALL_ENABLED", "false").lower() in {"1", "true", "yes"},
        prefall_checkpoints_root=Path(os.getenv(
            "PREFALL_CHECKPOINTS_ROOT", str(DEFAULT_PREFALL)
        )),
        prefall_min_positive_folds=int(os.getenv("PREFALL_MIN_POSITIVE_FOLDS", "5")),
    ),
    MultimodalReviewConfig(
        enabled=os.getenv("MULTIMODAL_ENABLED", "false").lower() in {"1", "true", "yes"},
        model_name=os.getenv("MULTIMODAL_MODEL", "Qwen/Qwen3-VL-2B-Instruct"),
        adapter_path=Path(os.environ["MULTIMODAL_ADAPTER_PATH"])
        if os.getenv("MULTIMODAL_ADAPTER_PATH") else None,
        device=os.getenv("MULTIMODAL_DEVICE", os.getenv("FALL_DEVICE", "cuda")),
        frames=int(os.getenv("MULTIMODAL_FRAMES", "8")),
        buffer_frames=int(os.getenv("MULTIMODAL_BUFFER_FRAMES", "160")),
        max_new_tokens=int(os.getenv("MULTIMODAL_MAX_NEW_TOKENS", "112")),
        cooldown_seconds=float(os.getenv("MULTIMODAL_COOLDOWN_SECONDS", "15")),
        post_trigger_seconds=float(os.getenv("MULTIMODAL_POST_TRIGGER_SECONDS", "2.5")),
        trigger_levels=tuple(
            value.strip().upper()
            for value in os.getenv(
                "MULTIMODAL_TRIGGER_LEVELS", "HIGH,FALL_CONFIRMED"
            ).split(",")
            if value.strip()
        ),
        allow_download=os.getenv("MULTIMODAL_ALLOW_DOWNLOAD", "false").lower()
        in {"1", "true", "yes"},
    ),
)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("FALL_SERVICE_API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="invalid API key")


class StreamSource(BaseModel):
    source_type: Literal["direct", "ezviz", "demo"] = "ezviz"
    source_url: str | None = None
    device_serial: str | None = None
    channel_no: int = Field(default=1, ge=1)
    protocol: int = Field(default=2, ge=1, le=5)
    quality: int = Field(default=2, ge=1, le=2)
    expire_seconds: int = Field(default=3600, ge=30, le=62_208_000)
    camera_id: str | None = None

    @model_validator(mode="after")
    def validate_choice(self):
        if self.source_type == "direct" and not self.source_url:
            raise ValueError("source_url is required for direct source")
        if self.source_type == "ezviz" and not self.device_serial:
            self.device_serial = os.getenv("YS7_DEVICE_SERIAL")
        if self.source_type == "ezviz" and not self.device_serial:
            raise ValueError("device_serial or YS7_DEVICE_SERIAL is required")
        return self


class StartRequest(StreamSource):
    process_every_n_frames: int = Field(default=1, ge=1, le=30)


def resolve_source(request: StreamSource) -> tuple[str, str, dict]:
    if request.source_type == "demo":
        demo_path = PROJECT / "demo" / "prefall_multimodal_raw.mp4"
        if not demo_path.is_file():
            raise ValueError(f"built-in demo video is missing: {demo_path}")
        return str(demo_path), request.camera_id or "built-in-demo", {"demo": True}
    if request.source_type == "direct":
        return request.source_url or "", request.camera_id or "direct-camera", {}
    address = EzvizClient().live_address(
        request.device_serial or "",
        channel_no=request.channel_no,
        protocol=request.protocol,
        quality=request.quality,
        expire_seconds=request.expire_seconds,
    )
    return address.url, request.camera_id or request.device_serial or "ezviz-camera", {
        "url_id": address.url_id,
        "expire_time": address.expire_time,
    }


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def demo_ui() -> str:
    return DEMO_HTML


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": "fall-detection", "stream": streams.status()}


@app.get("/v1/ezviz/devices", dependencies=[Depends(require_api_key)])
def devices(page_start: int = 0, page_size: int = 50) -> dict:
    try:
        return EzvizClient().list_devices(page_start, page_size)
    except (EzvizError, ValueError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.post("/v1/streams/probe", dependencies=[Depends(require_api_key)])
def probe(request: StreamSource, frames: int = Query(default=10, ge=1, le=100)) -> dict:
    try:
        source, camera_id, metadata = resolve_source(request)
        result = probe_video_source(source, frames=frames)
        return {"camera_id": camera_id, **metadata, **result}
    except (EzvizError, ValueError, RuntimeError) as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.post("/v1/streams/start", dependencies=[Depends(require_api_key)])
def start(request: StartRequest) -> dict:
    try:
        source, camera_id, metadata = resolve_source(request)
        status = streams.start(source, camera_id, request.process_every_n_frames)
        return {**metadata, "status": status}
    except (EzvizError, ValueError, RuntimeError) as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.post("/v1/streams/stop", dependencies=[Depends(require_api_key)])
def stop() -> dict:
    return streams.stop()


@app.get("/v1/streams/status", dependencies=[Depends(require_api_key)])
def status() -> dict:
    return streams.status()


@app.get("/v1/events", dependencies=[Depends(require_api_key)])
def events(limit: int = Query(default=50, ge=1, le=200)) -> dict:
    return {"events": streams.events(limit)}


@app.get("/v1/multimodal/status", dependencies=[Depends(require_api_key)])
def multimodal_status() -> dict:
    return streams.multimodal.status()


@app.post("/v1/multimodal/review", dependencies=[Depends(require_api_key)])
def multimodal_review() -> dict:
    result = streams.trigger_multimodal_review()
    if not result["triggered"]:
        raise HTTPException(
            status_code=409,
            detail="review not started: module disabled, busy, or not enough buffered frames",
        )
    return result


@app.get("/v1/frame.jpg", dependencies=[Depends(require_api_key)])
def latest_frame() -> Response:
    jpeg = streams.latest_jpeg()
    if jpeg is None:
        raise HTTPException(status_code=404, detail="no processed frame available")
    return Response(jpeg, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@app.get("/v1/preview.mjpg", dependencies=[Depends(require_api_key)])
def preview() -> StreamingResponse:
    def generate():
        last = None
        while True:
            jpeg = streams.latest_jpeg()
            if jpeg and jpeg is not last:
                last = jpeg
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
            time.sleep(0.1)
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
