from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.ezviz import EzvizClient
from app.ezviz_pc_sdk import EzvizPcSdkRecorder


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe EZVIZ PC SDK P2P capability")
    parser.add_argument("--credentials-file", type=Path, required=True)
    parser.add_argument("--delete-credentials", action="store_true")
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
    with EzvizPcSdkRecorder(
        app_key=str(credentials["app_key"]),
        access_token=str(credentials["access_token"]),
        device_serial=str(device["device_serial"]),
        device_code=str(credentials["device_code"]),
    ) as recorder:
        result = recorder.p2p_capabilities()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
