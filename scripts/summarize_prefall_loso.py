from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


HORIZONS = ("1s", "2s", "3s")
METRICS = ("accuracy", "precision", "recall", "specificity", "f1", "balanced_accuracy", "pr_auc")


def mean_std(values: list[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=np.float64)
    return {"mean": float(array.mean()), "std": float(array.std(ddof=1))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--fold-count", type=int, default=4)
    args = parser.parse_args()

    folds = [
        json.loads((args.root / f"fold_{fold}/metrics.json").read_text(encoding="utf-8"))
        for fold in range(1, args.fold_count + 1)
    ]
    per_horizon = {
        horizon: {
            metric: mean_std([float(fold["test"]["per_horizon"][horizon][metric]) for fold in folds])
            for metric in METRICS
        }
        for horizon in HORIZONS
    }
    overall = {
        metric: mean_std([float(fold["test"][metric]) for fold in folds])
        for metric in ("mean_balanced_accuracy", "mean_f1", "mean_pr_auc")
    }
    summary = {
        "protocol": (
            f"{args.fold_count}-fold subject-independent LOSO; "
            "validation-only checkpoint and threshold selection"
        ),
        "epochs_per_fold": sorted({int(fold["epochs_ran"]) for fold in folds}),
        "folds": [
            {
                "fold": int(fold["fold"]), "best_epoch": int(fold["best_epoch"]),
                "test_mean_balanced_accuracy": float(fold["test"]["mean_balanced_accuracy"]),
                "test_mean_f1": float(fold["test"]["mean_f1"]),
                "test_mean_pr_auc": float(fold["test"]["mean_pr_auc"]),
            }
            for fold in folds
        ],
        "test_fold_mean_std": {"per_horizon": per_horizon, "overall": overall},
    }
    (args.root / "loso_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (args.root / "loso_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle); writer.writerow(["horizon", "metric", "mean", "std"])
        for horizon in HORIZONS:
            for metric in METRICS:
                writer.writerow([horizon, metric, per_horizon[horizon][metric]["mean"], per_horizon[horizon][metric]["std"]])

    columns = 3 if args.fold_count > 4 else 2
    rows_count = math.ceil(args.fold_count / columns)
    figure, axes = plt.subplots(rows_count, columns, figsize=(6 * columns, 4 * rows_count))
    axes_array = np.atleast_1d(axes).flat
    for fold_number, axis in enumerate(axes_array, 1):
        if fold_number > args.fold_count:
            axis.axis("off")
            continue
        with (args.root / f"fold_{fold_number}/history.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        epoch = np.asarray([int(row["epoch"]) for row in rows]); metrics = folds[fold_number - 1]
        axis.plot(epoch, [float(row["train_loss"]) for row in rows], label="train loss")
        axis.plot(epoch, [float(row["val_loss"]) for row in rows], label="validation loss")
        axis.axvline(metrics["best_epoch"], color="#2a9d62", linestyle="--", label=f"best epoch {metrics['best_epoch']}")
        axis.set(title=f"Fold {fold_number}", xlabel="Epoch", ylabel="Loss"); axis.grid(alpha=0.2); axis.legend(fontsize=8)
    epochs_label = ",".join(map(str, summary["epochs_per_fold"]))
    figure.suptitle(
        f"Pre-fall RTMPose + ST-GCN++: {epochs_label}-epoch LOSO learning curves"
    )
    figure.tight_layout()
    figure.savefig(
        args.root / f"learning_curves_{args.fold_count}fold.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(figure)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
