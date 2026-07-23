from __future__ import annotations

import json
import sys
import time
from collections import Counter, deque
from pathlib import Path
from typing import TextIO

import cv2
import numpy as np
import torch


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402
from scripts.build_gcn_tensor import sequence_normalize  # noqa: E402
from scripts.extract_pose_cache import RTMPoseBackend, YoloPoseBackend  # noqa: E402

from .decision import DecisionConfig, DecisionEngine


EDGES = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
]
ROUTES = {
    "rtmpose_stgcnpp": ("rtmpose", "stgcnpp"),
    "rtmpose_ctrgcn": ("rtmpose", "ctrgcn"),
    "yolo_stgcnpp": ("yolo", "stgcnpp"),
    "yolo_ctrgcn": ("yolo", "ctrgcn"),
}


def write_jsonl(handle: TextIO, record: dict[str, object]) -> None:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    handle.flush()


class FoldEnsemble:
    def __init__(self, route: str, checkpoints_root: Path, device: torch.device) -> None:
        if route not in ROUTES:
            raise ValueError(f"Unknown route: {route}")
        _, model_name = ROUTES[route]
        self.route = route
        self.device = device
        self.models = []
        for fold in range(1, 5):
            checkpoint = checkpoints_root / route / f"fold_{fold}" / "best.pt"
            if not checkpoint.is_file():
                raise FileNotFoundError(f"Missing checkpoint: {checkpoint}")
            model = build_model(
                model_name, num_class=2, base_channels=64, dropout=0.5
            ).to(device)
            state = torch.load(checkpoint, map_location=device, weights_only=True)
            model.load_state_dict(state)
            model.eval()
            self.models.append(model)

    @torch.inference_mode()
    def predict(self, sample: np.ndarray) -> tuple[float, list[float]]:
        tensor = torch.from_numpy(sample[None]).to(self.device, non_blocking=True)
        probabilities = [
            float(torch.softmax(model(tensor), dim=1)[0, 1].item()) for model in self.models
        ]
        return float(np.mean(probabilities)), probabilities


def create_pose_backend(
    backend: str, device: str, yolo_model: Path, yolo_confidence: float,
) -> object:
    if backend == "yolo":
        if not yolo_model.is_file():
            raise FileNotFoundError(f"Missing YOLO pose model: {yolo_model}")
        return YoloPoseBackend(str(yolo_model), device, yolo_confidence)
    if backend == "rtmpose":
        return RTMPoseBackend("balanced", device)
    raise ValueError(f"Unknown pose backend: {backend}")


