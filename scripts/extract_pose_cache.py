from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np


COCO_KEYPOINTS = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sample_video(
    path: Path, frames: int, start_frame: int | None = None, end_frame: int | None = None
) -> tuple[list[np.ndarray], np.ndarray, tuple[int, int]]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        raise RuntimeError(f"Invalid frame count: {path}")
    start = 0 if start_frame is None else start_frame
    end = total - 1 if end_frame is None else end_frame
    if start < 0 or end < start or end >= total:
        raise RuntimeError(f"Invalid frame interval [{start}, {end}] for {path} ({total} frames)")
    indices = np.rint(np.linspace(start, end, frames)).astype(np.int32)
    decoded: list[np.ndarray] = []
    decoded_by_index: dict[int, np.ndarray] = {}
    for index in indices:
        key = int(index)
        if key not in decoded_by_index:
            capture.set(cv2.CAP_PROP_POS_FRAMES, key)
            ok, image = capture.read()
            if not ok or image is None:
                capture.release()
                raise RuntimeError(f"Cannot decode frame {index}: {path}")
            decoded_by_index[key] = image
        decoded.append(decoded_by_index[key])
    capture.release()
    height, width = decoded[0].shape[:2]
    return decoded, indices, (height, width)


class YoloPoseBackend:
    def __init__(self, model_path: str, device: str, confidence: float) -> None:
        import os

        # Keep Ultralytics settings inside the project so sandboxed and shared
        # runs do not depend on a user's roaming AppData permissions.
        config_dir = Path(__file__).resolve().parent.parent / ".ultralytics"
        config_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("YOLO_CONFIG_DIR", str(config_dir))
        from ultralytics import YOLO

        self.model = YOLO(model_path)
        self.device = device
        self.confidence = confidence

    def __call__(self, image: np.ndarray) -> np.ndarray:
        result = self.model.predict(
            image, device=self.device, conf=self.confidence, verbose=False
        )[0]
        if result.keypoints is None or result.boxes is None or len(result.boxes) == 0:
            return np.zeros((17, 3), dtype=np.float32)
        boxes = result.boxes.xyxy.detach().cpu().numpy()
        areas = np.maximum(0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0, boxes[:, 3] - boxes[:, 1])
        selected = int(np.argmax(areas))
        points = result.keypoints.data[selected].detach().cpu().numpy().astype(np.float32)
        if points.shape != (17, 3):
            raise RuntimeError(f"Expected YOLO COCO-17 keypoints, got {points.shape}")
        return points


class RTMPoseBackend:
    def __init__(self, mode: str, device: str, one_stage: bool = False) -> None:
        self._dll_handles = []
        if device.lower().startswith("cuda"):
            import os
            import onnxruntime as ort

            # Windows CUDA wheels use a shared ``nvidia/cu13`` directory rather
            # than the Linux-oriented ``*-cu13`` distribution names that ORT's
            # automatic discovery expects. Load both wheel directories explicitly.
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
            pose="rtmo" if one_stage else None,
            mode=mode,
            backend="onnxruntime",
            device=device,
            to_openpose=False,
        )
        sessions = []
        for component in vars(self.model).values():
            session = getattr(component, "session", None)
            if hasattr(session, "get_providers"):
                sessions.append(session)
        providers = [session.get_providers() for session in sessions]
        if providers:
            name = "RTMO" if one_stage else "RTMPose"
            print(f"{name} execution providers: {providers}", flush=True)

    def __call__(self, image: np.ndarray) -> np.ndarray:
        keypoints, scores = self.model(image)
        keypoints = np.asarray(keypoints, dtype=np.float32)
        scores = np.asarray(scores, dtype=np.float32)
        if keypoints.size == 0:
            return np.zeros((17, 3), dtype=np.float32)
        if keypoints.ndim == 2:
            keypoints = keypoints[None, ...]
        if scores.ndim == 1:
            scores = scores[None, ...]
        if keypoints.shape[1] != 17:
            raise RuntimeError(f"Expected RTMPose COCO-17 keypoints, got {keypoints.shape}")
        quality = []
        for person_points, person_scores in zip(keypoints, scores):
            valid = person_scores >= 0.2
            if not np.any(valid):
                quality.append(0.0)
                continue
            extent = np.ptp(person_points[valid], axis=0)
            quality.append(float(extent[0] * extent[1] * np.mean(person_scores[valid])))
        selected = int(np.argmax(quality))
        return np.concatenate([keypoints[selected], scores[selected, :, None]], axis=1).astype(np.float32)


