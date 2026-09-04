from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from app.pose_quality import PoseQualityConfig, assess_pose_frame  # noqa: E402
ROUTES = (
    (
        "RTMPose+ST-GCN++",
        "RTMPose+ST-GCN++_probability",
        "data/metadata/mcfd_rtmpose_t64.csv",
    ),
    (
        "YOLO-Pose+ST-GCN++",
        "YOLO-Pose+ST-GCN++_probability",
        "data/metadata/mcfd_yolo_t64_c010.csv",
    ),
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pose_index(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["path"], row["start_frame"], row["end_frame"]): row
        for row in read_rows(path)
    }


def resolve_cache(path: str) -> Path:
    value = Path(path)
    candidates = (value, PROJECT / value, PROJECT.parent / value)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Cannot resolve {path}; tried {candidates}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate abstaining pose-quality gates on frozen MCFD predictions"
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        default=PROJECT / "results/mcfd_error_analysis/all_cross_view_samples.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT / "results/mcfd_pose_quality_gate",
    )
    parser.add_argument("--min-pose-valid-ratio", type=float, default=0.5)
    parser.add_argument("--min-valid-joints", type=int, default=5)
    parser.add_argument("--min-torso-joints", type=int, default=2)
    parser.add_argument("--max-bone-image-ratio", type=float, default=0.35)
    parser.add_argument("--max-center-jump-ratio", type=float, default=0.25)
    args = parser.parse_args()

    config = PoseQualityConfig(
        min_valid_joints=args.min_valid_joints,
        min_torso_joints=args.min_torso_joints,
        max_bone_image_ratio=args.max_bone_image_ratio,
        max_center_jump_ratio=args.max_center_jump_ratio,
    )
    predictions = read_rows(args.predictions)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sample_rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []

    for route, probability_column, manifest_path in ROUTES:
        manifest = pose_index(PROJECT / manifest_path)
        baseline_correct = 0
        classified_correct = 0
        classified = 0
        unknown = 0
        blocked_errors = 0
        blocked_correct = 0
        reason_totals: Counter[str] = Counter()

        for row in predictions:
            key = (row["path"], row["start_frame"], row["end_frame"])
            pose_row = manifest[key]
            with np.load(resolve_cache(pose_row["pose_path"])) as cache:
                poses = cache["keypoints"].astype(np.float32)
                image_size = cache["image_size"].astype(np.float32)

            usable_frames = 0
            previous_pose = None
            reasons: Counter[str] = Counter()
            for pose in poses:
                quality = assess_pose_frame(
                    pose, image_size, config, previous_pose=previous_pose
                )
                if quality.usable:
                    usable_frames += 1
                    previous_pose = pose
                else:
                    reasons.update(quality.reasons)
            reason_totals.update(reasons)

            valid_ratio = usable_frames / len(poses)
            is_unknown = valid_ratio < args.min_pose_valid_ratio
            label = int(row["label"])
            probability = float(row[probability_column])
            prediction = int(probability >= 0.5)
            correct = prediction == label
            baseline_correct += int(correct)
            if is_unknown:
                unknown += 1
                blocked_correct += int(correct)
                blocked_errors += int(not correct)
                decision = "UNKNOWN"
            else:
                classified += 1
                classified_correct += int(correct)
                decision = "FALL" if prediction else "ADL"

            sample_rows.append(
                {
                    "route": route,
                    "sample": row["sample"],
                    "label": label,
                    "probability": f"{probability:.8f}",
                    "baseline_prediction": prediction,
                    "pose_valid_ratio": f"{valid_ratio:.6f}",
                    "quality_decision": decision,
                    "baseline_correct": int(correct),
                    "quality_reasons": json.dumps(
                        dict(reasons), ensure_ascii=False, sort_keys=True
                    ),
                }
            )

        total = len(predictions)
        summaries.append(
            {
                "route": route,
                "samples": total,
                "baseline_accuracy": baseline_correct / total,
                "coverage": classified / total,
                "unknown": unknown,
                "blocked_errors": blocked_errors,
                "blocked_correct": blocked_correct,
                "selective_accuracy": (
                    classified_correct / classified if classified else None
                ),
                "reason_totals": dict(reason_totals),
            }
        )

    with (args.output_dir / "samples.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample_rows[0]))
        writer.writeheader()
        writer.writerows(sample_rows)
    (args.output_dir / "summary.json").write_text(
        json.dumps(
            {
                "config": {
                    "min_pose_valid_ratio": args.min_pose_valid_ratio,
                    "min_valid_joints": config.min_valid_joints,
                    "min_torso_joints": config.min_torso_joints,
                    "max_bone_image_ratio": config.max_bone_image_ratio,
                    "max_center_jump_ratio": config.max_center_jump_ratio,
                },
                "routes": summaries,
                "interpretation": (
                    "UNKNOWN is an abstention, not a correct prediction. "
                    "Report coverage and selective accuracy together."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
