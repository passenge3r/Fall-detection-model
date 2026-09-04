from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.ezviz import EzvizClient
from app.webapp import app


def mask_serial(serial: str) -> str:
    return f"***{serial[-4:]}" if serial else "***"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="End-to-end smoke test using a real EZVIZ camera stream"
    )
    parser.add_argument("--credentials-file", type=Path, required=True)
    parser.add_argument("--delete-credentials", action="store_true")
    parser.add_argument("--timeout", type=float, default=240.0)
    parser.add_argument("--probe-frames", type=int, default=10)
    parser.add_argument("--min-processed", type=int, default=70)
    parser.add_argument("--process-every-n-frames", type=int, default=1)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT / "results/ezviz_live_smoke",
    )
    args = parser.parse_args()

    try:
        credentials = json.loads(args.credentials_file.read_text(encoding="utf-8"))
    finally:
        if args.delete_credentials:
            args.credentials_file.unlink(missing_ok=True)

    client = EzvizClient(
        app_key=credentials.get("app_key"),
        app_secret=credentials.get("app_secret"),
        access_token=credentials.get("access_token"),
        timeout_seconds=30,
    )
    listed = client.list_devices()
    online = [device for device in listed["devices"] if device["online"]]
    if not online:
        raise RuntimeError("No online EZVIZ device is available")

    device = online[0]
    api = TestClient(app)
    protocol_names = {1: "EZOPEN", 4: "HTTP-FLV", 3: "RTMP", 2: "HLS"}
    protocol_results: list[dict] = []
    selected: tuple[int, object, dict] | None = None
    for protocol in (1, 4, 3, 2):
        started_at = time.perf_counter()
        address_ok = False
        try:
            address = client.live_address(
                str(device["device_serial"]),
                protocol=protocol,
                quality=2,
                expire_seconds=3600,
                device_code=credentials.get("device_code"),
            )
            address_ok = True
            source = {
                "source_type": "direct",
                "source_url": address.url,
                "camera_id": "ezviz-live",
            }
            if protocol == 1:
                protocol_results.append(
                    {
                        "protocol": protocol_names[protocol],
                        "address_ok": True,
                        "decodable_by_opencv": False,
                        "elapsed_seconds": time.perf_counter() - started_at,
                        "note": "Encrypted EZOPEN requires EZVIZ SDK; not selected for OpenCV",
                    }
                )
                continue
            probe = api.post(
                f"/v1/streams/probe?frames={args.probe_frames}", json=source
            )
            probe.raise_for_status()
            probe_data = probe.json()
            protocol_results.append(
                {
                    "protocol": protocol_names[protocol],
                    "address_ok": True,
                    "ok": True,
                    "elapsed_seconds": time.perf_counter() - started_at,
                    "probe": probe_data,
                }
            )
            if selected is None:
                selected = (protocol, address, probe_data)
        except Exception as error:
            protocol_results.append(
                {
                    "protocol": protocol_names[protocol],
                    "address_ok": address_ok,
                    "ok": False,
                    "elapsed_seconds": time.perf_counter() - started_at,
                    "error": f"{type(error).__name__}: {str(error)[:160]}",
                }
            )

    if selected is None:
        raise RuntimeError(
            "No protocol produced a decodable stream: "
            + json.dumps(protocol_results, ensure_ascii=False)
        )

    selected_protocol, address, selected_probe = selected
    source = {
        "source_type": "direct",
        "source_url": address.url,
        "camera_id": "ezviz-live",
    }
    started = api.post(
        "/v1/streams/start",
        json={
            **source,
            "process_every_n_frames": args.process_every_n_frames,
        },
    )
    started.raise_for_status()

    deadline = time.time() + args.timeout
    status: dict = {}
    while time.time() < deadline:
        status = api.get("/v1/streams/status").json()
        if status.get("state") == "ERROR":
            break
        if int(status.get("frames_processed") or 0) >= args.min_processed:
            break
        time.sleep(0.5)

    frame = api.get("/v1/frame.jpg")
    stopped = api.post("/v1/streams/stop").json()
    if status.get("state") == "ERROR":
        raise RuntimeError(str(status.get("last_error")))
    if int(status.get("frames_processed") or 0) < args.min_processed:
        raise RuntimeError(f"Timed out after processing {status.get('frames_processed', 0)} frames")
    if frame.status_code != 200:
        raise RuntimeError(f"No processed preview frame (HTTP {frame.status_code})")

    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "latest_frame.jpg").write_bytes(frame.content)
    summary = {
        "device": {
            "name": device.get("device_name"),
            "type": device.get("device_type"),
            "serial": mask_serial(str(device.get("device_serial") or "")),
            "online": True,
        },
        "stream": {
            "protocol": protocol_names[selected_protocol],
            "expires": address.expire_time,
            "probe": selected_probe,
            "protocol_comparison": protocol_results,
        },
        "running_status": status,
        "stopped_status": stopped,
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
