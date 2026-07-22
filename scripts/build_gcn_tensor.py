from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sample_name(row: dict[str, str]) -> str:
    if row.get("start_frame") and row.get("end_frame"):
        return f"{row['path']}#f{row['start_frame']}-{row['end_frame']}"
    return row["path"]


def sequence_normalize(poses: np.ndarray, image_size: np.ndarray, threshold: float) -> np.ndarray:
    """Keep fall displacement while removing camera translation and subject scale."""
    coords = poses[..., :2].astype(np.float32)
    confidence = poses[..., 2].astype(np.float32)
    valid = confidence >= threshold

    centers = np.full((len(poses), 2), np.nan, dtype=np.float32)
    torso_lengths: list[float] = []
    bbox_diagonals: list[float] = []
    for frame in range(len(poses)):
        if valid[frame, 11] and valid[frame, 12]:
            centers[frame] = (coords[frame, 11] + coords[frame, 12]) / 2
        elif np.any(valid[frame]):
            centers[frame] = np.mean(coords[frame, valid[frame]], axis=0)

        if all(valid[frame, joint] for joint in (5, 6, 11, 12)):
            shoulder = (coords[frame, 5] + coords[frame, 6]) / 2
            hip = (coords[frame, 11] + coords[frame, 12]) / 2
            torso_lengths.append(float(np.linalg.norm(shoulder - hip)))
        if np.sum(valid[frame]) >= 2:
            extent = np.ptp(coords[frame, valid[frame]], axis=0)
            bbox_diagonals.append(float(np.linalg.norm(extent)))

    reference_candidates = centers[: min(8, len(centers))]
    reference_candidates = reference_candidates[np.all(np.isfinite(reference_candidates), axis=1)]
    if len(reference_candidates):
        reference = np.median(reference_candidates, axis=0)
    else:
        height, width = image_size
        reference = np.asarray([width / 2, height / 2], dtype=np.float32)

    positive_torso = [value for value in torso_lengths if value > 1]
    positive_bbox = [value for value in bbox_diagonals if value > 1]
    if positive_torso:
        scale = float(np.median(positive_torso))
    elif positive_bbox:
        scale = float(np.median(positive_bbox)) / 2
    else:
        scale = float(np.linalg.norm(image_size[::-1])) / 5
    scale = max(scale, 1.0)

    xy = (coords - reference[None, None, :]) / scale
    xy[~valid] = 0
    output = np.zeros((3, poses.shape[0], poses.shape[1], 1), dtype=np.float32)
    output[:2, :, :, 0] = xy.transpose(2, 0, 1)
    output[2, :, :, 0] = confidence
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    args = parser.parse_args()
    project_root = args.project_root.resolve()

    rows = read_rows(args.manifest)
    samples = []
    for row in rows:
        pose_path = Path(row["pose_path"])
        if not pose_path.is_absolute():
            candidates = (project_root / pose_path, project_root.parent / pose_path)
            pose_path = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
        if not pose_path.is_file():
            raise FileNotFoundError(f"Cannot resolve pose cache: {row['pose_path']} -> {pose_path}")
        with np.load(pose_path) as cached:
            poses = cached["keypoints"]
            image_size = cached["image_size"]
        if poses.shape[1:] != (17, 3):
            raise RuntimeError(f"Unexpected pose shape {poses.shape}: {pose_path}")
        samples.append(sequence_normalize(poses, image_size, args.confidence_threshold))

    data = np.stack(samples).astype(np.float32)
    labels = np.asarray([int(row["label"]) for row in rows], dtype=np.int64)
    names = np.asarray([sample_name(row) for row in rows])
    subjects = np.asarray([row.get("subject", row.get("scenario", "")) for row in rows])
    cameras = np.asarray([row.get("cam", "") for row in rows])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output, data=data, labels=labels, names=names, subjects=subjects, cameras=cameras
    )

    summary = {
        "output": args.output.as_posix(),
        "shape": list(data.shape),
        "layout": "N,C,T,V,M",
        "channels": ["x_centered_scaled", "y_centered_scaled", "confidence"],
        "samples": len(rows),
        "fall": int(np.sum(labels == 1)),
        "adl": int(np.sum(labels == 0)),
        "finite": bool(np.all(np.isfinite(data))),
        "confidence_threshold": args.confidence_threshold,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
