"""Build 64-frame RTMPose tensors aligned with the posture-5 video segments."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from build_gcn_tensor import sequence_normalize
from extract_full_video_rtmpose import cache_name


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path,
        default=project / "data/metadata/gmdcsa24_posture5_segments.csv",
    )
    parser.add_argument(
        "--pose-dir", type=Path,
        default=project / "data/poses/gmdcsa24_rtmpose_full",
    )
    parser.add_argument(
        "--output", type=Path,
        default=project / "data/gcn/gmdcsa24_posture5_rtmpose_t64.npz",
    )
    parser.add_argument("--frames", type=int, default=64)
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    args = parser.parse_args()
    rows = read_csv(args.manifest)
    samples = []
    valid_ratios = []
    for position, row in enumerate(rows, 1):
        cache_path = args.pose_dir / cache_name(row["video_path"])
        if not cache_path.is_file():
            raise FileNotFoundError(cache_path)
        with np.load(cache_path) as cache:
            poses = cache["keypoints"].astype(np.float32)
            image_size = cache["image_size"]
            fps = float(cache["fps"])
        start = max(0, min(int(round(float(row["start_seconds"]) * fps)), len(poses) - 1))
        end = max(start, min(int(round(float(row["end_seconds"]) * fps)) - 1, len(poses) - 1))
        indices = np.linspace(start, end, args.frames).round().astype(int)
        segment = poses[indices]
        samples.append(sequence_normalize(segment, image_size, args.confidence_threshold))
        valid_ratios.append(
            float(np.mean(np.max(segment[:, :, 2], axis=1) >= args.confidence_threshold))
        )
        print(f"[{position}/{len(rows)}] f{start}-{end} {row['segment_id']}", flush=True)
    data = np.stack(samples).astype(np.float32)
    labels = np.asarray([int(row["label"]) for row in rows], dtype=np.int64)
    names = np.asarray([row["segment_id"] for row in rows])
    subjects = np.asarray([row["subject"] for row in rows])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output, data=data, labels=labels, names=names, subjects=subjects,
        cameras=np.asarray([""] * len(rows)),
    )
    summary = {
        "shape": list(data.shape), "samples": len(rows),
        "class_counts": {str(label): int(np.sum(labels == label)) for label in range(5)},
        "mean_pose_valid_ratio": float(np.mean(valid_ratios)),
        "minimum_pose_valid_ratio": float(np.min(valid_ratios)),
        "finite": bool(np.all(np.isfinite(data))),
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
