import sys
from pathlib import Path

import torch


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))

from calibrate_prefall_operating_point import choose_operating_point  # noqa: E402
from train_prefall_ordinal_stgcnpp import (  # noqa: E402
    labels_to_stage,
    stage_probabilities_to_horizons,
)


def test_nested_labels_map_to_ordered_stages() -> None:
    labels = torch.tensor(
        [[0, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1]], dtype=torch.float32
    )
    assert labels_to_stage(labels).tolist() == [0, 1, 2, 3]


def test_stage_probabilities_produce_nested_horizon_risk() -> None:
    probabilities = torch.tensor([[0.4, 0.3, 0.2, 0.1]])
    risks = stage_probabilities_to_horizons(probabilities)
    assert torch.allclose(risks, torch.tensor([[0.1, 0.3, 0.6]]))


def test_operating_point_respects_budget_before_maximizing_recall() -> None:
    points = [
        {"event_recall": 0.9, "mean_lead_seconds": 1.0,
         "adl_false_alarm_episodes_per_hour": 20.0, "threshold": 0.2},
        {"event_recall": 0.6, "mean_lead_seconds": 1.2,
         "adl_false_alarm_episodes_per_hour": 8.0, "threshold": 0.5},
        {"event_recall": 0.4, "mean_lead_seconds": 1.4,
         "adl_false_alarm_episodes_per_hour": 2.0, "threshold": 0.8},
    ]
    selected = choose_operating_point(points, budget=10.0)
    assert selected["threshold"] == 0.5

