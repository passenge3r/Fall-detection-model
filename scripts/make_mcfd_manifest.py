from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2


FIELDS = [
    "path", "label", "start_frame", "end_frame", "scenario", "cam", "dataset", "source_row"
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        return -1
    count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--metadata-out", type=Path, required=True)
    parser.add_argument("--splits-out", type=Path, required=True)
    args = parser.parse_args()

    with args.annotations.open("r", encoding="utf-8-sig", newline="") as handle:
        source = list(csv.DictReader(handle))

    rows: list[dict[str, str]] = []
    corrections: list[dict[str, object]] = []
    missing: list[str] = []
    out_of_range: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    for index, item in enumerate(source, start=2):
        scenario = int(float(item["chute"]))
        cam = int(float(item["cam"]))
        if cam == 55:
            corrections.append({"csv_row": index, "field": "cam", "from": 55, "to": 5})
            cam = 5
        relative = f"dataset/dataset/chute{scenario:02d}/cam{cam}.avi"
        video = args.video_root / relative
        start = int(float(item["start"]))
        end = int(float(item["end"]))
        if not video.is_file():
            missing.append(relative)
        elif relative not in counts:
            counts[relative] = frame_count(video)
        if relative in counts and (start < 0 or end < start or end >= counts[relative]):
            out_of_range.append(
                {"csv_row": index, "path": relative, "start": start, "end": end, "frames": counts[relative]}
            )
        rows.append(
            {
                "path": relative,
                "label": str(int(float(item["label"]))),
                "start_frame": str(start),
                "end_frame": str(end),
                "scenario": str(scenario),
                "cam": str(cam),
                "dataset": "mcfd",
                "source_row": str(index),
            }
        )

    write_csv(args.metadata_out, rows)
    write_csv(args.splits_out / "all_external.csv", rows)
    for cam in range(1, 9):
        write_csv(args.splits_out / "by_camera" / f"cam{cam}.csv", [r for r in rows if r["cam"] == str(cam)])
    write_csv(args.splits_out / "calibration_cam1.csv", [r for r in rows if r["cam"] == "1"])
    write_csv(args.splits_out / "development_cam3.csv", [r for r in rows if r["cam"] == "3"])
    write_csv(args.splits_out / "test_cross_view.csv", [r for r in rows if r["cam"] not in {"1", "3"}])

    annotated_scenarios = sorted({int(row["scenario"]) for row in rows})
    video_scenarios = sorted(
        int(path.name.removeprefix("chute"))
        for path in (args.video_root / "dataset" / "dataset").glob("chute*")
    )
    audit = {
        "segments": len(rows),
        "fall_segments": sum(row["label"] == "1" for row in rows),
        "adl_segments": sum(row["label"] == "0" for row in rows),
        "videos_referenced": len({row["path"] for row in rows}),
        "cameras": sorted({int(row["cam"]) for row in rows}),
        "annotated_scenarios": annotated_scenarios,
        "unannotated_video_scenarios": sorted(set(video_scenarios) - set(annotated_scenarios)),
        "corrections": corrections,
        "missing_videos": sorted(set(missing)),
        "out_of_range_segments": out_of_range,
        "ok": not missing and not out_of_range and len(rows) == 552,
    }
    (args.splits_out / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
