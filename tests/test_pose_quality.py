from __future__ import annotations

import unittest

import numpy as np

from app.pose_quality import PoseQualityConfig, assess_pose_frame


IMAGE_SIZE = np.asarray([720, 1280], dtype=np.float32)


def plausible_pose(offset_x: float = 0.0, offset_y: float = 0.0) -> np.ndarray:
    points = np.asarray(
        [
            [640, 160], [625, 150], [655, 150], [610, 160], [670, 160],
            [590, 250], [690, 250], [550, 350], [730, 350], [520, 440], [760, 440],
            [610, 430], [670, 430], [600, 560], [680, 560], [590, 690], [690, 690],
        ],
        dtype=np.float32,
    )
    pose = np.zeros((17, 3), dtype=np.float32)
    pose[:, :2] = points + np.asarray([offset_x, offset_y], dtype=np.float32)
    pose[:, 2] = 0.9
    return pose


class PoseQualityTest(unittest.TestCase):
    def test_plausible_pose_is_usable(self) -> None:
        quality = assess_pose_frame(
            plausible_pose(), IMAGE_SIZE, PoseQualityConfig()
        )
        self.assertTrue(quality.usable)
        self.assertEqual(quality.reasons, ())

    def test_missing_torso_is_rejected(self) -> None:
        pose = plausible_pose()
        pose[:, 2] = 0.0
        pose[[0, 1, 2, 3, 4], 2] = 0.9
        quality = assess_pose_frame(pose, IMAGE_SIZE, PoseQualityConfig())
        self.assertFalse(quality.usable)
        self.assertIn("torso_missing", quality.reasons)

    def test_implausibly_long_bone_is_rejected(self) -> None:
        pose = plausible_pose()
        pose[6, :2] = [1200, 250]
        quality = assess_pose_frame(
            pose, IMAGE_SIZE, PoseQualityConfig(max_bone_image_ratio=0.25)
        )
        self.assertFalse(quality.usable)
        self.assertIn("implausible_bone", quality.reasons)

    def test_large_target_jump_is_rejected(self) -> None:
        previous = plausible_pose(offset_x=-350)
        current = plausible_pose(offset_x=350)
        quality = assess_pose_frame(
            current,
            IMAGE_SIZE,
            PoseQualityConfig(max_center_jump_ratio=0.2),
            previous_pose=previous,
        )
        self.assertFalse(quality.usable)
        self.assertIn("target_jump", quality.reasons)


if __name__ == "__main__":
    unittest.main()
