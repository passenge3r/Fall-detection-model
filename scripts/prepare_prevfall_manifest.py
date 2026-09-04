"""Build a video-level manifest for the selectively downloaded Pre-VFall data."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import cv2


SCENARIOS = {
    "confusion_delirium": ("confusion_delirium", False),
    "confusion_nph": ("confusion_nph", False),
    "dizziness_fall_forward": ("dizziness", True),
    "dizziness_fall_side": ("dizziness", True),
    "weakness_fall_forward": ("weakness", True),
    "weakness_fall_side": ("weakness", True),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frame-label-audit", type=Path)
    args = parser.parse_args()
    frame_labels = {}
    if args.frame_label_audit:
        audit = json.loads(args.frame_label_audit.read_text(encoding="utf-8"))
        frame_labels = {item["video"]: item for item in audit["per_video"]}
    videos = sorted(args.root.rglob("*.mp4"))
    rows = []
    for path in videos:
        scenario_folder = path.parent.name
        if scenario_folder not in SCENARIOS:
            raise RuntimeError(f"Unknown scenario folder: {path}")
        scenario, contains_fall = SCENARIOS[scenario_folder]
        match = re.search(r"([1-9])$", path.stem)
        if not match:
            raise RuntimeError(f"Cannot infer subject from {path.name}")
        subject = int(match.group(1))
        frame_label = frame_labels.get(path.stem, {})
        prefix = path.stem[:-1]
        view = "front" if prefix.endswith("FM") else "side" if prefix.endswith("SM") else "unknown"
        fall_direction = (
            "forward" if scenario_folder.endswith("_forward")
            else "side" if scenario_folder.endswith("_side")
            else "none"
        )
        capture = cv2.VideoCapture(str(path))
        opened = capture.isOpened()
        fps = float(capture.get(cv2.CAP_PROP_FPS)) if opened else 0.0
        frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) if opened else 0
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) if opened else 0
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) if opened else 0
        first_ok, _ = capture.read() if opened else (False, None)
        capture.release()
        rows.append(
            {
                "path": path.as_posix(),
                "subject": subject,
                "dataset": "PreVFall",
                "label": int(contains_fall),
                "scenario": scenario,
                "scenario_folder": scenario_folder,
                "contains_fall": int(contains_fall),
                "fall_direction": fall_direction,
                "view": view,
                "fps": fps,
                "frame_count": frames,
                "duration_seconds": frames / fps if fps else 0.0,
                "width": width,
                "height": height,
                "readable": int(opened and first_ok and frames > 0 and fps > 0),
                "abnormal_onset_frame": frame_label.get("abnormal_first_frame") or "",
                "fall_onset_frame": frame_label.get("fall_first_frame") or "",
                "fall_end_frame": frame_label.get("fall_last_frame") or "",
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "videos": len(rows),
        "subjects": sorted({row["subject"] for row in rows}),
        "readable": sum(row["readable"] for row in rows),
        "contains_fall": sum(row["contains_fall"] for row in rows),
        "fall_onset_available": sum(row["fall_onset_frame"] != "" for row in rows),
        "scenario_counts": dict(Counter(row["scenario_folder"] for row in rows)),
        "view_counts": dict(Counter(row["view"] for row in rows)),
        "fps_values": sorted({row["fps"] for row in rows}),
        "resolution_counts": dict(Counter(f"{row['width']}x{row['height']}" for row in rows)),
        "duration_seconds": {
            "min": min(row["duration_seconds"] for row in rows),
            "max": max(row["duration_seconds"] for row in rows),
            "total": sum(row["duration_seconds"] for row in rows),
        },
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
