"""Train ST-GCN++ as an ordered four-stage pre-fall classifier.

Stages are safe, far-risk (2-3 s), mid-risk (1-2 s), and near-risk (0-1 s).
The three deployment probabilities are derived cumulatively from one coherent
stage distribution instead of three unrelated sigmoid heads.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from train_prefall_multihorizon_stgcnpp import (
    HORIZON_NAMES,
    MultiHorizonSet,
    metric_bundle,
    optimal_threshold,
    plot_history,
    read_names,
    set_seed,
    write_history,
    write_predictions,
)

import sys

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402


STAGE_NAMES = ("safe", "far_2_3s", "mid_1_2s", "near_0_1s")


def labels_to_stage(labels: torch.Tensor) -> torch.Tensor:
    """Convert nested y1/y2/y3 targets to safe/far/mid/near stage IDs."""
    stage = torch.zeros(len(labels), dtype=torch.long, device=labels.device)
    stage = torch.where(labels[:, 2] > 0.5, 1, stage)
    stage = torch.where(labels[:, 1] > 0.5, 2, stage)
    stage = torch.where(labels[:, 0] > 0.5, 3, stage)
    return stage


def stage_probabilities_to_horizons(probabilities: torch.Tensor) -> torch.Tensor:
    """Map P(stage) to P(fall within 1 s), 2 s, and 3 s."""
    return torch.stack(
        (
            probabilities[:, 3],
            probabilities[:, 2] + probabilities[:, 3],
            probabilities[:, 1] + probabilities[:, 2] + probabilities[:, 3],
        ),
        dim=1,
    )


@torch.inference_mode()
def evaluate(
    model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: torch.device
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    model.eval()
    total_loss = 0.0
    labels_all: list[np.ndarray] = []
    scores_all: list[np.ndarray] = []
    stages_all: list[np.ndarray] = []
    names_all: list[str] = []
    for samples, labels, names in loader:
        samples = samples.to(device)
        labels = labels.to(device)
        stage = labels_to_stage(labels)
        logits = model(samples)
        loss = loss_fn(logits, stage)
        total_loss += float(loss) * len(labels)
        scores = stage_probabilities_to_horizons(torch.softmax(logits, dim=1))
        labels_all.append(labels.cpu().numpy())
        scores_all.append(scores.cpu().numpy())
        stages_all.append(stage.cpu().numpy())
        names_all.extend(names)
    return (
        total_loss / len(loader.dataset),
        np.concatenate(labels_all),
        np.concatenate(scores_all),
        np.concatenate(stages_all),
        names_all,
    )


def stage_accuracy(target: np.ndarray, scores: np.ndarray) -> float:
    return float(np.mean(target == scores.argmax(axis=1)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=PROJECT / "data/gcn/gmdcsa24_rtmpose_prefall_w64_s16_h123.npz")
    parser.add_argument("--splits", type=Path, default=PROJECT / "data/splits/gmdcsa24_prefall_loso")
    parser.add_argument("--fold", type=int, choices=(1, 2, 3, 4), required=True)
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
    args = parser.parse_args()

    set_seed(args.seed + args.fold)
    args.output.mkdir(parents=True, exist_ok=True)
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    with np.load(args.data) as package:
        data = package["data"].astype(np.float32)
        labels = package["labels"].astype(np.float32)
        names = package["names"]
    fold_dir = args.splits / f"fold_{args.fold}"
    datasets = {
        split: MultiHorizonSet(
            data, labels, names, read_names(fold_dir / f"{split}.csv"), split == "train", "base"
        )
        for split in ("train", "val", "test")
    }
    loaders = {
        split: DataLoader(
            dataset,
            batch_size=args.batch_size,
            shuffle=split == "train",
            num_workers=0,
            pin_memory=device.type == "cuda",
        )
        for split, dataset in datasets.items()
    }

    train_targets = torch.from_numpy(labels[datasets["train"].indices])
    train_stages = labels_to_stage(train_targets).numpy()
    stage_counts = np.bincount(train_stages, minlength=4)
    # Square-root inverse frequency is less brittle than full inverse weighting.
    class_weights = np.sqrt(stage_counts.sum() / np.maximum(stage_counts, 1))
    class_weights /= class_weights.mean()
    loss_fn = nn.CrossEntropyLoss(
        weight=torch.as_tensor(class_weights, dtype=torch.float32, device=device)
    )
    model = build_model(
        "stgcnpp", num_class=4, in_channels=3,
        base_channels=args.base_channels, dropout=args.dropout,
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    amp_enabled = device.type == "cuda" and not args.no_amp
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)
    checkpoint = args.output / "best.pt"
    history: list[dict[str, object]] = []
    best_score = -1.0
    best_epoch = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        for samples, labels_batch, _ in loaders["train"]:
            samples = samples.to(device)
            labels_batch = labels_batch.to(device)
            target_stage = labels_to_stage(labels_batch)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=amp_enabled):
                logits = model(samples)
                loss = loss_fn(logits, target_stage)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            scaler.step(optimizer)
            scaler.update()
            total_loss += float(loss.detach()) * len(labels_batch)
        scheduler.step()

        val_loss, val_labels, val_scores, val_stages, _ = evaluate(model, loaders["val"], loss_fn, device)
        thresholds = np.asarray([
            optimal_threshold(val_labels[:, index], val_scores[:, index]) for index in range(3)
        ])
        metrics = metric_bundle(val_labels, val_scores, thresholds)
        record = {
            "epoch": epoch,
            "train_loss": total_loss / len(datasets["train"]),
            "val_loss": val_loss,
            "val_mean_balanced_accuracy": metrics["mean_balanced_accuracy"],
            "val_mean_f1": metrics["mean_f1"],
            "val_mean_pr_auc": metrics["mean_pr_auc"],
        }
        history.append(record)
        # PR-AUC is threshold-free and better aligned with this highly imbalanced task.
        score = float(metrics["mean_pr_auc"])
        if score > best_score + 1e-9:
            best_score = score
            best_epoch = epoch
            torch.save(model.state_dict(), checkpoint)
        print(json.dumps(record), flush=True)

    model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=True))
    result = {}
    saved = {}
    thresholds = None
    for split in ("val", "test"):
        loss, split_labels, split_scores, split_stages, split_names = evaluate(
            model, loaders[split], loss_fn, device
        )
        stage_probs = []
        with torch.inference_mode():
            for samples, _, _ in loaders[split]:
                logits = model(samples.to(device))
                stage_probs.append(torch.softmax(logits, dim=1).cpu().numpy())
        stage_probs_array = np.concatenate(stage_probs)
        if split == "val":
            thresholds = np.asarray([
                optimal_threshold(split_labels[:, index], split_scores[:, index]) for index in range(3)
            ])
        assert thresholds is not None
        result[split] = {
            "loss": loss,
            "stage_accuracy": stage_accuracy(split_stages, stage_probs_array),
            **metric_bundle(split_labels, split_scores, thresholds),
        }
        write_predictions(args.output / f"{split}_predictions.csv", split_names, split_labels, split_scores)
        saved[split] = len(split_names)

    summary = {
        "route": "RTMPose+ST-GCN++ ordered four-stage pre-fall",
        "fold": args.fold,
        "stage_names": STAGE_NAMES,
        "best_epoch": best_epoch,
        "checkpoint_metric": "validation mean PR-AUC",
        "epochs_ran": args.epochs,
        "device": str(device),
        "samples": saved,
        "train_stage_counts": dict(zip(STAGE_NAMES, stage_counts.tolist(), strict=True)),
        "class_weights": dict(zip(STAGE_NAMES, class_weights.tolist(), strict=True)),
        "decision_thresholds_calibrated_on_validation": dict(zip(HORIZON_NAMES, thresholds.tolist(), strict=True)),
        "validation": result["val"],
        "test": result["test"],
        "config": {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
    }
    (args.output / "metrics.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_history(args.output / "history.csv", history)
    plot_history(args.output / "learning_curve.png", history)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
