from __future__ import annotations

import time
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from scripts.build_gcn_tensor import sequence_normalize

from .decision import DecisionConfig, DecisionEngine
from .pipeline import (
    PROJECT,
    ROUTES,
    FoldEnsemble,
    create_pose_backend,
    draw_overlay,
)
from .pose_quality import PoseQualityConfig, assess_pose_frame
from .prefall import PreFallEnsemble


def prefall_pose_gate(pose_valid_ratio: float, minimum: float) -> bool:
    """Reject pre-fall inference when the history lacks reliable skeletons."""
    return pose_valid_ratio >= minimum


@dataclass(frozen=True)
class RealtimeDetectorConfig:
    route: str = "yolo_stgcnpp"
    checkpoints_root: Path = PROJECT / "results/benchmark_e300_full"
    yolo_model: Path = PROJECT / "yolo26n-pose.pt"
    device: str = "cuda"
    window_frames: int = 64
    stride_frames: int = 16
    pose_threshold: float = 0.2
    yolo_confidence: float = 0.1
    threshold: float = 0.5
    confirm_windows: int = 3
    cooldown_windows: int = 10
    min_pose_valid_ratio: float = 0.5
    min_positive_folds: int = 3
    prefall_enabled: bool = False
    prefall_checkpoints_root: Path = PROJECT / "outputs/prevfall_rtmpose_stgcnpp_300e_b128"
    prefall_min_positive_folds: int = 5


class RealtimeFallDetector:
    """Stateful, single-camera real-time skeleton fall detector."""

    def __init__(self, config: RealtimeDetectorConfig | None = None) -> None:
        self.config = config or RealtimeDetectorConfig()
        if self.config.route not in ROUTES:
            raise ValueError(f"Unknown route: {self.config.route}")
        self.device = torch.device(
            self.config.device if torch.cuda.is_available() else "cpu"
        )
        pose_name, _ = ROUTES[self.config.route]
        if self.config.prefall_enabled and pose_name != "rtmpose":
            raise ValueError(
                "Current pre-fall weights were trained on RTMPose; set "
                "FALL_ROUTE=rtmpose_stgcnpp or disable PREFALL_ENABLED"
            )
        self.pose_backend = create_pose_backend(
            pose_name,
            str(self.device),
            self.config.yolo_model,
            self.config.yolo_confidence,
        )
        self.classifier = FoldEnsemble(
            self.config.route, self.config.checkpoints_root, self.device
        )
        self.prefall = (
            PreFallEnsemble(
                self.config.prefall_checkpoints_root,
                self.device,
                self.config.prefall_min_positive_folds,
            )
            if self.config.prefall_enabled else None
        )
        self.decision = DecisionEngine(
            DecisionConfig(
                threshold=self.config.threshold,
                confirm_windows=self.config.confirm_windows,
                cooldown_windows=self.config.cooldown_windows,
                min_pose_valid_ratio=self.config.min_pose_valid_ratio,
                min_positive_folds=self.config.min_positive_folds,
            )
        )
        self.quality = PoseQualityConfig(
            confidence_threshold=self.config.pose_threshold
        )
        self.poses: deque[np.ndarray] = deque(maxlen=self.config.window_frames)
        self.usable: deque[bool] = deque(maxlen=self.config.window_frames)
        self.previous_pose: np.ndarray | None = None
        self.frame_index = 0
        self.window_index = 0
        self.last_probability: float | None = None
        self.last_state = "WARMUP"
        self.last_positive_folds: int | None = None
        self.last_pose_valid_ratio: float | None = None
        self.last_prefall: dict[str, object] = {
            "enabled": bool(self.prefall), "risk_level": "WARMUP"
        }

    def process(
        self, frame: np.ndarray, timestamp_ms: int | None = None
    ) -> tuple[np.ndarray, dict[str, object], dict[str, object] | None]:
        started = time.perf_counter()
        height, width = frame.shape[:2]
        pose = np.asarray(self.pose_backend(frame), dtype=np.float32)
        if pose.shape != (17, 3):
            raise RuntimeError(f"Unexpected pose shape: {pose.shape}")
        quality = assess_pose_frame(
            pose,
            np.asarray([height, width]),
            self.quality,
            previous_pose=self.previous_pose,
        )
        if quality.usable:
            self.previous_pose = pose.copy()
        self.poses.append(pose)
        self.usable.append(quality.usable)
        event = None
        evaluated = False
        if (
            len(self.poses) == self.config.window_frames
            and (self.frame_index - self.config.window_frames + 1)
            % self.config.stride_frames
            == 0
        ):
            evaluated = True
            sample = sequence_normalize(
                np.stack(self.poses),
                np.asarray([height, width]),
                self.config.pose_threshold,
            )
            probability, folds = self.classifier.predict(sample)
            pose_valid_ratio = float(np.mean(self.usable))
            if self.prefall is not None:
                if prefall_pose_gate(pose_valid_ratio, self.config.min_pose_valid_ratio):
                    self.last_prefall = {
                        **self.prefall.predict(sample),
                        "prediction_active": True,
                        "pose_valid_ratio": pose_valid_ratio,
                    }
                else:
                    self.last_prefall = {
                        "enabled": True,
                        "risk_level": "POSE_UNAVAILABLE",
                        "prediction_active": False,
                        "reason": "insufficient_pose_quality",
                        "pose_valid_ratio": pose_valid_ratio,
                        "minimum_pose_valid_ratio": self.config.min_pose_valid_ratio,
                    }
            positive_folds = sum(
                value >= self.config.threshold for value in folds
            )
            now_ms = timestamp_ms if timestamp_ms is not None else int(time.time() * 1000)
            state, raw_event = self.decision.update(
                probability, pose_valid_ratio, now_ms, positive_folds
            )
            self.last_probability = probability
            self.last_state = state
            self.last_positive_folds = positive_folds
            self.last_pose_valid_ratio = pose_valid_ratio
            if state == "CONFIRMED":
                self.last_prefall = {
                    **self.last_prefall, "risk_level": "FALL_CONFIRMED",
                    "prediction_active": False,
                }
            elif state == "COOLDOWN":
                self.last_prefall = {
                    **self.last_prefall, "risk_level": "RESPONSE_ACTIVE",
                    "prediction_active": False,
                }
            if raw_event is not None:
                event = {
                    **raw_event,
                    "window_index": self.window_index,
                    "route": self.config.route,
                }
            self.window_index += 1
        reason = "ok" if quality.usable else ",".join(quality.reasons)
        overlay = draw_overlay(
            frame,
            pose,
            self.frame_index,
            self.last_probability,
            self.last_state,
            self.config.pose_threshold,
            self.config.route,
            self.last_pose_valid_ratio,
            self.last_positive_folds,
            "primary" if quality.usable else "rejected",
            reason,
            self.last_prefall,
        )
        result: dict[str, object] = {
            "frame_index": self.frame_index,
            "window_index": self.window_index,
            "evaluated": evaluated,
            "state": self.last_state,
            "fall_probability": self.last_probability,
            "positive_folds": self.last_positive_folds,
            "pose_valid_ratio": self.last_pose_valid_ratio,
            "pose_quality": reason,
            "latency_ms": (time.perf_counter() - started) * 1000,
            "prefall_prediction": self.last_prefall,
        }
        self.frame_index += 1
        return overlay, result, event
