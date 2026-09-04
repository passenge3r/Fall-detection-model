"""Plot the complete 300-epoch histories for suspicious-window V-JEPA runs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def plot_run(root: Path, title: str, output: Path) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(14, 9))
    for fold, axis in enumerate(axes.flat, 1):
        rows = read_rows(root / f"fold_{fold}" / "history.csv")
        epochs = [int(row["epoch"]) for row in rows]
        val_loss = [float(row["val_loss"]) for row in rows]
        val_ba = [float(row["val_balanced_accuracy"]) for row in rows]
        metrics = json.loads(
            (root / f"fold_{fold}" / "metrics.json").read_text(encoding="utf-8")
        )
        if "train_loss" in rows[0]:
            axis.plot(epochs, [float(row["train_loss"]) for row in rows], label="Train loss")
        axis.plot(epochs, val_loss, label="Validation loss", color="#e36a33")
        axis.axvline(
            int(metrics["best_epoch"]), color="#2a9d62", linestyle="--",
            label=f"Selected epoch: {metrics['best_epoch']}",
        )
        axis.set(title=f"Fold {fold}", xlabel="Epoch", ylabel="Loss")
        axis.grid(alpha=0.2)
        second = axis.twinx()
        second.plot(epochs, val_ba, color="#7a49a5", alpha=0.7, label="Validation BA")
        second.set_ylim(-0.02, 1.02)
        second.set_ylabel("Balanced accuracy")
        handles, labels = axis.get_legend_handles_labels()
        handles2, labels2 = second.get_legend_handles_labels()
        axis.legend(handles + handles2, labels + labels2, fontsize=8, loc="best")
    figure.suptitle(title, fontsize=15)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    plot_run(
        args.root / "linear_probe_e300",
        "Pose-selected V-JEPA 2.1-B linear probe: 300 epochs",
        args.root / "linear_probe_e300" / "learning_curves.png",
    )
    plot_run(
        args.root / "rtmpose_stgcnpp_feature_fusion_e300",
        "RTMPose/ST-GCN++ + pose-selected V-JEPA feature fusion: 300 epochs",
        args.root / "rtmpose_stgcnpp_feature_fusion_e300" / "learning_curves.png",
    )


if __name__ == "__main__":
    main()
