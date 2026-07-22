"""Pre-recorded video fall-detection prototype."""

from .decision import DecisionConfig, DecisionEngine
from .pipeline import run_video

__all__ = ["DecisionConfig", "DecisionEngine", "run_video"]
