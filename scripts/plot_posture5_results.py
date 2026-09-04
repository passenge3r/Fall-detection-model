"""Plot five-class confusion matrices and per-class recall comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


CLASSES = ["Walking", "Standing", "Sitting", "Lying", "Falling"]


def normalized(matrix: np.ndarray) -> np.ndarray:
    denominator = matrix.sum(1, keepdims=True)
    return np.divide(matrix, denominator, out=np.zeros_like(matrix, dtype=float), where=denominator > 0)


def annotate(axis: plt.Axes, matrix: np.ndarray) -> None:
    for row in range(len(CLASSES)):
        for column in range(len(CLASSES)):
            axis.text(column, row, f"{matrix[row, column]:.0%}", ha="center", va="center",
                      color="white" if matrix[row, column] > 0.55 else "black")


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skeleton-summary", type=Path,
        default=project / "results/posture5/rtmpose_compact_tgcn_e300/summary.json",
    )
    parser.add_argument(
        "--vjepa-summary", type=Path,
        default=project / "results/posture5/vjepa21b_linear_probe_e300/summary.json",
    )
    parser.add_argument(
        "--qwen-summary", type=Path,
        default=project / "results/posture5/qwen3vl2b_zero_shot_balanced50/summary.json",
    )
    parser.add_argument(
        "--output", type=Path,
        default=project / "results/posture5/posture5_model_comparison.png",
    )
    args = parser.parse_args()
    skeleton = json.loads(args.skeleton_summary.read_text(encoding="utf-8"))["oof_test"]
    vjepa = json.loads(args.vjepa_summary.read_text(encoding="utf-8"))["oof_test"]
    qwen = json.loads(args.qwen_summary.read_text(encoding="utf-8"))
    matrices = [
        normalized(np.asarray(skeleton["confusion_matrix"], dtype=float)),
        normalized(np.asarray(vjepa["confusion_matrix"], dtype=float)),
        normalized(np.asarray(qwen["confusion_matrix"], dtype=float)),
    ]
    recalls = [np.diag(matrix) for matrix in matrices]
    figure = plt.figure(figsize=(20, 9))
    grid = figure.add_gridspec(2, 3, height_ratios=(1, 0.75))
    for index, (matrix, title) in enumerate(zip(
        matrices,
        ("RTMPose + compact graph-temporal\n292 segments, 300 epochs/fold LOSO",
         "V-JEPA 2.1-B + 300-epoch linear probe\n292 segments, four-fold LOSO",
         "Qwen3-VL-2B zero-shot\n50-segment balanced pilot"),
        strict=True,
    )):
        axis = figure.add_subplot(grid[0, index])
        axis.imshow(matrix, cmap="Blues", vmin=0, vmax=1)
        annotate(axis, matrix)
        axis.set_xticks(range(len(CLASSES)), CLASSES, rotation=25, ha="right")
        axis.set_yticks(range(len(CLASSES)), CLASSES)
        axis.set(xlabel="Predicted class", ylabel="True class", title=title)
    axis = figure.add_subplot(grid[1, :])
    x = np.arange(len(CLASSES)); width = 0.25
    axis.bar(x - width, recalls[0], width, label="RTMPose + graph-temporal")
    axis.bar(x, recalls[1], width, label="V-JEPA 2.1-B")
    axis.bar(x + width, recalls[2], width, label="Qwen3-VL-2B")
    axis.set_xticks(x, CLASSES); axis.set_ylim(0, 1.08)
    axis.set(ylabel="Recall", title="Per-class recall (protocols differ; Qwen result is a pilot)")
    axis.grid(axis="y", alpha=0.2); axis.legend()
    for container in axis.containers:
        axis.bar_label(
            container,
            labels=[f"{bar.get_height():.0%}" for bar in container],
            padding=3,
        )
    figure.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
