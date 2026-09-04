from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.webapp import app


def main() -> None:
    project = PROJECT
    parser = argparse.ArgumentParser(description="End-to-end local-video smoke test of the camera API")
    parser.add_argument(
        "--video",
        type=Path,
        default=project / "data/raw/GMDCSA24/Subject 1/Fall/01.mp4",
    )
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--min-processed", type=int, default=70)
    parser.add_argument(
        "--output-root", type=Path,
        default=project / "results/camera_service_smoke",
    )
    args = parser.parse_args(); args.output_root.mkdir(parents=True, exist_ok=True)
    client = TestClient(app)
    started = client.post("/v1/streams/start", json={
        "source_type": "direct",
        "source_url": str(args.video.resolve()),
        "camera_id": "local-smoke-camera",
    })
    started.raise_for_status(); deadline = time.time() + args.timeout
    status = {}
    while time.time() < deadline:
        status = client.get("/v1/streams/status").json()
        if status.get("state") == "ERROR": break
        if int(status.get("frames_processed") or 0) >= args.min_processed: break
        time.sleep(0.5)
    frame = client.get("/v1/frame.jpg")
    stopped = client.post("/v1/streams/stop").json()
    if status.get("state") == "ERROR":
        raise RuntimeError(status.get("last_error"))
    if int(status.get("frames_processed") or 0) < args.min_processed:
        raise RuntimeError(f"Timed out: {status}")
    if frame.status_code != 200:
        raise RuntimeError(f"No preview frame: {frame.status_code} {frame.text}")
    (args.output_root / "latest_frame.jpg").write_bytes(frame.content)
    summary = {"start": started.json(), "running_status": status, "stopped_status": stopped}
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