def draw_overlay(
    frame: np.ndarray, pose: np.ndarray, frame_index: int,
    probability: float | None, state: str, pose_threshold: float,
    route: str, pose_valid_ratio: float | None, positive_folds: int | None,
) -> np.ndarray:
    canvas = frame.copy()
    valid = pose[:, 2] >= pose_threshold
    for start, end in EDGES:
        if valid[start] and valid[end]:
            p1 = tuple(np.rint(pose[start, :2]).astype(int))
            p2 = tuple(np.rint(pose[end, :2]).astype(int))
            cv2.line(canvas, p1, p2, (60, 220, 70), 2, cv2.LINE_AA)
    for point in pose[valid]:
        cv2.circle(canvas, tuple(np.rint(point[:2]).astype(int)), 4, (40, 70, 255), -1)

    colors = {
        "NORMAL": (60, 210, 70), "SUSPECTED": (30, 190, 255),
        "CONFIRMED": (30, 30, 255), "COOLDOWN": (190, 100, 30),
        "UNKNOWN": (150, 150, 150), "WARMUP": (220, 220, 220),
    }
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 82), (0, 0, 0), -1)
    probability_text = "--" if probability is None else f"{probability:.3f}"
    cv2.putText(
        canvas, f"frame={frame_index}  fall_probability={probability_text}",
        (12, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA,
    )
    cv2.putText(
        canvas, f"state={state}", (12, 49), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, colors.get(state, (255, 255, 255)), 2, cv2.LINE_AA,
    )
    quality_text = "--" if pose_valid_ratio is None else f"{pose_valid_ratio:.2f}"
    agreement_text = "--/4" if positive_folds is None else f"{positive_folds}/4"
    cv2.putText(
        canvas,
        f"route={route}  pose_valid={quality_text}  positive_folds={agreement_text}",
        (12, 73),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (220, 220, 220),
        1,
        cv2.LINE_AA,
    )
    return canvas


def run_video(
    input_path: Path,
    output_dir: Path,
    route: str = "rtmpose_stgcnpp",
    checkpoints_root: Path = PROJECT / "results/benchmark_e300_full",
    yolo_model: Path = PROJECT / "models/yolo26n-pose.pt",
    device_name: str = "cuda",
    window_frames: int = 64,
    stride_frames: int = 16,
    pose_threshold: float = 0.2,
    yolo_confidence: float = 0.1,
    decision_config: DecisionConfig | None = None,
    write_video: bool = True,
    max_frames: int | None = None,
) -> dict[str, object]:
    if route not in ROUTES:
        raise ValueError(f"route must be one of {sorted(ROUTES)}")
    if window_frames < 2 or stride_frames < 1:
        raise ValueError("window_frames must be >=2 and stride_frames must be >=1")
    if not input_path.is_file():
        raise FileNotFoundError(f"Input video not found: {input_path}")
    config = decision_config or DecisionConfig()
    device = torch.device(device_name if torch.cuda.is_available() else "cpu")
    pose_name, _ = ROUTES[route]

    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {input_path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if fps <= 0 or width <= 0 or height <= 0:
        capture.release()
        raise RuntimeError(f"Invalid video metadata: fps={fps}, size={width}x{height}")

    output_dir.mkdir(parents=True, exist_ok=True)
    pose_backend = create_pose_backend(pose_name, str(device), yolo_model, yolo_confidence)
    classifier = FoldEnsemble(route, checkpoints_root, device)
    decision = DecisionEngine(config)
    pose_buffer: deque[np.ndarray] = deque(maxlen=window_frames)
    writer = None
    if write_video:
        writer = cv2.VideoWriter(
            str(output_dir / "annotated.mp4"), cv2.VideoWriter_fourcc(*"mp4v"),
            fps, (width, height),
        )
        if not writer.isOpened():
            capture.release()
            raise RuntimeError(f"Cannot create {output_dir / 'annotated.mp4'}")

    start_time = time.perf_counter()
    frame_index = 0
    window_index = 0
    latest_probability: float | None = None
    latest_state = "WARMUP"
    latest_pose_valid_ratio: float | None = None
    latest_positive_folds: int | None = None
    state_counts: Counter[str] = Counter()
    event_count = 0
    zero_pose_frames = 0
    with (
        (output_dir / "windows.jsonl").open("w", encoding="utf-8") as windows_handle,
        (output_dir / "events.jsonl").open("w", encoding="utf-8") as events_handle,
    ):
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            pose = np.asarray(pose_backend(frame), dtype=np.float32)
            if pose.shape != (17, 3):
                raise RuntimeError(f"Unexpected pose shape at frame {frame_index}: {pose.shape}")
            if not np.any(pose[:, 2] >= pose_threshold):
                zero_pose_frames += 1
            pose_buffer.append(pose)

            window_ready = len(pose_buffer) == window_frames
            if window_ready and (frame_index - window_frames + 1) % stride_frames == 0:
                raw_poses = np.stack(pose_buffer)
                pose_valid_ratio = float(
                    np.mean(np.max(raw_poses[:, :, 2], axis=1) >= pose_threshold)
                )
                sample = sequence_normalize(
                    raw_poses, np.asarray([height, width]), pose_threshold
                )
                latest_probability, fold_probabilities = classifier.predict(sample)
                positive_folds = sum(
                    probability >= config.threshold for probability in fold_probabilities
                )
                latest_pose_valid_ratio = pose_valid_ratio
                latest_positive_folds = positive_folds
                timestamp_ms = int(round(frame_index / fps * 1000))
                latest_state, event = decision.update(
                    latest_probability, pose_valid_ratio, timestamp_ms, positive_folds
                )
                record: dict[str, object] = {
                    "window_index": window_index,
                    "start_frame": frame_index - window_frames + 1,
                    "end_frame": frame_index,
                    "start_ms": int(round((frame_index - window_frames + 1) / fps * 1000)),
                    "end_ms": timestamp_ms,
                    "route": route,
                    "fall_probability": latest_probability,
                    "fold_probabilities": fold_probabilities,
                    "positive_folds": positive_folds,
                    "pose_valid_ratio": pose_valid_ratio,
                    "state": latest_state,
                }
                write_jsonl(windows_handle, record)
                state_counts[latest_state] += 1
                if event is not None:
                    event_count += 1
                    write_jsonl(
                        events_handle,
                        {
                            "event_id": f"fall-{event_count:06d}",
                            "source": str(input_path.resolve()),
                            "route": route,
                            "window_index": window_index,
                            **event,
                        },
                    )
                window_index += 1

            if writer is not None:
                writer.write(
                    draw_overlay(
                        frame, pose, frame_index, latest_probability,
                        latest_state, pose_threshold, route,
                        latest_pose_valid_ratio, latest_positive_folds,
                    )
                )
            frame_index += 1
            if max_frames is not None and frame_index >= max_frames:
                break

    capture.release()
    if writer is not None:
        writer.release()
    elapsed = time.perf_counter() - start_time
    summary: dict[str, object] = {
        "input": str(input_path.resolve()),
        "output_dir": str(output_dir.resolve()),
        "route": route,
        "pose_backend": pose_name,
        "classifier": ROUTES[route][1],
        "ensemble_folds": 4,
        "device": str(device),
        "source_fps": fps,
        "source_size": [width, height],
        "frames_processed": frame_index,
        "windows_processed": window_index,
        "window_frames": window_frames,
        "stride_frames": stride_frames,
        "zero_pose_frames": zero_pose_frames,
        "zero_pose_rate": zero_pose_frames / frame_index if frame_index else 0.0,
        "state_counts": dict(state_counts),
        "confirmed_events": event_count,
        "elapsed_seconds": elapsed,
        "processing_fps": frame_index / elapsed if elapsed else 0.0,
        "decision": {
            "threshold": config.threshold,
            "confirm_windows": config.confirm_windows,
            "cooldown_windows": config.cooldown_windows,
            "min_pose_valid_ratio": config.min_pose_valid_ratio,
            "min_positive_folds": config.min_positive_folds,
        },
        "warning": "Research prototype; window distribution differs from uniform-sampling training clips.",
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary
