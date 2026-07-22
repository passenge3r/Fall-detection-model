from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


ROUTES = (
    "rtmpose_stgcnpp", "rtmpose_ctrgcn", "rtmpose_posec3d",
    "yolo_stgcnpp", "yolo_ctrgcn", "yolo_posec3d",
    "yolo_bytetrack_stgcnpp", "yolo_bytetrack_ctrgcn", "yolo_bytetrack_posec3d",
    "rtmo_stgcnpp", "rtmo_ctrgcn", "rtmo_posec3d",
    "hourglass_stgcnpp", "hourglass_ctrgcn", "hourglass_posec3d",
    "openpose_stgcnpp", "openpose_ctrgcn", "openpose_posec3d",
    "alphapose_stgcnpp", "alphapose_ctrgcn", "alphapose_posec3d",
)
ROUTE_LABELS = {
    "rtmpose_stgcnpp": "RTMPose + ST-GCN++",
    "rtmpose_ctrgcn": "RTMPose + CTR-GCN",
    "rtmpose_posec3d": "RTMPose + PoseC3D",
    "yolo_stgcnpp": "YOLO-Pose + ST-GCN++",
    "yolo_ctrgcn": "YOLO-Pose + CTR-GCN",
    "yolo_posec3d": "YOLO-Pose + PoseC3D",
    "yolo_bytetrack_stgcnpp": "YOLO-Pose + ByteTrack + ST-GCN++",
    "yolo_bytetrack_ctrgcn": "YOLO-Pose + ByteTrack + CTR-GCN",
    "yolo_bytetrack_posec3d": "YOLO-Pose + ByteTrack + PoseC3D",
    "rtmo_stgcnpp": "RTMO + ST-GCN++",
    "rtmo_ctrgcn": "RTMO + CTR-GCN",
    "rtmo_posec3d": "RTMO + PoseC3D",
    "hourglass_stgcnpp": "Hourglass52 + ST-GCN++",
    "hourglass_ctrgcn": "Hourglass52 + CTR-GCN",
    "hourglass_posec3d": "Hourglass52 + PoseC3D",
    "openpose_stgcnpp": "OpenPose + ST-GCN++",
    "openpose_ctrgcn": "OpenPose + CTR-GCN",
    "openpose_posec3d": "OpenPose + PoseC3D",
    "alphapose_stgcnpp": "AlphaPose + ST-GCN++",
    "alphapose_ctrgcn": "AlphaPose + CTR-GCN",
    "alphapose_posec3d": "AlphaPose + PoseC3D",
}


def read_history(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {
        key: np.asarray([float(row[key]) for row in rows], dtype=np.float64)
        for key in ("epoch", "train_loss", "val_loss", "val_balanced_accuracy")
    }


def plot_route(root: Path, route: str) -> list[dict[str, object]]:
    figure, axes = plt.subplots(2, 2, figsize=(14, 9), sharex=False)
    summary: list[dict[str, object]] = []
    early_stopping: bool | None = None
    for fold, axis in enumerate(axes.flat, 1):
        fold_dir = root / route / f"fold_{fold}"
        history = read_history(fold_dir / "history.csv")
        metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
        early_stopping = metrics["config"].get("early_stopping", True)
        epoch = history["epoch"]
        axis.plot(epoch, history["train_loss"], label="Train loss", color="#2474b5")
        axis.plot(epoch, history["val_loss"], label="Validation loss", color="#e36a33")
        axis.axvline(metrics["best_epoch"], color="#2a9d62", linestyle="--", alpha=0.85,
                     label=f"Best epoch: {metrics['best_epoch']}")
        axis.set(title=f"Fold {fold}", xlabel="Epoch", ylabel="Loss")
        axis.grid(alpha=0.2)
        accuracy_axis = axis.twinx()
        accuracy_axis.plot(epoch, history["val_balanced_accuracy"], color="#7a49a5", alpha=0.65,
                           label="Validation balanced accuracy")
        accuracy_axis.set_ylabel("Balanced accuracy")
        accuracy_axis.set_ylim(-0.02, 1.02)
        handles, labels = axis.get_legend_handles_labels()
        handles2, labels2 = accuracy_axis.get_legend_handles_labels()
        axis.legend(handles + handles2, labels + labels2, fontsize=8, loc="best")
        summary.append({
            "route": route,
            "fold": fold,
            "best_epoch": metrics["best_epoch"],
            "epochs_ran": metrics["epochs_ran"],
            "best_val_balanced_accuracy": metrics["validation"]["balanced_accuracy"],
            "test_accuracy": metrics["test"]["accuracy"],
            "test_f1": metrics["test"]["f1"],
            "test_balanced_accuracy": metrics["test"]["balanced_accuracy"],
        })
    training_mode = "early stopping" if early_stopping else "all 300 epochs (no early stopping)"
    figure.suptitle(f"{ROUTE_LABELS[route]}: {training_mode}", fontsize=15)
    figure.tight_layout()
    figure.savefig(root / route / "learning_curves.png", dpi=180, bbox_inches="tight")
    plt.close(figure)
    return summary


def plot_comparison(root: Path, summaries: list[dict[str, object]]) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(13, 5))
    x = np.arange(1, 5)
    for route in ROUTES:
        rows = [row for row in summaries if row["route"] == route]
        axes[0].plot(x, [row["best_epoch"] for row in rows], marker="o", label=ROUTE_LABELS[route])
        axes[1].plot(x, [row["test_balanced_accuracy"] for row in rows], marker="o",
                     label=ROUTE_LABELS[route])
    axes[0].set(title="Best epoch selected by validation set", xlabel="Fold", ylabel="Best epoch")
    axes[1].set(title="Internal test balanced accuracy", xlabel="Fold", ylabel="Balanced accuracy")
    axes[1].set_ylim(-0.02, 1.02)
    for axis in axes:
        axis.set_xticks(x)
        axis.grid(alpha=0.2)
        axis.legend(fontsize=8)
    figure.suptitle(f"{len(ROUTES)}-route experiment summary", fontsize=15)
    figure.tight_layout()
    figure.savefig(root / "learning_curve_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    summaries: list[dict[str, object]] = []
    for route in ROUTES:
        summaries.extend(plot_route(args.results, route))
    plot_comparison(args.results, summaries)
    with (args.results / "training_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)


if __name__ == "__main__":
    main()
