from __future__ import annotations

import threading
import time
import uuid
from collections import deque
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import cv2

from .realtime import RealtimeDetectorConfig, RealtimeFallDetector
from .multimodal import MultimodalReviewConfig, MultimodalReviewService


ALLOWED_SCHEMES = {"http", "https", "rtsp", "rtmp"}


def validate_source(source: str) -> str:
    if Path(source).is_file():
        return source
    parsed = urlparse(source)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("stream URL must use http(s), rtsp, or rtmp")
    return source


def probe_video_source(source: str, frames: int = 10, timeout_seconds: float = 15.0) -> dict:
    validate_source(source)
    started = time.perf_counter()
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        capture.release()
        raise RuntimeError("stream could not be opened")
    decoded = 0
    width = height = 0
    while decoded < frames and time.perf_counter() - started < timeout_seconds:
        ok, frame = capture.read()
        if not ok or frame is None:
            break
        decoded += 1; height, width = frame.shape[:2]
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0)
    capture.release()
    if decoded == 0:
        raise RuntimeError("stream opened but no video frame was decoded")
    return {
        "ok": True,
        "decoded_frames": decoded,
        "width": width,
        "height": height,
        "reported_fps": fps,
        "elapsed_seconds": time.perf_counter() - started,
    }


class CameraStreamService:
    def __init__(
        self,
        detector_config: RealtimeDetectorConfig | None = None,
        multimodal_config: MultimodalReviewConfig | None = None,
    ) -> None:
        self.detector_config = detector_config or RealtimeDetectorConfig()
        self.multimodal = MultimodalReviewService(
            multimodal_config or MultimodalReviewConfig()
        )
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._latest_jpeg: bytes | None = None
        self._events: deque[dict] = deque(maxlen=200)
        self._status: dict[str, object] = {
            "running": False,
            "state": "STOPPED",
            "camera_id": None,
            "frames_decoded": 0,
            "frames_processed": 0,
            "reconnects": 0,
            "last_error": None,
            "latest_result": None,
            "detector": asdict(self.detector_config),
        }

    def start(self, source: str, camera_id: str, process_every_n_frames: int = 1) -> dict:
        validate_source(source)
        if process_every_n_frames < 1:
            raise ValueError("process_every_n_frames must be positive")
        with self._lock:
            if self._thread and self._thread.is_alive():
                raise RuntimeError("a stream is already running")
            self.multimodal.reset_buffer()
            self._stop.clear()
            self._status.update(
                running=True, state="STARTING", camera_id=camera_id,
                frames_decoded=0, frames_processed=0, reconnects=0,
                last_error=None, latest_result=None,
            )
            self._thread = threading.Thread(
                target=self._run,
                args=(source, camera_id, process_every_n_frames),
                daemon=True,
                name="fall-camera-stream",
            )
            self._thread.start()
            return self.status()

    def stop(self, timeout_seconds: float = 10.0) -> dict:
        self._stop.set()
        thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout_seconds)
        with self._lock:
            self._status["running"] = bool(thread and thread.is_alive())
            if not self._status["running"]:
                self._status["state"] = "STOPPED"
        return self.status()

    def status(self) -> dict:
        with self._lock:
            result = dict(self._status)
            result["detector"] = {
                key: str(value) if isinstance(value, Path) else value
                for key, value in dict(result["detector"]).items()
            }
            latest = result.get("latest_result")
            if isinstance(latest, dict):
                latest = dict(latest)
                latest["multimodal_review"] = self.multimodal.status()
                result["latest_result"] = latest
            result["multimodal_review"] = self.multimodal.status()
            return result

    def trigger_multimodal_review(self) -> dict:
        with self._lock:
            latest = dict(self._status.get("latest_result") or {})
        prefall = latest.get("prefall_prediction") or {}
        triggered = self.multimodal.trigger(
            {
                "manual": True,
                "fall_state": latest.get("state"),
                "fall_probability": latest.get("fall_probability"),
                "prefall_risk_level": prefall.get("risk_level"),
                "prefall_probabilities": prefall.get("probabilities", {}),
                "pose_valid_ratio": latest.get("pose_valid_ratio"),
            },
            force=True,
        )
        return {"triggered": triggered, "review": self.multimodal.status()}

    def events(self, limit: int = 50) -> list[dict]:
        with self._lock:
            return list(self._events)[-max(1, min(limit, 200)):][::-1]

    def latest_jpeg(self) -> bytes | None:
        with self._lock:
            return self._latest_jpeg

    def _run(self, source: str, camera_id: str, every: int) -> None:
        capture = None
        try:
            detector = RealtimeFallDetector(self.detector_config)
            with self._lock: self._status["state"] = "CONNECTING"
            consecutive_failures = 0
            while not self._stop.is_set():
                if capture is None or not capture.isOpened():
                    if capture is not None: capture.release()
                    capture = cv2.VideoCapture(source)
                    if not capture.isOpened():
                        consecutive_failures += 1
                        with self._lock:
                            self._status["last_error"] = "stream open failed"
                            self._status["reconnects"] = int(self._status["reconnects"]) + 1
                        self._stop.wait(min(10.0, 1.5 * consecutive_failures))
                        continue
                    consecutive_failures = 0
                    source_fps = float(capture.get(cv2.CAP_PROP_FPS) or 30.0)
                    with self._lock: self._status["state"] = "RUNNING"
                ok, frame = capture.read()
                if not ok or frame is None:
                    capture.release(); capture = None
                    with self._lock:
                        self._status["reconnects"] = int(self._status["reconnects"]) + 1
                        self._status["last_error"] = "frame decode failed; reconnecting"
                    self._stop.wait(1.0)
                    continue
                with self._lock:
                    self._status["frames_decoded"] = int(self._status["frames_decoded"]) + 1
                    decoded = int(self._status["frames_decoded"])
                if decoded % every:
                    continue
                overlay, result, event = detector.process(frame, int(time.time() * 1000))
                self.multimodal.observe(frame)
                prefall = result.get("prefall_prediction") or {}
                risk = str(prefall.get("risk_level", "NORMAL"))
                should_review = risk in set(self.multimodal.config.trigger_levels) or str(
                    result.get("state")
                ) == "CONFIRMED"
                if should_review:
                    post_frames = max(0, round(
                        self.multimodal.config.post_trigger_seconds
                        * source_fps / every
                    ))
                    self.multimodal.schedule({
                        "manual": False,
                        "fall_state": result.get("state"),
                        "fall_probability": result.get("fall_probability"),
                        "prefall_risk_level": risk,
                        "prefall_probabilities": prefall.get("probabilities", {}),
                        "pose_valid_ratio": result.get("pose_valid_ratio"),
                    }, post_frames=post_frames)
                result["multimodal_review"] = self.multimodal.status()
                ok_jpeg, encoded = cv2.imencode(".jpg", overlay, [cv2.IMWRITE_JPEG_QUALITY, 82])
                with self._lock:
                    self._status["frames_processed"] = int(self._status["frames_processed"]) + 1
                    self._status["latest_result"] = result
                    if ok_jpeg: self._latest_jpeg = encoded.tobytes()
                    if event is not None:
                        self._events.append({
                            "event_id": str(uuid.uuid4()),
                            "camera_id": camera_id,
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            **event,
                        })
        except Exception as error:
            with self._lock:
                self._status["last_error"] = f"{type(error).__name__}: {str(error)[:200]}"
                self._status["state"] = "ERROR"
        finally:
            if capture is not None: capture.release()
            with self._lock: self._status["running"] = False
