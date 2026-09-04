"""Train 300-epoch LOSO five-class probes on frozen V-JEPA 2.1 features."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

import matplotlib
import numpy as np
import torch
from torch import nn

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


CLASS_NAMES = ["walking", "standing", "sitting", "lying_sleeping", "falling"]


def multiclass_metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, object]:
    count = len(CLASS_NAMES)
    confusion = np.zeros((count, count), dtype=int)
    for label, prediction in zip(labels.astype(int), predictions.astype(int), strict=True):
        confusion[label, prediction] += 1
    per_class = {}
    precisions, recalls, f1s = [], [], []
    for index, name in enumerate(CLASS_NAMES):
        tp = int(confusion[index, index])
        fp = int(confusion[:, index].sum() - tp)
        fn = int(confusion[index, :].sum() - tp)
        support = int(confusion[index, :].sum())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[name] = {
            "precision": precision, "recall": recall, "f1": f1, "support": support
        }
        precisions.append(precision); recalls.append(recall); f1s.append(f1)
    fall_true = labels == 4
    fall_pred = predictions == 4
    tp = int(np.sum(fall_true & fall_pred)); tn = int(np.sum(~fall_true & ~fall_pred))
    fp = int(np.sum(~fall_true & fall_pred)); fn = int(np.sum(fall_true & ~fall_pred))
    fall_recall = tp / (tp + fn) if tp + fn else 0.0
    fall_specificity = tn / (tn + fp) if tn + fp else 0.0
    return {
        "accuracy": float(np.mean(labels == predictions)),
        "macro_precision": float(np.mean(precisions)),
        "macro_recall_balanced_accuracy": float(np.mean(recalls)),
        "macro_f1": float(np.mean(f1s)),
        "per_class": per_class,
        "confusion_matrix": confusion.tolist(),
        "fall_vs_rest": {
            "balanced_accuracy": (fall_recall + fall_specificity) / 2,
            "recall": fall_recall, "specificity": fall_specificity,
            "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        },
    }


@torch.inference_mode()
def evaluate(model: nn.Module, x: torch.Tensor, labels: np.ndarray) -> tuple[float, np.ndarray]:
    model.eval()
    logits = model(x)
    loss = nn.functional.cross_entropy(
        logits, torch.as_tensor(labels, dtype=torch.long, device=x.device)
    )
    return float(loss), logits.argmax(1).cpu().numpy()


def write_predictions(
    path: Path, names: np.ndarray, labels: np.ndarray, predictions: np.ndarray
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["segment_id", "label", "class_name", "prediction", "predicted_class"])
        for name, label, prediction in zip(names, labels, predictions, strict=True):
            writer.writerow(
                [str(name), int(label), CLASS_NAMES[int(label)], int(prediction), CLASS_NAMES[int(prediction)]]
            )


def plot_curves(root: Path) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(14, 9))
    for fold, axis in enumerate(axes.flat, 1):
        with (root / f"fold_{fold}" / "history.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        metrics = json.loads(
            (root / f"fold_{fold}" / "metrics.json").read_text(encoding="utf-8")
        )
        epoch = [int(row["epoch"]) for row in rows]
        axis.plot(epoch, [float(row["train_loss"]) for row in rows], label="Train loss")
        axis.plot(epoch, [float(row["val_loss"]) for row in rows], label="Validation loss")
        axis.axvline(metrics["best_epoch"], linestyle="--", color="#2a9d62",
                     label=f"Selected epoch: {metrics['best_epoch']}")
        axis.set(title=f"Fold {fold}", xlabel="Epoch", ylabel="Loss")
        axis.grid(alpha=0.2)
        second = axis.twinx()
        second.plot(
            epoch, [float(row["val_macro_recall"]) for row in rows],
            color="#7a49a5", alpha=0.7, label="Validation macro recall",
        )
        second.set_ylim(-0.02, 1.02); second.set_ylabel("Macro recall")
        handles, labels = axis.get_legend_handles_labels()
        handles2, labels2 = second.get_legend_handles_labels()
        axis.legend(handles + handles2, labels + labels2, fontsize=8, loc="best")
    figure.suptitle("V-JEPA 2.1-B five-class posture probe: 300 epochs", fontsize=15)
    figure.tight_layout()
    figure.savefig(root / "learning_curves.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=3e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-2)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)

    package = np.load(args.features)
    features = package["features"].astype(np.float32)
    labels = package["labels"].astype(np.int64)
    subjects = package["subjects"].astype(str)
    names = package["paths"].astype(str)
    if sorted(np.unique(labels).tolist()) != list(range(len(CLASS_NAMES))):
        raise ValueError("Feature package does not contain all five classes")
    unique_subjects = sorted(np.unique(subjects), key=int)
    args.output_root.mkdir(parents=True, exist_ok=True)
    all_labels, all_predictions, fold_summaries = [], [], []

    for fold_index, test_subject in enumerate(unique_subjects):
        val_subject = unique_subjects[(fold_index + 1) % len(unique_subjects)]
        train_mask = (subjects != test_subject) & (subjects != val_subject)
        val_mask = subjects == val_subject
        test_mask = subjects == test_subject
        mean = features[train_mask].mean(0, keepdims=True)
        std = features[train_mask].std(0, keepdims=True); std[std < 1e-6] = 1.0
        tensor = lambda mask: torch.from_numpy((features[mask] - mean) / std).to(args.device)
        train_x, val_x, test_x = tensor(train_mask), tensor(val_mask), tensor(test_mask)
        train_y = torch.as_tensor(labels[train_mask], dtype=torch.long, device=args.device)
        counts = np.bincount(labels[train_mask], minlength=len(CLASS_NAMES))
        weights = len(train_y) / (len(CLASS_NAMES) * np.maximum(counts, 1))
        weights_t = torch.as_tensor(weights, dtype=torch.float32, device=args.device)
        torch.manual_seed(args.seed + fold_index)
        model = nn.Linear(features.shape[1], len(CLASS_NAMES)).to(args.device)
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=args.epochs, eta_min=args.learning_rate / 100
        )
        best_loss, best_epoch, best_state = float("inf"), 0, None
        history = []
        for epoch in range(1, args.epochs + 1):
            model.train(); optimizer.zero_grad(set_to_none=True)
            logits = model(train_x)
            train_loss = nn.functional.cross_entropy(logits, train_y, weight=weights_t)
            train_loss.backward(); optimizer.step(); scheduler.step()
            val_loss, val_prediction = evaluate(model, val_x, labels[val_mask])
            val_metric = multiclass_metrics(labels[val_mask], val_prediction)
            history.append(
                {
                    "epoch": epoch, "train_loss": float(train_loss.detach().cpu()),
                    "val_loss": val_loss,
                    "val_accuracy": val_metric["accuracy"],
                    "val_macro_recall": val_metric["macro_recall_balanced_accuracy"],
                    "val_macro_f1": val_metric["macro_f1"],
                    "learning_rate": optimizer.param_groups[0]["lr"],
                }
            )
            if val_loss < best_loss:
                best_loss, best_epoch = val_loss, epoch
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        assert best_state is not None
        model.load_state_dict(best_state)
        val_loss, val_prediction = evaluate(model, val_x, labels[val_mask])
        test_loss, test_prediction = evaluate(model, test_x, labels[test_mask])
        fold_dir = args.output_root / f"fold_{test_subject}"; fold_dir.mkdir(parents=True, exist_ok=True)
        torch.save({"model": best_state, "mean": mean, "std": std, "classes": CLASS_NAMES}, fold_dir / "best.pt")
        with (fold_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(history[0])); writer.writeheader(); writer.writerows(history)
        write_predictions(fold_dir / "test_predictions.csv", names[test_mask], labels[test_mask], test_prediction)
        summary = {
            "fold": int(test_subject), "epochs_ran": args.epochs, "best_epoch": best_epoch,
            "validation": {"loss": val_loss, **multiclass_metrics(labels[val_mask], val_prediction)},
            "test": {"loss": test_loss, **multiclass_metrics(labels[test_mask], test_prediction)},
        }
        (fold_dir / "metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        fold_summaries.append(summary); all_labels.append(labels[test_mask]); all_predictions.append(test_prediction)
        print(
            f"fold={test_subject} best_epoch={best_epoch} "
            f"test_acc={summary['test']['accuracy']:.4f} test_macro_f1={summary['test']['macro_f1']:.4f}",
            flush=True,
        )
    total_labels, total_predictions = np.concatenate(all_labels), np.concatenate(all_predictions)
    summary = {
        "route": "V-JEPA 2.1-B frozen encoder + five-class linear probe",
        "classes": CLASS_NAMES, "protocol": "four-fold LOSO; next subject validation",
        "epochs": args.epochs, "oof_test": multiclass_metrics(total_labels, total_predictions),
        "folds": fold_summaries,
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    plot_curves(args.output_root)
    print(json.dumps(summary["oof_test"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
