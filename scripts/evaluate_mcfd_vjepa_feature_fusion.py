"""Evaluate GMDCSA24-trained skeleton/V-JEPA feature fusion on external MCFD."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402
from evaluate_mcfd_ensemble import metrics, select_threshold  # noqa: E402
from train_vjepa_stgcnpp_feature_fusion import skeleton_features  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skeleton-data", type=Path, required=True)
    parser.add_argument("--skeleton-checkpoints", type=Path, required=True)
    parser.add_argument("--fusion-checkpoints", type=Path, required=True)
    parser.add_argument("--vjepa-features", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    sk_pack = np.load(args.skeleton_data); data = sk_pack["data"].astype(np.float32)
    labels = sk_pack["labels"].astype(int); names = sk_pack["names"].astype(str); cameras = sk_pack["cameras"].astype(str)
    vj_pack = np.load(args.vjepa_features); index = {name: i for i, name in enumerate(vj_pack["names"].astype(str))}
    if set(names) != set(index):
        raise ValueError(f"Feature names differ: skeleton={len(set(names))}, V-JEPA={len(index)}")
    vjepa = np.stack([vj_pack["features"][index[name]] for name in names]).astype(np.float32)
    fold_scores = []
    for fold in range(1, 5):
        skeleton = build_model("stgcnpp", num_class=2, in_channels=3, num_point=17, num_person=1,
                               base_channels=64, dropout=0.5).to(args.device)
        skeleton.load_state_dict(torch.load(args.skeleton_checkpoints / f"fold_{fold}" / "best.pt",
                                            map_location=args.device, weights_only=True)); skeleton.eval()
        sk_features = skeleton_features(skeleton, data, args.device)
        # This checkpoint is produced locally by our fusion trainer and also contains
        # NumPy normalization arrays, which are intentionally outside weights-only mode.
        saved = torch.load(args.fusion_checkpoints / f"fold_{fold}" / "best.pt", map_location="cpu", weights_only=False)
        combined = np.concatenate([
            (sk_features - saved["skeleton_mean"]) / saved["skeleton_std"],
            (vjepa - saved["vjepa_mean"]) / saved["vjepa_std"],
        ], axis=1).astype(np.float32)
        weight = saved["head"]["weight"]; head = nn.Linear(weight.shape[1], weight.shape[0]).to(args.device)
        head.load_state_dict(saved["head"]); head.eval()
        with torch.inference_mode():
            score = head(torch.from_numpy(combined).to(args.device)).softmax(1)[:, 1].cpu().numpy()
        fold_scores.append(score); print(f"fold={fold} complete", flush=True)
    probabilities = np.mean(np.stack(fold_scores), axis=0)
    masks = {"all": np.ones(len(labels), dtype=bool), "cam1": cameras == "1",
             "cross_view_test": np.isin(cameras, ["2", "4", "5", "6", "7", "8"])}
    threshold, calibration = select_threshold(labels[masks["cam1"]], probabilities[masks["cam1"]])
    result = {"protocol": "GMDCSA24-trained fusion, four-fold probability ensemble, no MCFD training",
              "threshold_selection": {"source": "MCFD cam1 only", "selected": threshold, "metrics": calibration},
              "fixed_0p5": {name: metrics(labels[mask], probabilities[mask]) for name, mask in masks.items()},
              "calibrated": {name: metrics(labels[mask], probabilities[mask], threshold) for name, mask in masks.items()}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
