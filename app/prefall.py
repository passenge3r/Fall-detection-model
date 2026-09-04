from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch

from models import build_model


HORIZONS = ("1s", "2s", "3s")


def risk_level(positive_folds: list[int], min_positive_folds: int) -> str:
    if positive_folds[0] >= min_positive_folds:
        return "HIGH"
    if positive_folds[1] >= min_positive_folds:
        return "MEDIUM"
    if positive_folds[2] >= min_positive_folds:
        return "LOW"
    return "NORMAL"


class PreFallEnsemble:
    """LOSO ST-GCN++ ensemble with fold-specific validation thresholds."""

    def __init__(self, root: Path, device: torch.device, min_positive_folds: int = 2) -> None:
        self.device = device
        self.min_positive_folds = min_positive_folds
        self.models: list[torch.nn.Module] = []
        thresholds: list[list[float]] = []
        fold_dirs = sorted(
            (path for path in root.glob("fold_*") if path.is_dir()),
            key=lambda path: int(path.name.rsplit("_", 1)[-1]),
        )
        if not fold_dirs:
            raise FileNotFoundError(f"No pre-fall fold directories found in {root}")
        for fold_dir in fold_dirs:
            checkpoint = fold_dir / "best.pt"
            metrics_path = fold_dir / "metrics.json"
            if not checkpoint.is_file() or not metrics_path.is_file():
                raise FileNotFoundError(f"Missing pre-fall artifacts in {fold_dir}")
            model = build_model("stgcnpp", num_class=3, base_channels=64, dropout=0.5).to(device)
            model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=True))
            model.eval(); self.models.append(model)
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            values = metrics["decision_thresholds_calibrated_on_validation"]
            thresholds.append([float(values[name]) for name in HORIZONS])
        if not 1 <= self.min_positive_folds <= len(self.models):
            raise ValueError(
                f"min_positive_folds must be within 1..{len(self.models)}, "
                f"got {self.min_positive_folds}"
            )
        self.thresholds = np.asarray(thresholds, dtype=np.float32)

    @torch.inference_mode()
    def predict(self, sample: np.ndarray) -> dict[str, object]:
        tensor = torch.from_numpy(sample[None]).to(self.device, non_blocking=True)
        per_fold = []
        for model in self.models:
            raw = torch.sigmoid(model(tensor))[0].cpu().numpy()
            per_fold.append(np.maximum.accumulate(raw))
        probabilities = np.asarray(per_fold, dtype=np.float32)
        positive = probabilities >= self.thresholds
        votes = positive.sum(axis=0).astype(int).tolist()
        means = probabilities.mean(axis=0).tolist()
        return {
            "enabled": True,
            "risk_level": risk_level(votes, self.min_positive_folds),
            "probabilities": dict(zip(HORIZONS, means, strict=True)),
            "positive_folds": dict(zip(HORIZONS, votes, strict=True)),
            "min_positive_folds": self.min_positive_folds,
            "ensemble_folds": len(self.models),
            "per_fold_probabilities": [
                dict(zip(HORIZONS, row.tolist(), strict=True)) for row in probabilities
            ],
            "experimental": True,
        }
