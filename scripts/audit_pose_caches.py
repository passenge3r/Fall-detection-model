from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_pose(row: dict[str, str], root: Path) -> Path:
    path = Path(row["pose_path"])
    return path if path.is_absolute() else root / path


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    by_label: dict[str, dict[str, int]] = {}
    for label, name in (("0", "adl"), ("1", "fall")):
        selected = [row for row in rows if row["label"] == label]
        zeros = sum(int(row["zero_pose_frames"]) for row in selected)
        frames = sum(int(row["frames"]) for row in selected)
        by_label[name] = {
            "videos": len(selected),
            "frames": frames,
            "zero_pose_frames": zeros,
            "zero_pose_rate_ppm": round(1_000_000 * zeros / frames) if frames else 0,
        }
    total_frames = sum(int(row["frames"]) for row in rows)
    total_zeros = sum(int(row["zero_pose_frames"]) for row in rows)
    return {
        "backend": rows[0]["backend"] if rows else None,
        "videos": len(rows),
        "frames": total_frames,
        "zero_pose_frames": total_zeros,
        "zero_pose_rate": total_zeros / total_frames if total_frames else 0,
        "mean_confidence": float(np.mean([float(row["mean_confidence"]) for row in rows])),
        "by_label": by_label,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    all_rows = [read_rows(path) for path in args.manifest]
    reference = all_rows[0]
    checks = {"same_row_count": True, "same_order_labels_subjects": True, "same_frame_indices": True}
    for rows in all_rows[1:]:
        if len(rows) != len(reference):
            checks["same_row_count"] = False
            checks["same_order_labels_subjects"] = False
            checks["same_frame_indices"] = False
            continue
        for left, right in zip(reference, rows):
            keys = ("path", "label", "subject", "scenario", "cam", "start_frame", "end_frame")
            if any(left.get(key, "") != right.get(key, "") for key in keys):
                checks["same_order_labels_subjects"] = False
            with np.load(resolve_pose(left, args.project_root)) as left_pose, np.load(
                resolve_pose(right, args.project_root)
            ) as right_pose:
                if not np.array_equal(left_pose["frame_indices"], right_pose["frame_indices"]):
                    checks["same_frame_indices"] = False

    report = {
        "checks": checks,
        "manifests": {
            str(path): summarize(rows) for path, rows in zip(args.manifest, all_rows)
        },
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
