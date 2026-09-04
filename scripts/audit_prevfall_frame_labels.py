"""Audit Pre-VFall frame labels embedded in the distributed keypoint CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ID_PATTERN = re.compile(
    r"^(?P<video>[A-Z]+[1-9])[-_](?P<stage>[^_]+)-json_.*?_(?P<frame>\d+)_keypoints$"
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    class_counts: Counter[str] = Counter()
    video_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    unmatched = []
    with args.csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            match = ID_PATTERN.match(row["id"])
            if not match:
                unmatched.append(row["id"])
                continue
            item = {
                "frame": int(match.group("frame")),
                "stage": match.group("stage"),
                "class": int(row["class"]),
            }
            video_rows[match.group("video")].append(item)
            class_counts[str(item["class"])] += 1

    per_video = []
    for video, items in sorted(video_rows.items()):
        frames = [int(item["frame"]) for item in items]
        stages = Counter(str(item["stage"]) for item in items)
        classes = Counter(str(item["class"]) for item in items)
        fall_frames = [
            int(item["frame"]) for item in items
            if str(item["stage"]).lower() == "fall" or int(item["class"]) == 2
        ]
        abnormal_frames = [
            int(item["frame"]) for item in items
            if str(item["stage"]).lower() == "abnormal" or int(item["class"]) == 1
        ]
        per_video.append(
            {
                "video": video,
                "labeled_frames": len(items),
                "min_frame": min(frames),
                "max_frame": max(frames),
                "stage_counts": dict(stages),
                "class_counts": dict(classes),
                "abnormal_first_frame": min(abnormal_frames) if abnormal_frames else None,
                "fall_first_frame": min(fall_frames) if fall_frames else None,
                "fall_last_frame": max(fall_frames) if fall_frames else None,
            }
        )
    summary = {
        "matched_rows": sum(class_counts.values()),
        "unmatched_rows": len(unmatched),
        "videos": len(per_video),
        "class_counts": dict(class_counts),
        "videos_with_fall": sum(item["fall_first_frame"] is not None for item in per_video),
        "videos_with_abnormal": sum(item["abnormal_first_frame"] is not None for item in per_video),
        "per_video": per_video,
        "unmatched_examples": unmatched[:10],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "per_video"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
