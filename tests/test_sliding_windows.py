from __future__ import annotations

import unittest

from scripts.build_sliding_window_dataset import parse_fall_interval, window_label


class SlidingWindowLabelTest(unittest.TestCase):
    def test_parses_normal_and_malformed_source_annotations(self) -> None:
        self.assertEqual(
            parse_fall_interval("Falling (SW)[3.4 to 6]; Sitting[0 to 3.4]"),
            (3.4, 6.0),
        )
        self.assertEqual(
            parse_fall_interval("Falling (BW)[2.3 6]; Sitting[0 to 2]"),
            (2.3, 6.0),
        )
        self.assertEqual(parse_fall_interval("Fall (FW)[0 to 3]"), (0.0, 3.0))

    def test_adl_window_is_negative(self) -> None:
        self.assertEqual(window_label(0, 63, None, 15), 0)

    def test_pre_fall_positive_and_boundary_labels(self) -> None:
        self.assertEqual(window_label(0, 63, 80, 15), 0)
        self.assertIsNone(window_label(32, 95, 90, 15))
        self.assertEqual(window_label(48, 111, 90, 15), 1)


if __name__ == "__main__":
    unittest.main()
