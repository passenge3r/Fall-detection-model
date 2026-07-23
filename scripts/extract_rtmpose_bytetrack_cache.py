from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from extract_bytetrack_pose_cache import cache_stem, read_rows


PROJECT = Path(__file__).resolve().parent.parent


class RTMPoseMatcher:
    """Run RTMPose and select the person associated with a ByteTrack box."""

    def __init__(self, mode: str, device: str) -> None:
        self._dll_handles = []
        if device.lower().startswith("cuda"):
            import onnxruntime as ort

            nvidia_root = Path(ort.__file__).resolve().parent.parent / "nvidia"
            dll_dirs = [nvidia_root / "cu13" / "bin" / "x86_64", nvidia_root / "cudnn" / "bin"]
            for dll_dir in dll_dirs:
                if dll_dir.is_dir():
                    self._dll_handles.append(os.add_dll_directory(str(dll_dir)))
            if hasattr(ort, "preload_dlls"):
                for dll_dir in dll_dirs:
                    if dll_dir.is_dir():
                        ort.preload_dlls(directory=str(dll_dir))
        from rtmlib import Body

        self.model = Body(
            mode=mode, backend="onnxruntime", device=device, to_openpose=False
        )

    @staticmethod
    def _iou(first: np.ndarray, second: np.ndarray) -> float:
        x1, y1 = np.maximum(first[:2], second[:2])
        x2, y2 = np.minimum(first[2:], second[2:])
        intersection = max(0.0, float(x2 - x1)) * max(0.0, float(y2 - y1))
        area1 = max(0.0, float(first[2] - first[0])) * max(0.0, float(first[3] - first[1]))
        area2 = max(0.0, float(second[2] - second[0])) * max(0.0, float(second[3] - second[1]))
        union = area1 + area2 - intersection
        return intersection / union if union else 0.0

    def __call__(self, image: np.ndarray, track_box: np.ndarray) -> np.ndarray:
        keypoints, scores = self.model(image)
        keypoints = np.asarray(keypoints, dtype=np.float32)
        scores = np.asarray(scores, dtype=np.float32)
        if keypoints.size == 0:
            return np.zeros((17, 3), dtype=np.float32)
        if keypoints.ndim == 2:
            keypoints = keypoints[None, ...]
        if scores.ndim == 1:
            scores = scores[None, ...]

        candidates: list[tuple[float, int]] = []
        tx1, ty1, tx2, ty2 = track_box
        for index, (points, confidence) in enumerate(zip(keypoints, scores)):
            valid = confidence >= 0.2
            if not np.any(valid):
                candidates.append((-1.0, index))
                continue
            visible = points[valid]
            pose_box = np.asarray([
                visible[:, 0].min(), visible[:, 1].min(),
                visible[:, 0].max(), visible[:, 1].max(),
            ], dtype=np.float32)
            inside = (
                (visible[:, 0] >= tx1) & (visible[:, 0] <= tx2)
                & (visible[:, 1] >= ty1) & (visible[:, 1] <= ty2)
            )
            match = 2.0 * self._iou(pose_box, track_box) + float(np.mean(inside))
            match += 0.01 * float(np.mean(confidence[valid]))
            candidates.append((match, index))
        selected = max(candidates)[1]
        return np.concatenate(
            [keypoints[selected], scores[selected, :, None]], axis=1
        ).astype(np.float32)


def track_boxes(model: object, path: Path, device: str, confidence: float) -> tuple[
    list[dict[int, tuple[np.ndarray, float]]], np.ndarray
]:
    observations: list[dict[int, tuple[np.ndarray, float]]] = []
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
        if boxes is not None and boxes.id is not None:
            ids = boxes.id.detach().cpu().numpy().astype(np.int64)
            xyxy = boxes.xyxy.detach().cpu().numpy().astype(np.float32)
            for track_id, box in zip(ids, xyxy):
                area = float(max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1]))
                frame_tracks[int(track_id)] = (box, area)
        observations.append(frame_tracks)
    if not observations or image_size is None:
        raise RuntimeError(f"No frames decoded from {path}")
    return observations, np.asarray(image_size, dtype=np.int32)


