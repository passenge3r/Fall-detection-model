"""Plot the Qwen temporal-prompt ablation and triggered fusion outcome."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    basic = json.loads((project / "results/posture5/qwen3vl2b_zero_shot_balanced50/summary.json").read_text(encoding="utf-8"))
    temporal_root = project / "results/posture5/qwen3vl2b_temporal8_balanced50"
    temporal = json.loads((temporal_root / "summary.json").read_text(encoding="utf-8"))
    fusion = json.loads((temporal_root / "triggered_fusion_summary.json").read_text(encoding="utf-8"))
    classes = ["Walking", "Standing", "Sitting", "Lying", "Falling", "Overall"]
    basic_values = list(basic["per_class_recall"].values()) + [basic["accuracy"]]
    temporal_values = list(temporal["per_class_recall"].values()) + [temporal["accuracy"]]
    figure, axes = plt.subplots(1, 2, figsize=(16, 6))
    x = np.arange(len(classes)); width = 0.36
    axes[0].bar(x - width / 2, basic_values, width, label="Basic prompt")
    axes[0].bar(x + width / 2, temporal_values, width, label="Temporal decision prompt")
    axes[0].set_xticks(x, classes); axes[0].set_ylim(0, 1.08)
    axes[0].set(ylabel="Recall / accuracy", title="Qwen3-VL-2B prompt ablation on the same 50 clips")
    axes[0].grid(axis="y", alpha=0.2); axes[0].legend()
    for container in axes[0].containers:
        axes[0].bar_label(container, labels=[f"{bar.get_height():.0%}" for bar in container], padding=3)
    fall = fusion["alarm_counts_by_truth"]["falling"]
    normal = fusion["alarm_counts_by_truth"]["non_falling"]
    categories = ["True falling (10)", "Non-falling (40)"]
    confirmed = [fall.get("level_1_confirmed_fall", 0), normal.get("level_1_confirmed_fall", 0)]
    review = [fall.get("level_2_pose_trigger_review", 0), normal.get("level_2_pose_trigger_review", 0)]
    none = [fall.get("no_fall_alert", 0), normal.get("no_fall_alert", 0)]
    axes[1].bar(categories, confirmed, label="Level 1: both confirm", color="#d1495b")
    axes[1].bar(categories, review, bottom=confirmed, label="Level 2: review", color="#edae49")
    axes[1].bar(categories, none, bottom=np.asarray(confirmed) + np.asarray(review), label="No alert", color="#66a182")
    axes[1].set(ylabel="Number of clips", title="Triggered fusion keeps disagreement as review")
    axes[1].legend(); axes[1].grid(axis="y", alpha=0.2)
    figure.tight_layout()
    figure.savefig(temporal_root / "prompt_and_fusion_ablation.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
