from __future__ import annotations

from dataclasses import dataclass

import numpy as np


EDGES = (
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
)
TORSO_JOINTS = (5, 6, 11, 12)


@dataclass(frozen=True)
class PoseQualityConfig:
    confidence_threshold: float = 0.2
    min_valid_joints: int = 5
    min_torso_joints: int = 2
    max_bone_image_ratio: float = 0.35
    max_center_jump_ratio: float = 0.25
    coordinate_margin_ratio: float = 0.05

    def __post_init__(self) -> None:
        if not 0 <= self.confidence_threshold <= 1:
            raise ValueError("confidence_threshold must be between 0 and 1")
        if not 1 <= self.min_valid_joints <= 17:
            raise ValueError("min_valid_joints must be between 1 and 17")
        if not 0 <= self.min_torso_joints <= len(TORSO_JOINTS):
            raise ValueError("min_torso_joints must be between 0 and 4")
        if self.max_bone_image_ratio <= 0:
            raise ValueError("max_bone_image_ratio must be positive")
        if self.max_center_jump_ratio <= 0:
            raise ValueError("max_center_jump_ratio must be positive")
        if self.coordinate_margin_ratio < 0:
            raise ValueError("coordinate_margin_ratio cannot be negative")


@dataclass(frozen=True)
class FramePoseQuality:
    usable: bool
    valid_joints: int
    torso_joints: int
    max_bone_image_ratio: float
    center_jump_ratio: float | None
    reasons: tuple[str, ...]


def _valid_mask(
    pose: np.ndarray, image_size: np.ndarray, config: PoseQualityConfig,
) -> np.ndarray:
    height, width = np.asarray(image_size, dtype=np.float32)
    margin_x = width * config.coordinate_margin_ratio
    margin_y = height * config.coordinate_margin_ratio
    finite = np.all(np.isfinite(pose), axis=1)
    within = (
        (pose[:, 0] >= -margin_x)
        & (pose[:, 0] <= width + margin_x)
        & (pose[:, 1] >= -margin_y)
        & (pose[:, 1] <= height + margin_y)
    )
    return finite & within & (pose[:, 2] >= config.confidence_threshold)


def pose_center(
    pose: np.ndarray, image_size: np.ndarray, config: PoseQualityConfig,
) -> np.ndarray | None:
    valid = _valid_mask(pose, image_size, config)
    if int(np.sum(valid)) < config.min_valid_joints:
        return None
    torso_valid = valid[np.asarray(TORSO_JOINTS)]
    if np.any(torso_valid):
        torso_indices = np.asarray(TORSO_JOINTS)[torso_valid]
        return np.median(pose[torso_indices, :2], axis=0)
    return np.median(pose[valid, :2], axis=0)


def assess_pose_frame(
    pose: np.ndarray,
    image_size: np.ndarray,
    config: PoseQualityConfig,
    previous_pose: np.ndarray | None = None,
) -> FramePoseQuality:
    pose = np.asarray(pose, dtype=np.float32)
    if pose.shape != (17, 3):
        raise ValueError(f"Expected pose [17,3], got {pose.shape}")
    height, width = np.asarray(image_size, dtype=np.float32)
    image_diagonal = float(np.hypot(width, height))
    if image_diagonal <= 0:
        raise ValueError(f"Invalid image size: {image_size}")

    valid = _valid_mask(pose, image_size, config)
    valid_joints = int(np.sum(valid))
    torso_joints = int(np.sum(valid[np.asarray(TORSO_JOINTS)]))
    reasons: list[str] = []
    if valid_joints < config.min_valid_joints:
        reasons.append("too_few_joints")
    if torso_joints < config.min_torso_joints:
        reasons.append("torso_missing")

    max_bone_ratio = 0.0
    for start, end in EDGES:
        if valid[start] and valid[end]:
            length = float(np.linalg.norm(pose[start, :2] - pose[end, :2]))
            max_bone_ratio = max(max_bone_ratio, length / image_diagonal)
    if max_bone_ratio > config.max_bone_image_ratio:
        reasons.append("implausible_bone")

    jump_ratio: float | None = None
    current_center = pose_center(pose, image_size, config)
    if previous_pose is not None and current_center is not None:
        previous_center = pose_center(previous_pose, image_size, config)
        if previous_center is not None:
            jump_ratio = float(np.linalg.norm(current_center - previous_center) / image_diagonal)
            if jump_ratio > config.max_center_jump_ratio:
                reasons.append("target_jump")

    return FramePoseQuality(
        usable=not reasons,
        valid_joints=valid_joints,
        torso_joints=torso_joints,
        max_bone_image_ratio=max_bone_ratio,
        center_jump_ratio=jump_ratio,
        reasons=tuple(reasons),
    )


def rejected_pose() -> np.ndarray:
    return np.zeros((17, 3), dtype=np.float32)