def choose_primary(
    observations: list[dict[int, tuple[np.ndarray, float]]], start: int, end: int
) -> tuple[int, int, float]:
    counts: defaultdict[int, int] = defaultdict(int)
    areas: defaultdict[int, float] = defaultdict(float)
    for frame in observations[start:end + 1]:
        for identity, (_, area) in frame.items():
            counts[identity] += 1
            areas[identity] += area
    primary = max(counts, key=lambda identity: (counts[identity], areas[identity])) if counts else -1
    coverage = counts.get(primary, 0) / (end - start + 1)
    return primary, len(counts), coverage


def infer_interval(
    matcher: RTMPoseMatcher, video_path: Path,
    observations: list[dict[int, tuple[np.ndarray, float]]],
    primary: int, start: int, end: int, frames: int,
) -> tuple[np.ndarray, np.ndarray]:
    indices = np.rint(np.linspace(start, end, frames)).astype(np.int32)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    inferred: dict[int, np.ndarray] = {}
    zero = np.zeros((17, 3), dtype=np.float32)
    for frame_index in np.unique(indices):
        tracked = observations[int(frame_index)].get(primary)
        if tracked is None:
            inferred[int(frame_index)] = zero
            continue
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
        ok, image = capture.read()
        if not ok or image is None:
            capture.release()
            raise RuntimeError(f"Cannot decode frame {frame_index}: {video_path}")
        inferred[int(frame_index)] = matcher(image, tracked[0])
    capture.release()
    poses = np.stack([inferred[int(index)] for index in indices]).astype(np.float32)
    return poses, indices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument("--tracking-model", type=Path, default=PROJECT / "models/yolo26n-pose.pt")
    parser.add_argument("--frames", type=int, default=64)
    parser.add_argument("--confidence", type=float, default=0.1)
    parser.add_argument("--rtmpose-mode", choices=("lightweight", "balanced", "performance"), default="balanced")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--path-contains")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    os.environ.setdefault("YOLO_CONFIG_DIR", str(PROJECT / ".ultralytics"))
    from ultralytics import YOLO

    rows = read_rows(args.manifest)
    if args.path_contains:
        rows = [row for row in rows if args.path_contains in row["path"]]
    if args.limit is not None:
        rows = rows[:args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    tracker = YOLO(str(args.tracking_model))
    matcher = RTMPoseMatcher(args.rtmpose_mode, args.device)
    output_rows: list[dict[str, str]] = []
    tracked_videos: dict[str, tuple[list[dict[int, tuple[np.ndarray, float]]], np.ndarray]] = {}

    for number, row in enumerate(rows, 1):
        output_path = args.output_dir / f"{cache_stem(row)}.npz"
        if not output_path.exists() or args.overwrite:
            video_path = args.video_root / row["path"]
            if row["path"] not in tracked_videos:
                tracked_videos[row["path"]] = track_boxes(
                    tracker, video_path, args.device, args.confidence
                )
            observations, image_size = tracked_videos[row["path"]]
            start = int(row["start_frame"]) if row.get("start_frame") else 0
            end = int(row["end_frame"]) if row.get("end_frame") else len(observations) - 1
            if start < 0 or end < start or end >= len(observations):
                raise RuntimeError(f"Invalid interval [{start}, {end}] for {row['path']}")
            primary, track_count, coverage = choose_primary(observations, start, end)
            poses, indices = infer_interval(
                matcher, video_path, observations, primary, start, end, args.frames
            )
            np.savez_compressed(
                output_path, keypoints=poses, frame_indices=indices,
                image_size=image_size, source_frames=np.asarray(len(observations)),
                track_count=np.asarray(track_count), primary_track_id=np.asarray(primary),
                primary_track_coverage=np.asarray(coverage),
            )
        with np.load(output_path) as cached:
            poses = cached["keypoints"]
            source_frames = int(cached["source_frames"])
            track_count = int(cached["track_count"])
            primary = int(cached["primary_track_id"])
            coverage = float(cached["primary_track_coverage"])
        confidence_values = poses[:, :, 2]
        output_rows.append({
            **row, "pose_path": output_path.as_posix(),
            "backend": "rtmpose_bytetrack", "frames": str(args.frames),
            "zero_pose_frames": str(int(np.sum(np.max(confidence_values, axis=1) == 0))),
            "mean_confidence": f"{float(np.mean(confidence_values)):.6f}",
            "source_frames": str(source_frames), "track_count": str(track_count),
            "primary_track_id": str(primary),
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
        "mean_confidence": float(np.mean([float(row["mean_confidence"]) for row in output_rows])),
    }
    args.output_manifest.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
