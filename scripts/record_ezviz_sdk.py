from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.ezviz import EzvizClient
from app.ezviz_pc_sdk import EzvizPcSdkRecorder


def mask_serial(serial: str) -> str:
    return f"***{serial[-4:]}" if serial else "***"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture an encrypted EZOPEN live stream with EZVIZ PC SDK"
    )
    parser.add_argument("--credentials-file", type=Path, required=True)
    parser.add_argument("--delete-credentials", action="store_true")
    parser.add_argument("--duration", type=float, default=15.0)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT / "results/ezviz_sdk_smoke",
    )
    args = parser.parse_args()
    try:
        credentials = json.loads(args.credentials_file.read_text(encoding="utf-8"))
    finally:
        if args.delete_credentials:
            args.credentials_file.unlink(missing_ok=True)

    devices = EzvizClient(
        app_key=credentials.get("app_key"),
        app_secret=credentials.get("app_secret"),
        access_token=credentials.get("access_token"),
        timeout_seconds=30,
    ).list_devices()["devices"]
    online = [device for device in devices if device["online"]]
    if not online:
        raise RuntimeError("No online EZVIZ device is available")
    device = online[0]

    args.output_root.mkdir(parents=True, exist_ok=True)
    capture_path = args.output_root / "capture.mp4"
    with EzvizPcSdkRecorder(
        app_key=str(credentials["app_key"]),
        access_token=str(credentials["access_token"]),
        device_serial=str(device["device_serial"]),
        device_code=str(credentials["device_code"]),
    ) as recorder:
        capture = recorder.record(capture_path, args.duration)

    summary = {
        "device": {
            "name": device.get("device_name"),
            "type": device.get("device_type"),
            "serial": mask_serial(str(device.get("device_serial") or "")),
            "online": True,
        },
        "capture": {
            **asdict(capture),
            "output_path": str(capture.output_path),
        },
    }
    (args.output_root / "sdk_capture_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
