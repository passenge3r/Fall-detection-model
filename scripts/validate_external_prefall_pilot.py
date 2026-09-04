"""Validate the cached MCFD external-data pilot artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pose-dir",
        type=Path,
        default=Path("data/poses/mcfd_cam1_rtmpose_full"),
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/gcn/mcfd_cam1_rtmpose_prefall_w64_s16_h123.npz"),
    )
    parser.add_argument(
        "--merged-dataset",
        type=Path,
        default=Path(
            "data/gcn/gmdcsa24_mcfdcam1_rtmpose_prefall_w64_s16_h123.npz"
        ),
    )
    parser.add_argument(
        "--merged-splits",
        type=Path,
        default=Path("data/splits/gmdcsa24_mcfdcam1_prefall_loso"),
    )
    parser.add_argument("--expected-videos", type=int, default=23)
    parser.add_argument("--expected-fps", type=float, default=30.0)
    parser.add_argument("--expected-sample-step", type=int, default=4)
    parser.add_argument("--expected-windows", type=int, default=168)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pose_files = sorted(args.pose_dir.glob("*.npz"))
    assert len(pose_files) == args.expected_videos, (
        f"expected {args.expected_videos} pose files, got {len(pose_files)}"
    )

    fps_values: set[float] = set()
    sample_steps: set[int] = set()
    sampled_frames = 0
    zero_pose_frames = 0
    irregular_files: list[str] = []

    for path in pose_files:
        with np.load(path, allow_pickle=True) as pose:
            frame_indices = pose["frame_indices"]
            fps_values.add(float(pose["fps"]))
            sample_step = int(pose["sample_step"])
            sample_steps.add(sample_step)
            sampled_frames += len(frame_indices)
            keypoints = pose["keypoints"]
            zero_pose_frames += int((keypoints[..., 2].max(axis=1) == 0).sum())
            if len(frame_indices) > 1 and not np.all(
                np.diff(frame_indices) == sample_step
            ):
                irregular_files.append(path.name)

    assert not irregular_files, f"irregular frame indices: {irregular_files}"
    assert fps_values == {args.expected_fps}, fps_values
    assert sample_steps == {args.expected_sample_step}, sample_steps

    with np.load(args.dataset, allow_pickle=True) as dataset:
        assert len(dataset["data"]) == args.expected_windows
        assert np.isfinite(dataset["data"]).all()
        labels = dataset["labels"]
        supplemental_names = set(map(str, dataset["names"]))
        result = {
            "pose_files": len(pose_files),
            "sampled_frames": sampled_frames,
            "zero_pose_frames": zero_pose_frames,
            "zero_pose_rate": zero_pose_frames / sampled_frames,
            "fps": sorted(fps_values),
            "sample_steps": sorted(sample_steps),
            "windows": len(dataset["data"]),
            "y1_positive": int(labels[:, 0].sum()),
            "y2_positive": int(labels[:, 1].sum()),
            "y3_positive": int(labels[:, 2].sum()),
        }

    with np.load(args.merged_dataset, allow_pickle=True) as merged:
        merged_names = set(map(str, merged["names"]))
    assert supplemental_names <= merged_names
    fold_summary = {}
    for fold in range(1, 5):
        fold_dir = args.merged_splits / f"fold_{fold}"
        split_names = {}
        for split in ("train", "val", "test"):
            with (fold_dir / f"{split}.csv").open(
                "r", encoding="utf-8-sig"
            ) as handle:
                rows = [line.strip() for line in handle.readlines()[1:] if line.strip()]
            split_names[split] = set(rows)
        assert supplemental_names <= split_names["train"]
        assert not (supplemental_names & split_names["val"])
        assert not (supplemental_names & split_names["test"])
        fold_summary[str(fold)] = {
            "supplement_in_train": len(supplemental_names & split_names["train"]),
            "supplement_in_val": len(supplemental_names & split_names["val"]),
            "supplement_in_test": len(supplemental_names & split_names["test"]),
        }
    result["split_isolation"] = fold_summary

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
