"""Train a shared ST-GCN++ encoder for 1/2/3-second pre-fall prediction."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

import matplotlib
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402


HORIZON_NAMES = ("1s", "2s", "3s")


def causal_smooth_xy(xy: np.ndarray, valid: np.ndarray, alpha: float = 0.4) -> np.ndarray:
    """Confidence-aware causal EMA; never uses frames after the current frame."""
    smoothed = xy.copy()
    initialized = np.zeros(xy.shape[2], dtype=bool)
    state = np.zeros((2, xy.shape[2]), dtype=np.float32)
    for frame in range(xy.shape[1]):
        frame_valid = valid[frame]
        first = frame_valid & ~initialized
        continuing = frame_valid & initialized
        state[:, first] = xy[:, frame, first]
        state[:, continuing] = (
            alpha * xy[:, frame, continuing] + (1 - alpha) * state[:, continuing]
        )
        initialized |= frame_valid
        smoothed[:, frame, frame_valid] = state[:, frame_valid]
    return smoothed


def build_motion_features(sample: np.ndarray, confidence_threshold: float = 0.2,
                          smooth: bool = False) -> np.ndarray:
    """Expand C=3 normalized skeletons to C=9 motion-aware skeletons."""
    if sample.shape[0] != 3:
        raise ValueError(f"Expected C=3 skeleton input, got {sample.shape}")
    raw_xy = sample[:2, :, :, 0]
    confidence = sample[2, :, :, 0]
    valid = confidence >= confidence_threshold
    xy = causal_smooth_xy(raw_xy, valid) if smooth else raw_xy
    velocity = np.zeros_like(xy)
    velocity[:, 1:] = xy[:, 1:] - xy[:, :-1]
    velocity[:, 1:] *= (valid[1:] & valid[:-1])[None]
    acceleration = np.zeros_like(xy)
    acceleration[:, 2:] = velocity[:, 2:] - velocity[:, 1:-1]
    acceleration[:, 2:] *= (valid[2:] & valid[1:-1] & valid[:-2])[None]

    torso_lean = np.zeros(sample.shape[1], dtype=np.float32)
    torso_valid = valid[:, 5] & valid[:, 6] & valid[:, 11] & valid[:, 12]
    shoulder = (xy[:, :, 5] + xy[:, :, 6]) / 2
    hip = (xy[:, :, 11] + xy[:, :, 12]) / 2
    torso = shoulder - hip
    torso_norm = np.linalg.norm(torso, axis=0)
    usable_torso = torso_valid & (torso_norm > 1e-6)
    torso_lean[usable_torso] = torso[0, usable_torso] / torso_norm[usable_torso]

    hip_vertical_velocity = np.zeros(sample.shape[1], dtype=np.float32)
    hip_valid = valid[:, 11] & valid[:, 12]
    hip_y = hip[1]
    pair_valid = hip_valid[1:] & hip_valid[:-1]
    hip_vertical_velocity[1:][pair_valid] = hip_y[1:][pair_valid] - hip_y[:-1][pair_valid]

    output = np.zeros((9, sample.shape[1], sample.shape[2], 1), dtype=np.float32)
    output[:3] = sample
    output[3:5, :, :, 0] = velocity
    output[5:7, :, :, 0] = acceleration
    output[7, :, :, 0] = torso_lean[:, None]
    output[8, :, :, 0] = hip_vertical_velocity[:, None]
    return output


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def read_names(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


class MultiHorizonSet(Dataset):
    def __init__(self, data: np.ndarray, labels: np.ndarray, names: np.ndarray, selected: list[str], augment: bool,
                 features: str = "base") -> None:
        lookup = {str(name): index for index, name in enumerate(names)}
        missing = [name for name in selected if name not in lookup]
        if missing:
            raise RuntimeError(f"Split entries missing from tensor: {missing[:3]}")
        self.indices = np.asarray([lookup[name] for name in selected], dtype=np.int64)
        self.data = data
        self.labels = labels
        self.names = names
        self.augment = augment
        self.features = features

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, item: int) -> tuple[torch.Tensor, torch.Tensor, str]:
        index = int(self.indices[item])
        sample = self.data[index].copy()
        if self.augment:
            valid = sample[2, :, :, 0] >= 0.2
            angle = np.random.uniform(-10, 10) * math.pi / 180
            scale = np.random.uniform(0.9, 1.1)
            rotation = np.asarray(
                [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
                dtype=np.float32,
            ) * scale
            xy = sample[:2, :, :, 0].transpose(1, 2, 0) @ rotation.T
            xy += np.random.normal(0, 0.01, xy.shape).astype(np.float32) * valid[..., None]
            sample[:2, :, :, 0] = xy.transpose(2, 0, 1)
        if self.features in {"motion9", "motion9_smooth"}:
            sample = build_motion_features(sample, smooth=self.features == "motion9_smooth")
        return torch.from_numpy(sample), torch.from_numpy(self.labels[index]), str(self.names[index])


def average_precision(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = int(labels.sum())
    if positives == 0:
        return 0.0
    order = np.argsort(-scores, kind="stable")
    sorted_labels = labels[order]
    precision = np.cumsum(sorted_labels) / np.arange(1, len(labels) + 1)
    return float(np.sum(precision * sorted_labels) / positives)


def binary_metrics(labels: np.ndarray, scores: np.ndarray, threshold: float = 0.5) -> dict[str, float | int]:
    predictions = scores >= threshold
    labels = labels.astype(bool)
    tp = int(np.sum(labels & predictions)); tn = int(np.sum(~labels & ~predictions))
    fp = int(np.sum(~labels & predictions)); fn = int(np.sum(labels & ~predictions))
    safe = lambda a, b: float(a / b) if b else 0.0
    recall = safe(tp, tp + fn); specificity = safe(tn, tn + fp); precision = safe(tp, tp + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)), "precision": precision, "recall": recall,
        "specificity": specificity, "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "pr_auc": average_precision(labels.astype(np.int64), scores), "threshold": float(threshold),
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def optimal_threshold(labels: np.ndarray, scores: np.ndarray) -> float:
    """Find the exact balanced-accuracy optimum in O(n log n).

    Threshold metrics only change when crossing a score. Sorting once avoids the
    previous quadratic loop, which also recomputed threshold-independent AP.
    """
    candidates = np.unique(np.concatenate(([0.0], scores, [1.0])))
    order = np.argsort(scores, kind="stable")
    sorted_scores = scores[order]
    sorted_positive = labels[order].astype(np.int64)
    cumulative_positive = np.concatenate(([0], np.cumsum(sorted_positive)))
    cumulative_negative = np.arange(len(labels) + 1) - cumulative_positive
    split = np.searchsorted(sorted_scores, candidates, side="left")
    positives = int(sorted_positive.sum())
    negatives = len(labels) - positives
    recall = (positives - cumulative_positive[split]) / positives if positives else np.zeros(len(candidates))
    specificity = cumulative_negative[split] / negatives if negatives else np.zeros(len(candidates))
    balanced_accuracy = (recall + specificity) / 2
    return float(candidates[int(np.argmax(balanced_accuracy))])


def metric_bundle(labels: np.ndarray, scores: np.ndarray, thresholds: np.ndarray | None = None) -> dict[str, object]:
    if thresholds is None:
        thresholds = np.full(len(HORIZON_NAMES), 0.5, dtype=np.float64)
    per_horizon = {
        name: binary_metrics(labels[:, index], scores[:, index], float(thresholds[index]))
        for index, name in enumerate(HORIZON_NAMES)
    }
    return {
        "per_horizon": per_horizon,
        "mean_balanced_accuracy": float(np.mean([value["balanced_accuracy"] for value in per_horizon.values()])),
        "mean_f1": float(np.mean([value["f1"] for value in per_horizon.values()])),
        "mean_pr_auc": float(np.mean([value["pr_auc"] for value in per_horizon.values()])),
    }


def multihorizon_loss(logits: torch.Tensor, labels: torch.Tensor, bce: nn.Module) -> torch.Tensor:
    probabilities = torch.sigmoid(logits)
    consistency = torch.relu(probabilities[:, 0] - probabilities[:, 1]).mean()
    consistency += torch.relu(probabilities[:, 1] - probabilities[:, 2]).mean()
    return bce(logits, labels) + 0.1 * consistency


class FocalBCEWithLogits(nn.Module):
    def __init__(self, pos_weight: torch.Tensor, gamma: float = 2.0) -> None:
        super().__init__(); self.register_buffer("pos_weight", pos_weight); self.gamma = gamma

    def forward(self, logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        raw = nn.functional.binary_cross_entropy_with_logits(
            logits, labels, pos_weight=self.pos_weight, reduction="none"
        )
        probabilities = torch.sigmoid(logits)
        probability_true_class = labels * probabilities + (1 - labels) * (1 - probabilities)
        return (((1 - probability_true_class) ** self.gamma) * raw).mean()


def load_oof_hard_negative_scores(root: Path) -> dict[str, float]:
    scores: dict[str, float] = {}
    for fold in range(1, 5):
        fold_dir = root / f"fold_{fold}"
        metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
        thresholds = metrics["decision_thresholds_calibrated_on_validation"]
        with (fold_dir / "test_predictions.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if any(int(float(row[f"y_{horizon}s"])) for horizon in (1, 2, 3)):
                    scores[row["path"]] = 0.0
                    continue
                normalized = [
                    float(row[f"p_{horizon}s"]) / max(float(thresholds[f"{horizon}s"]), 1e-6)
                    for horizon in (1, 2, 3)
                ]
                scores[row["path"]] = float(min(max(normalized), 2.0) / 2.0)
    return scores


@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: torch.device) -> tuple[float, dict[str, object], np.ndarray, np.ndarray, list[str]]:
    model.eval(); total_loss = 0.0; labels_all = []; scores_all = []; names_all = []
    for samples, labels, names in loader:
        samples = samples.to(device); labels = labels.to(device)
        logits = model(samples); loss = multihorizon_loss(logits, labels, loss_fn)
        total_loss += float(loss) * len(labels)
        labels_all.append(labels.cpu().numpy())
        raw_scores = torch.sigmoid(logits).cpu().numpy()
        scores_all.append(np.maximum.accumulate(raw_scores, axis=1))
        names_all.extend(names)
    label_array = np.concatenate(labels_all); score_array = np.concatenate(scores_all)
    return total_loss / len(loader.dataset), metric_bundle(label_array, score_array), label_array, score_array, names_all


def write_predictions(path: Path, names: list[str], labels: np.ndarray, scores: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "y_1s", "p_1s", "y_2s", "p_2s", "y_3s", "p_3s"])
        for name, target, probability in zip(names, labels, scores, strict=True):
            writer.writerow([name, int(target[0]), float(probability[0]), int(target[1]), float(probability[1]), int(target[2]), float(probability[2])])


def write_history(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def plot_history(path: Path, rows: list[dict[str, object]]) -> None:
    epochs = [int(row["epoch"]) for row in rows]
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(epochs, [row["train_loss"] for row in rows], label="train")
    axes[0].plot(epochs, [row["val_loss"] for row in rows], label="validation")
    axes[0].set(title="Multi-horizon loss", xlabel="Epoch", ylabel="BCE loss"); axes[0].legend(); axes[0].grid(alpha=0.2)
    axes[1].plot(epochs, [row["val_mean_balanced_accuracy"] for row in rows], label="mean balanced accuracy")
    axes[1].plot(epochs, [row["val_mean_pr_auc"] for row in rows], label="mean PR-AUC")
    axes[1].set(title="Validation metrics", xlabel="Epoch", ylim=(0, 1)); axes[1].legend(); axes[1].grid(alpha=0.2)
    figure.tight_layout(); figure.savefig(path, dpi=180, bbox_inches="tight"); plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=PROJECT / "data/gcn/gmdcsa24_rtmpose_prefall_w64_s16_h123.npz")
    parser.add_argument("--splits", type=Path, default=PROJECT / "data/splits/gmdcsa24_prefall_loso")
    parser.add_argument("--fold", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-3)
    parser.add_argument("--base-channels", type=int, default=64)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--no-amp", action="store_true")
    parser.add_argument("--features", choices=("base", "motion9", "motion9_smooth"), default="base")
    parser.add_argument("--loss", choices=("bce", "focal"), default="bce")
    parser.add_argument("--focal-gamma", type=float, default=2.0)
    parser.add_argument("--hard-negative-root", type=Path)
    parser.add_argument("--hard-negative-strength", type=float, default=2.0)
    parser.add_argument(
        "--init-checkpoint", type=Path,
        help="Optional compatible ST-GCN++ state_dict used only for weight initialization",
    )
    parser.add_argument(
        "--init-backbone-only", action="store_true",
        help="Load --init-checkpoint except the final fc classification layer",
    )
    args = parser.parse_args()

    set_seed(args.seed + args.fold); args.output.mkdir(parents=True, exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    with np.load(args.data) as package:
        data = package["data"].astype(np.float32); labels = package["labels"].astype(np.float32); names = package["names"]
    fold_dir = args.splits / f"fold_{args.fold}"
    datasets = {
        split: MultiHorizonSet(data, labels, names, read_names(fold_dir / f"{split}.csv"), split == "train", args.features)
        for split in ("train", "val", "test")
    }
    train_sampler = None; hard_negative_summary = None
    if args.hard_negative_root is not None:
        oof_scores = load_oof_hard_negative_scores(args.hard_negative_root)
        missing = [str(names[index]) for index in datasets["train"].indices if str(names[index]) not in oof_scores]
        if missing:
            raise RuntimeError(f"Missing OOF hard-negative scores: {missing[:3]}")
        sampler_weights = []
        selected_scores = []
        for index in datasets["train"].indices:
            score = oof_scores[str(names[index])] if not labels[index].any() else 0.0
            selected_scores.append(score); sampler_weights.append(1 + args.hard_negative_strength * score)
        generator = torch.Generator().manual_seed(args.seed + args.fold)
        train_sampler = WeightedRandomSampler(sampler_weights, len(sampler_weights), replacement=True, generator=generator)
        hard_negative_summary = {
            "source": str(args.hard_negative_root), "mean_oof_score": float(np.mean(selected_scores)),
            "max_sample_weight": float(np.max(sampler_weights)), "strength": args.hard_negative_strength,
        }
    loaders = {
        split: DataLoader(
            dataset, batch_size=args.batch_size,
            shuffle=split == "train" and train_sampler is None,
            sampler=train_sampler if split == "train" else None,
            num_workers=0, pin_memory=device.type == "cuda",
        ) for split, dataset in datasets.items()
    }
    input_channels = 9 if args.features in {"motion9", "motion9_smooth"} else 3
    model = build_model("stgcnpp", num_class=3, in_channels=input_channels,
                        base_channels=args.base_channels, dropout=args.dropout).to(device)
    if args.init_checkpoint is not None:
        init_state = torch.load(args.init_checkpoint, map_location=device, weights_only=True)
        if args.init_backbone_only:
            init_state = {key: value for key, value in init_state.items() if not key.startswith("fc.")}
            incompatible = model.load_state_dict(init_state, strict=False)
            if set(incompatible.missing_keys) != {"fc.weight", "fc.bias"} or incompatible.unexpected_keys:
                raise RuntimeError(f"Unexpected backbone initialization mismatch: {incompatible}")
        else:
            model.load_state_dict(init_state)
    train_labels = labels[datasets["train"].indices]
    positives = train_labels.sum(axis=0); negatives = len(train_labels) - positives
    pos_weight = torch.as_tensor(negatives / np.maximum(positives, 1), dtype=torch.float32, device=device)
    loss_fn = (
        FocalBCEWithLogits(pos_weight, args.focal_gamma)
        if args.loss == "focal" else nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    amp_enabled = device.type == "cuda" and not args.no_amp
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)
    history: list[dict[str, object]] = []; best_score = -1.0; best_epoch = 0
    checkpoint = args.output / "best.pt"
    for epoch in range(1, args.epochs + 1):
        model.train(); total_loss = 0.0
        for samples, batch_labels, _ in loaders["train"]:
            samples = samples.to(device); batch_labels = batch_labels.to(device); optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=amp_enabled):
                logits = model(samples); loss = multihorizon_loss(logits, batch_labels, loss_fn)
            scaler.scale(loss).backward(); scaler.unscale_(optimizer); torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            scaler.step(optimizer); scaler.update(); total_loss += float(loss.detach()) * len(batch_labels)
        scheduler.step()
        val_loss, _, val_target, val_scores, _ = evaluate(model, loaders["val"], loss_fn, device)
        epoch_thresholds = np.asarray(
            [optimal_threshold(val_target[:, index], val_scores[:, index]) for index in range(3)]
        )
        val_metrics = metric_bundle(val_target, val_scores, epoch_thresholds)
        record = {
            "epoch": epoch, "train_loss": total_loss / len(datasets["train"]), "val_loss": val_loss,
            "val_mean_balanced_accuracy": val_metrics["mean_balanced_accuracy"],
            "val_mean_f1": val_metrics["mean_f1"], "val_mean_pr_auc": val_metrics["mean_pr_auc"],
        }
        history.append(record); score = float(val_metrics["mean_balanced_accuracy"])
        if score > best_score + 1e-9:
            best_score = score; best_epoch = epoch; torch.save(model.state_dict(), checkpoint)
        print(json.dumps(record), flush=True)

    model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=True))
    results: dict[str, object] = {}
    val_loss, _, val_target, val_scores, val_names = evaluate(model, loaders["val"], loss_fn, device)
    thresholds = np.asarray(
        [optimal_threshold(val_target[:, index], val_scores[:, index]) for index in range(3)]
    )
    val_metrics = metric_bundle(val_target, val_scores, thresholds)
    results["val"] = {"loss": val_loss, **val_metrics}
    write_predictions(args.output / "val_predictions.csv", val_names, val_target, val_scores)
    test_loss, _, test_target, test_scores, test_names = evaluate(model, loaders["test"], loss_fn, device)
    test_metrics = metric_bundle(test_target, test_scores, thresholds)
    results["test"] = {"loss": test_loss, **test_metrics}
    write_predictions(args.output / "test_predictions.csv", test_names, test_target, test_scores)
    summary = {
        "route": f"RTMPose+ST-GCN++ {args.features} multi-horizon pre-fall", "fold": args.fold,
        "horizons_seconds": [1, 2, 3], "best_epoch": best_epoch, "epochs_ran": args.epochs,
        "device": str(device), "samples": {key: len(value) for key, value in datasets.items()},
        "train_positive_counts": dict(zip(HORIZON_NAMES, positives.astype(int).tolist(), strict=True)),
        "pos_weight": dict(zip(HORIZON_NAMES, pos_weight.cpu().tolist(), strict=True)),
        "hard_negative_sampling": hard_negative_summary,
        "decision_thresholds_calibrated_on_validation": dict(zip(HORIZON_NAMES, thresholds.tolist(), strict=True)),
        "validation": results["val"], "test": results["test"],
        "config": {
            **{key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
            "amp": amp_enabled,
        },
    }
    (args.output / "metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_history(args.output / "history.csv", history); plot_history(args.output / "learning_curve.png", history)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
