"""Build a five-class posture/action segment manifest from GMDCSA24 CSV labels."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


CLASS_BLOCK = re.compile(
    r"(?P<name>Falling|Fall|Walking|Standing|Sitting|Sleeping)"
    r"(?:\s*\([^)]*\))?\s*\[(?P<ranges>[^\]]+)\]",
    re.IGNORECASE,
)
RANGE = re.compile(r"(?P<start>[0-9.]+)\s*(?:to\s*)?(?P<end>[0-9.]+)")
CLASS_MAP = {
    "walking": (0, "walking"),
    "standing": (1, "standing"),
    "sitting": (2, "sitting"),
    "sleeping": (3, "lying_sleeping"),
    "falling": (4, "falling"),
    "fall": (4, "falling"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_intervals(text: str) -> list[tuple[int, str, float, float]]:
    intervals = []
    for block in CLASS_BLOCK.finditer(text):
        class_id, class_name = CLASS_MAP[block.group("name").lower()]
        for match in RANGE.finditer(block.group("ranges")):
            start, end = float(match.group("start")), float(match.group("end"))
            # The source has one known reversed typo, Sitting[9.7 to 3].
            # Description and neighboring intervals show that 3--9.7 is intended.
            if end < start:
                start, end = end, start
            intervals.append((class_id, class_name, start, end))
    return intervals


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/GMDCSA24")
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "data/metadata/gmdcsa24_posture5_segments.csv",
    )
    parser.add_argument("--min-duration", type=float, default=0.5)
    args = parser.parse_args()

    output_rows: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []
    for subject_dir in sorted(args.video_root.glob("Subject *")):
        subject = subject_dir.name.split()[-1]
        for source_kind in ("ADL", "Fall"):
            annotation_path = subject_dir / f"{source_kind}.csv"
            for row in read_csv(annotation_path):
                class_text = next(
                    value for key, value in row.items() if key and key.strip() == "Classes"
                )
                video_path = f"{subject_dir.name}/{source_kind}/{row['File Name']}"
                intervals = parse_intervals(class_text)
                if not intervals:
                    rejected.append({"path": video_path, "reason": "no posture interval"})
                for ordinal, (class_id, class_name, start, end) in enumerate(intervals, 1):
                    duration = end - start
                    if duration < args.min_duration:
                        rejected.append(
                            {
                                "path": video_path,
                                "class_name": class_name,
                                "start_seconds": start,
                                "end_seconds": end,
                                "reason": f"duration<{args.min_duration}",
                            }
                        )
                        continue
                    output_rows.append(
                        {
                            "segment_id": f"{video_path}#t{start:.3f}-{end:.3f}-{class_name}-{ordinal}",
                            "video_path": video_path,
                            "label": class_id,
                            "class_name": class_name,
                            "subject": subject,
                            "source_kind": source_kind.lower(),
                            "start_seconds": f"{start:.6f}",
                            "end_seconds": f"{end:.6f}",
                            "duration_seconds": f"{duration:.6f}",
                            "description": row.get("Description", ""),
                            "source_classes": class_text,
                        }
                    )

    if not output_rows:
        raise RuntimeError("No posture segments were parsed")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    by_subject: dict[str, dict[str, int]] = defaultdict(dict)
    for subject in sorted({str(row["subject"]) for row in output_rows}, key=int):
        counts = Counter(
            str(row["class_name"]) for row in output_rows if str(row["subject"]) == subject
        )
        by_subject[subject] = dict(sorted(counts.items()))
    summary = {
        "classes": {str(value[0]): value[1] for value in CLASS_MAP.values()},
        "samples": len(output_rows),
        "class_counts": dict(Counter(str(row["class_name"]) for row in output_rows)),
        "subject_class_counts": by_subject,
        "min_duration_seconds": args.min_duration,
        "rejected": rejected,
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
