from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parent.parent


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_stem(relative_path: str) -> str:
    path = Path(relative_path)
    return "__".join(path.with_suffix("").parts).replace(" ", "_")


def cache_stem(row: dict[str, str]) -> str:
    stem = safe_stem(row["path"])
    if row.get("start_frame") and row.get("end_frame"):
        stem += f"__f{row['start_frame']}_{row['end_frame']}"
    return stem


def track_video(model: object, path: Path, device: str,
                confidence: float) -> tuple[list[dict[int, tuple[np.ndarray, float]]], np.ndarray]:
    observations: list[dict[int, tuple[np.ndarray, float]]] = []
    track_counts: defaultdict[int, int] = defaultdict(int)
    track_area: defaultdict[int, float] = defaultdict(float)
    image_size: tuple[int, int] | None = None

    results = model.track(
        source=str(path), stream=True, persist=True, tracker="bytetrack.yaml",
        device=device, conf=confidence, verbose=False,
    )
    for result in results:
        if image_size is None:
            image_size = tuple(int(value) for value in result.orig_shape)
        frame_tracks: dict[int, tuple[np.ndarray, float]] = {}
        boxes = result.boxes
        keypoints = result.keypoints
        if (
            boxes is not None and keypoints is not None and boxes.id is not None
            and len(boxes) == len(keypoints.data)
        ):
            ids = boxes.id.detach().cpu().numpy().astype(np.int64)
            xyxy = boxes.xyxy.detach().cpu().numpy()
            poses = keypoints.data.detach().cpu().numpy().astype(np.float32)
            for track_id, box, pose in zip(ids, xyxy, poses):
                if pose.shape != (17, 3):
                    continue
                identity = int(track_id)
                area = float(max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1]))
                frame_tracks[identity] = (pose, area)
                track_counts[identity] += 1
                track_area[identity] += area
        observations.append(frame_tracks)

    if not observations or image_size is None:
        raise RuntimeError(f"No frames decoded from {path}")
    return observations, np.asarray(image_size, dtype=np.int32)


def sample_interval(
    observations: list[dict[int, tuple[np.ndarray, float]]], start: int, end: int, frames: int
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    track_counts: defaultdict[int, int] = defaultdict(int)
    track_area: defaultdict[int, float] = defaultdict(float)
    for frame in observations[start:end + 1]:
        for identity, (_, area) in frame.items():
            track_counts[identity] += 1
            track_area[identity] += area
    primary = (
        max(track_counts, key=lambda identity: (track_counts[identity], track_area[identity]))
        if track_counts else -1
    )
    indices = np.rint(np.linspace(start, end, frames)).astype(np.int32)
    zero = np.zeros((17, 3), dtype=np.float32)
    poses = np.stack([
        observations[int(index)].get(primary, (zero, 0.0))[0] for index in indices
    ]).astype(np.float32)
    metadata = {
        "source_frames": len(observations),
        "track_count": len(track_counts),
        "primary_track_id": primary,
        "primary_track_coverage": track_counts.get(primary, 0) / (end - start + 1),
    }
    return poses, indices, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument("--model", type=Path, default=PROJECT / "models/yolo26n-pose.pt")
    parser.add_argument("--frames", type=int, default=64)
    parser.add_argument("--confidence", type=float, default=0.1)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    os.environ.setdefault("YOLO_CONFIG_DIR", str(PROJECT / ".ultralytics"))
    from ultralytics import YOLO

    rows = read_rows(args.manifest)
    if args.limit is not None:
        rows = rows[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(args.model))
    output_rows: list[dict[str, str]] = []
    tracked_videos: dict[str, tuple[list[dict[int, tuple[np.ndarray, float]]], np.ndarray]] = {}
    for number, row in enumerate(rows, 1):
        output_path = args.output_dir / f"{cache_stem(row)}.npz"
        if not output_path.exists() or args.overwrite:
            if row["path"] not in tracked_videos:
                tracked_videos[row["path"]] = track_video(
                    model, args.video_root / row["path"], args.device, args.confidence
                )
            observations, image_size = tracked_videos[row["path"]]
            start = int(row["start_frame"]) if row.get("start_frame") else 0
            end = int(row["end_frame"]) if row.get("end_frame") else len(observations) - 1
            if start < 0 or end < start or end >= len(observations):
                raise RuntimeError(
                    f"Invalid interval [{start}, {end}] for {row['path']} ({len(observations)} frames)"
                )
            poses, indices, metadata = sample_interval(observations, start, end, args.frames)
            np.savez_compressed(
                output_path, keypoints=poses, frame_indices=indices,
                image_size=image_size,
                source_frames=np.asarray(metadata["source_frames"]),
                track_count=np.asarray(metadata["track_count"]),
                primary_track_id=np.asarray(metadata["primary_track_id"]),
                primary_track_coverage=np.asarray(metadata["primary_track_coverage"]),
            )
        with np.load(output_path) as cached:
            poses = cached["keypoints"]
            source_frames = int(cached["source_frames"])
            track_count = int(cached["track_count"])
            primary_track_id = int(cached["primary_track_id"])
            coverage = float(cached["primary_track_coverage"])
        confidence_values = poses[:, :, 2]
        output_rows.append({
            **row,
            "pose_path": output_path.as_posix(),
            "backend": "yolo_bytetrack",
            "frames": str(args.frames),
            "zero_pose_frames": str(int(np.sum(np.max(confidence_values, axis=1) == 0))),
            "mean_confidence": f"{float(np.mean(confidence_values)):.6f}",
            "source_frames": str(source_frames),
            "track_count": str(track_count),
            "primary_track_id": str(primary_track_id),
            "primary_track_coverage": f"{coverage:.6f}",
        })
        print(f"[{number}/{len(rows)}] {row['path']} coverage={coverage:.3f}", flush=True)

    with args.output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    summary = {
        "videos": len(output_rows),
        "mean_primary_track_coverage": float(np.mean([
            float(row["primary_track_coverage"]) for row in output_rows
        ])),
        "mean_track_count": float(np.mean([int(row["track_count"]) for row in output_rows])),
        "zero_pose_frames": sum(int(row["zero_pose_frames"]) for row in output_rows),
    }
    args.output_manifest.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
