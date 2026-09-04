"""Convert OmniFall MCFD temporal segments into a video-level pre-fall manifest."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import cv2


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cameras", type=int, nargs="+", default=list(range(1, 9)))
    parser.add_argument(
        "--frame-labels", type=Path,
        help="Local MCFD data_tuple3.csv; uses exact frames instead of OmniFall timestamps",
    )
    args = parser.parse_args()

    selected_cameras = set(args.cameras)
    frame_onsets: dict[tuple[int, int], int] = {}
    if args.frame_labels:
        for row in read_rows(args.frame_labels):
            if int(float(row["label"])) != 1:
                continue
            scenario = int(float(row["chute"]))
            camera = int(float(row["cam"]))
            if camera == 55:
                camera = 5
            key = (scenario, camera)
            start = int(float(row["start"]))
            frame_onsets[key] = min(frame_onsets.get(key, start), start)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(args.labels):
        if int(row["cam"]) in selected_cameras:
            grouped[row["path"]].append(row)

    output_rows = []
    missing = []
    invalid_onsets = []
    for omnifall_path, rows in sorted(grouped.items()):
        fall_segments = [row for row in rows if int(row["label"]) == 1]
        if not fall_segments:
            continue
        scenario_text, camera_text = omnifall_path.split("/")
        scenario = int(scenario_text.removeprefix("chute"))
        camera = int(camera_text.removeprefix("cam"))
        relative = f"dataset/dataset/chute{scenario:02d}/cam{camera}.avi"
        video = args.video_root / relative
        if not video.is_file():
            missing.append(relative)
            continue
        capture = cv2.VideoCapture(str(video))
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        capture.release()
        duration = frames / fps if fps > 0 else 0.0
        onset_frame = frame_onsets.get((scenario, camera))
        if onset_frame is not None:
            onset = onset_frame / fps
        else:
            onset = min(float(row["start"]) for row in fall_segments)
            onset_frame = int(round(onset * fps))
        if not (0 < onset_frame < frames):
            invalid_onsets.append({
                "path": relative, "onset_frame": onset_frame, "frames": frames,
                "onset_seconds": onset, "duration": duration,
            })
        output_rows.append({
            "path": relative,
            "label": 1,
            # MCFD does not expose reliable subject IDs. Scenario is used only
            # as a grouping key to prevent multi-view leakage.
            "subject": scenario,
            "dataset": "mcfd",
            "scenario": scenario,
            "cam": camera,
            "fall_onset_frame": onset_frame,
            "fall_onset_seconds": f"{onset:.6f}",
            "fps": f"{fps:.6f}",
            "frames": frames,
            "duration_seconds": f"{duration:.6f}",
        })

    fields = [
        "path", "label", "subject", "dataset", "scenario", "cam",
        "fall_onset_frame", "fall_onset_seconds", "fps", "frames", "duration_seconds",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    audit = {
        "videos": len(output_rows),
        "cameras": sorted(selected_cameras),
        "scenarios": sorted({int(row["scenario"]) for row in output_rows}),
        "missing": missing,
        "invalid_onsets": invalid_onsets,
        "warning": "MCFD subject identity unavailable; scenario IDs only prevent multi-view leakage",
        "ok": bool(output_rows) and not missing and not invalid_onsets,
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
