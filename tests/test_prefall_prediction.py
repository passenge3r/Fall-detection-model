import json

import torch

import app.prefall as prefall_module
from app.prefall import PreFallEnsemble, risk_level
from app.realtime import prefall_pose_gate
from scripts.build_prefall_prediction_dataset import prediction_labels, risk_stage


def test_adl_windows_are_negative_for_all_horizons() -> None:
    labels, lead = prediction_labels(end_frame=100, fall_onset_frame=None, fps=30.0)
    assert labels == (0, 0, 0)
    assert lead is None


def test_windows_at_or_after_onset_are_excluded() -> None:
    assert prediction_labels(end_frame=100, fall_onset_frame=100, fps=30.0) is None
    assert prediction_labels(end_frame=101, fall_onset_frame=100, fps=30.0) is None


def test_prediction_horizons_are_nested_and_include_boundaries() -> None:
    assert prediction_labels(70, 100, 30.0)[0] == (1, 1, 1)
    assert prediction_labels(69, 100, 30.0)[0] == (0, 1, 1)
    assert prediction_labels(40, 100, 30.0)[0] == (0, 1, 1)
    assert prediction_labels(39, 100, 30.0)[0] == (0, 0, 1)
    assert prediction_labels(10, 100, 30.0)[0] == (0, 0, 1)
    assert prediction_labels(9, 100, 30.0)[0] == (0, 0, 0)


def test_risk_stage_is_mutually_exclusive() -> None:
    assert risk_stage((1, 1, 1), True) == "PRE_FALL_0_1S"
    assert risk_stage((0, 1, 1), True) == "PRE_FALL_1_2S"
    assert risk_stage((0, 0, 1), True) == "PRE_FALL_2_3S"
    assert risk_stage((0, 0, 0), True) == "EARLY_FALL_VIDEO"
    assert risk_stage((0, 0, 0), False) == "ADL"


def test_risk_level_uses_configured_vote_count() -> None:
    assert risk_level([5, 5, 5], 5) == "HIGH"
    assert risk_level([4, 5, 5], 5) == "MEDIUM"
    assert risk_level([4, 4, 5], 5) == "LOW"
    assert risk_level([4, 4, 4], 5) == "NORMAL"


def test_prefall_pose_gate_rejects_low_quality_windows() -> None:
    assert not prefall_pose_gate(0.0, 0.5)
    assert not prefall_pose_gate(0.49, 0.5)
    assert prefall_pose_gate(0.5, 0.5)


def test_prefall_ensemble_discovers_all_fold_directories(tmp_path, monkeypatch) -> None:
    def fake_model(*_args, **_kwargs):
        return torch.nn.Linear(1, 3)

    monkeypatch.setattr(prefall_module, "build_model", fake_model)
    state = fake_model().state_dict()
    for fold in range(1, 10):
        fold_dir = tmp_path / f"fold_{fold}"
        fold_dir.mkdir()
        torch.save(state, fold_dir / "best.pt")
        (fold_dir / "metrics.json").write_text(
            json.dumps({
                "decision_thresholds_calibrated_on_validation": {
                    "1s": 0.4, "2s": 0.5, "3s": 0.6,
                }
            }),
            encoding="utf-8",
        )
    ensemble = PreFallEnsemble(tmp_path, torch.device("cpu"), min_positive_folds=5)
    assert len(ensemble.models) == 9
    assert ensemble.thresholds.shape == (9, 3)
