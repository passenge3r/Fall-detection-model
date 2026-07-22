from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionConfig:
    threshold: float = 0.5
    confirm_windows: int = 3
    cooldown_windows: int = 10
    min_pose_valid_ratio: float = 0.5
    min_positive_folds: int = 3

    def __post_init__(self) -> None:
        if not 0 <= self.threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        if self.confirm_windows < 1:
            raise ValueError("confirm_windows must be positive")
        if self.cooldown_windows < 0:
            raise ValueError("cooldown_windows cannot be negative")
        if not 0 <= self.min_pose_valid_ratio <= 1:
            raise ValueError("min_pose_valid_ratio must be between 0 and 1")
        if not 1 <= self.min_positive_folds <= 4:
            raise ValueError("min_positive_folds must be between 1 and 4")


class DecisionEngine:
    """Convert independent window probabilities into a small alarm state machine."""

    def __init__(self, config: DecisionConfig) -> None:
        self.config = config
        self.state = "NORMAL"
        self.consecutive_positive = 0
        self.cooldown_remaining = 0
        self.event_index = 0

    def update(
        self, probability: float, pose_valid_ratio: float, timestamp_ms: int,
        positive_folds: int = 4,
    ) -> tuple[str, dict[str, object] | None]:
        event = None
        if pose_valid_ratio < self.config.min_pose_valid_ratio:
            self.state = "UNKNOWN"
            self.consecutive_positive = 0
            return self.state, event

        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
            self.state = "COOLDOWN"
            return self.state, event

        ensemble_positive = (
            probability >= self.config.threshold
            and positive_folds >= self.config.min_positive_folds
        )
        if ensemble_positive:
            self.consecutive_positive += 1
            self.state = "SUSPECTED"
            if self.consecutive_positive >= self.config.confirm_windows:
                self.event_index += 1
                self.state = "CONFIRMED"
                self.consecutive_positive = 0
                self.cooldown_remaining = self.config.cooldown_windows
                event = {
                    "event_index": self.event_index,
                    "confirmed_at_ms": timestamp_ms,
                    "fall_probability": probability,
                    "pose_valid_ratio": pose_valid_ratio,
                    "positive_folds": positive_folds,
                    "status": self.state,
                }
        else:
            self.consecutive_positive = 0
            self.state = "NORMAL"
        return self.state, event
