from __future__ import annotations

import unittest

import numpy as np

from scripts.repair_rtmpose_bytetrack_cache import repair_sequence


def pose(value: float, confidence: float = 0.9) -> np.ndarray:
    result = np.zeros((17, 3), dtype=np.float32)
    result[:, :2] = value
    result[:, 2] = confidence
    return result


class PoseRepairTest(unittest.TestCase):
    def test_same_frame_fallback_has_priority_over_interpolation(self) -> None:
        tracked = np.stack([pose(0), pose(0, 0), pose(2)])
        fallback = np.stack([pose(10), pose(1), pose(12)])
        repaired, sources = repair_sequence(
            tracked,
            fallback,
            np.asarray([0, 2, 4]),
        )
        np.testing.assert_allclose(repaired[1], fallback[1])
        np.testing.assert_array_equal(sources, np.asarray([0, 1, 0]))

    def test_short_bounded_gap_is_interpolated_when_both_backends_miss(self) -> None:
        tracked = np.stack([pose(0), pose(0, 0), pose(2)])
        fallback = np.stack([pose(10), pose(0, 0), pose(12)])
        repaired, sources = repair_sequence(
            tracked,
            fallback,
            np.asarray([0, 2, 4]),
            max_source_gap=4,
        )
        np.testing.assert_allclose(repaired[1, :, :2], 1.0)
        self.assertEqual(int(sources[1]), 2)

    def test_long_gap_remains_missing(self) -> None:
        tracked = np.stack([pose(0), pose(0, 0), pose(2)])
        fallback = np.stack([pose(10), pose(0, 0), pose(12)])
        repaired, sources = repair_sequence(
            tracked,
            fallback,
            np.asarray([0, 10, 20]),
            max_source_gap=12,
        )
        self.assertEqual(int(sources[1]), 3)
        self.assertFalse(np.any(repaired[1, :, 2] >= 0.2))


if __name__ == "__main__":
    unittest.main()