def safe_stem(relative_path: str) -> str:
    path = Path(relative_path)
    return "__".join(path.with_suffix("").parts).replace(" ", "_")


def cache_stem(row: dict[str, str]) -> str:
    stem = safe_stem(row["path"])
    if row.get("start_frame") and row.get("end_frame"):
        stem += f"__f{row['start_frame']}_{row['end_frame']}"
    return stem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument("--backend", choices=("yolo", "rtmpose", "rtmo"), required=True)
    parser.add_argument("--frames", type=int, default=64)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--yolo-model", default="yolo26n-pose.pt")
    parser.add_argument("--yolo-conf", type=float, default=0.1)
    parser.add_argument("--rtmpose-mode", choices=("lightweight", "balanced", "performance"), default="balanced")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--path-contains")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = read_manifest(args.manifest)
    if args.path_contains:
        rows = [row for row in rows if args.path_contains in row["path"]]
    if args.limit is not None:
        rows = rows[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    if args.backend == "yolo":
        backend = YoloPoseBackend(args.yolo_model, args.device, args.yolo_conf)
    else:
        backend = RTMPoseBackend(
            args.rtmpose_mode, args.device, one_stage=args.backend == "rtmo"
        )

    output_rows = []
    for item_number, row in enumerate(rows, start=1):
        video_path = args.video_root / row["path"]
        output_path = args.output_dir / f"{cache_stem(row)}.npz"
        if not output_path.exists() or args.overwrite:
            start_frame = int(row["start_frame"]) if row.get("start_frame") else None
            end_frame = int(row["end_frame"]) if row.get("end_frame") else None
            images, indices, image_size = sample_video(
                video_path, args.frames, start_frame=start_frame, end_frame=end_frame
            )
            # Short annotated intervals can contain fewer unique frames than the
            # fixed output length. Infer each source frame once, then repeat its
            # cached pose at the requested temporal positions.
            inferred: dict[int, np.ndarray] = {}
            pose_sequence = []
            for frame_index, image in zip(indices, images):
                key = int(frame_index)
                if key not in inferred:
                    inferred[key] = backend(image)
                pose_sequence.append(inferred[key])
            poses = np.stack(pose_sequence).astype(np.float32)
            np.savez_compressed(
                output_path,
                keypoints=poses,
                frame_indices=indices,
                image_size=np.asarray(image_size, dtype=np.int32),
                keypoint_names=np.asarray(COCO_KEYPOINTS),
            )
        with np.load(output_path) as cached:
            poses = cached["keypoints"]
        confidence = poses[:, :, 2]
        output_rows.append(
            {
                **row,
                "pose_path": output_path.as_posix(),
                "backend": args.backend,
                "frames": str(args.frames),
                "zero_pose_frames": str(int(np.sum(np.max(confidence, axis=1) == 0))),
                "mean_confidence": f"{float(np.mean(confidence)):.6f}",
            }
        )
        print(f"[{item_number}/{len(rows)}] {row['path']}", flush=True)

    fields = list(output_rows[0]) if output_rows else []
    with args.output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    summary = {
        "backend": args.backend,
        "videos": len(output_rows),
        "frames_per_video": args.frames,
        "zero_pose_frames": sum(int(row["zero_pose_frames"]) for row in output_rows),
        "mean_confidence": float(np.mean([float(row["mean_confidence"]) for row in output_rows])),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
