from __future__ import annotations

import unittest

from app.decision import DecisionConfig, DecisionEngine


class DecisionEngineTest(unittest.TestCase):
    def test_confirmation_and_cooldown(self) -> None:
        engine = DecisionEngine(
            DecisionConfig(threshold=0.5, confirm_windows=2, cooldown_windows=2)
        )
        self.assertEqual(engine.update(0.8, 1.0, 100)[0], "SUSPECTED")
        state, event = engine.update(0.9, 1.0, 200)
        self.assertEqual(state, "CONFIRMED")
        self.assertIsNotNone(event)
        self.assertEqual(engine.update(0.9, 1.0, 300)[0], "COOLDOWN")
        self.assertEqual(engine.update(0.9, 1.0, 400)[0], "COOLDOWN")
        self.assertEqual(engine.update(0.1, 1.0, 500)[0], "NORMAL")

    def test_low_pose_quality_is_unknown(self) -> None:
        engine = DecisionEngine(DecisionConfig(min_pose_valid_ratio=0.5))
        state, event = engine.update(0.99, 0.49, 100)
        self.assertEqual(state, "UNKNOWN")
        self.assertIsNone(event)

    def test_fold_agreement_blocks_weak_ensemble(self) -> None:
        engine = DecisionEngine(
            DecisionConfig(threshold=0.5, confirm_windows=1, min_positive_folds=3)
        )
        state, event = engine.update(0.8, 1.0, 100, positive_folds=2)
        self.assertEqual(state, "NORMAL")
        self.assertIsNone(event)
        state, event = engine.update(0.8, 1.0, 200, positive_folds=3)
        self.assertEqual(state, "CONFIRMED")
        self.assertIsNotNone(event)


if __name__ == "__main__":
    unittest.main()
