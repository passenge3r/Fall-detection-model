"""Train subject-isolated linear probes on cached V-JEPA 2.1 features."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=3e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-2)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--device", default="cuda")
    return parser.parse_args()


def metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    labels = labels.astype(int)
    predictions = predictions.astype(int)
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))

    def safe(numerator: float, denominator: float) -> float:
        return numerator / denominator if denominator else 0.0

    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def write_predictions(
    path: Path,
    names: np.ndarray,
    labels: np.ndarray,
    probabilities: np.ndarray,
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "label", "prediction", "fall_probability"])
        for name, label, probability in zip(names, labels, probabilities, strict=True):
            writer.writerow([str(name), int(label), int(probability >= 0.5), float(probability)])


def evaluate(
    model: nn.Module, features: torch.Tensor, labels: np.ndarray
) -> tuple[float, np.ndarray]:
    model.eval()
    with torch.inference_mode():
        logits = model(features)
        loss = nn.functional.cross_entropy(
            logits, torch.as_tensor(labels, dtype=torch.long, device=features.device)
        )
        probabilities = logits.softmax(dim=1)[:, 1].cpu().numpy()
    return float(loss), probabilities


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.device.startswith("cuda"):
        torch.cuda.manual_seed_all(args.seed)

    package = np.load(args.features)
    features = package["features"].astype(np.float32)
    labels = package["labels"].astype(np.int64)
    subjects = package["subjects"].astype(str)
    names = package["paths"].astype(str)
    unique_subjects = sorted(np.unique(subjects), key=lambda item: int(item))
    if len(unique_subjects) < 3:
        raise ValueError("At least three subjects are required for train/val/test isolation")

    args.output_root.mkdir(parents=True, exist_ok=True)
    all_test_labels: list[np.ndarray] = []
    all_test_probabilities: list[np.ndarray] = []
    fold_summaries: list[dict[str, object]] = []

    for fold_index, test_subject in enumerate(unique_subjects):
        val_subject = unique_subjects[(fold_index + 1) % len(unique_subjects)]
        train_mask = (subjects != test_subject) & (subjects != val_subject)
        val_mask = subjects == val_subject
        test_mask = subjects == test_subject

        mean = features[train_mask].mean(axis=0, keepdims=True)
        std = features[train_mask].std(axis=0, keepdims=True)
        std[std < 1e-6] = 1.0

        def tensor(mask: np.ndarray) -> torch.Tensor:
            normalized = (features[mask] - mean) / std
            return torch.from_numpy(normalized).to(args.device)

        train_x, val_x, test_x = tensor(train_mask), tensor(val_mask), tensor(test_mask)
        train_y = torch.as_tensor(labels[train_mask], dtype=torch.long, device=args.device)

        torch.manual_seed(args.seed + fold_index)
        model = nn.Linear(features.shape[1], 2).to(args.device)
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=args.epochs, eta_min=args.learning_rate / 100
        )
        best_val_loss = float("inf")
        best_epoch = 0
        best_state: dict[str, torch.Tensor] | None = None
        history: list[dict[str, float | int]] = []

        for epoch in range(1, args.epochs + 1):
            model.train()
            optimizer.zero_grad(set_to_none=True)
            logits = model(train_x)
            train_loss = nn.functional.cross_entropy(logits, train_y)
            train_loss.backward()
            optimizer.step()
            scheduler.step()
            val_loss, val_probabilities = evaluate(model, val_x, labels[val_mask])
            val_metrics = metrics(labels[val_mask], val_probabilities >= 0.5)
            history.append(
                {
                    "epoch": epoch,
                    "train_loss": float(train_loss.detach().cpu()),
                    "val_loss": val_loss,
                    "val_f1": float(val_metrics["f1"]),
                    "val_balanced_accuracy": float(val_metrics["balanced_accuracy"]),
                    "learning_rate": optimizer.param_groups[0]["lr"],
                }
            )
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epoch
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}

        assert best_state is not None
        model.load_state_dict(best_state)
        val_loss, val_probabilities = evaluate(model, val_x, labels[val_mask])
        test_loss, test_probabilities = evaluate(model, test_x, labels[test_mask])
        val_metrics = metrics(labels[val_mask], val_probabilities >= 0.5)
        test_metrics = metrics(labels[test_mask], test_probabilities >= 0.5)

        fold_dir = args.output_root / f"fold_{test_subject}"
        fold_dir.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "model": best_state,
                "feature_mean": torch.from_numpy(mean),
                "feature_std": torch.from_numpy(std),
                "feature_dim": features.shape[1],
            },
            fold_dir / "best.pt",
        )
        with (fold_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(history[0]))
            writer.writeheader()
            writer.writerows(history)
        write_predictions(
            fold_dir / "val_predictions.csv",
            names[val_mask], labels[val_mask], val_probabilities,
        )
        write_predictions(
            fold_dir / "test_predictions.csv",
            names[test_mask], labels[test_mask], test_probabilities,
        )
        fold_summary = {
            "fold": int(test_subject),
            "train_subjects": sorted(set(subjects[train_mask]), key=int),
            "val_subject": val_subject,
            "test_subject": test_subject,
            "samples": {
                "train": int(train_mask.sum()),
                "val": int(val_mask.sum()),
                "test": int(test_mask.sum()),
            },
            "epochs_ran": args.epochs,
            "best_epoch": best_epoch,
            "validation": {"loss": val_loss, **val_metrics},
            "test": {"loss": test_loss, **test_metrics},
        }
        (fold_dir / "metrics.json").write_text(
            json.dumps(fold_summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        fold_summaries.append(fold_summary)
        all_test_labels.append(labels[test_mask])
        all_test_probabilities.append(test_probabilities)
        print(
            f"fold={test_subject} best_epoch={best_epoch} "
            f"test_f1={test_metrics['f1']:.4f} test_bal_acc={test_metrics['balanced_accuracy']:.4f}",
            flush=True,
        )

    oof_labels = np.concatenate(all_test_labels)
    oof_probabilities = np.concatenate(all_test_probabilities)
    summary = {
        "route": "V-JEPA 2.1-B frozen encoder + linear probe",
        "features": str(args.features),
        "protocol": "4-fold leave-one-subject-out; next subject is validation",
        "epochs": args.epochs,
        "selection": "minimum validation cross-entropy; no early stopping",
        "oof_test": metrics(oof_labels, oof_probabilities >= 0.5),
        "folds": fold_summaries,
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary["oof_test"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
