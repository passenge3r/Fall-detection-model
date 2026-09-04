"""Validation-selected score fusion of skeleton and V-JEPA fall classifiers."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skeleton-root", type=Path, required=True)
    parser.add_argument("--vjepa-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--alpha-step", type=float, default=0.05)
    return parser.parse_args()


def calculate(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))

    def safe(a: float, b: float) -> float:
        return a / b if b else 0.0

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


def read_predictions(path: Path) -> dict[str, tuple[int, float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            row["path"]: (int(row["label"]), float(row["fall_probability"]))
            for row in csv.DictReader(handle)
        }


def aligned(
    left: dict[str, tuple[int, float]], right: dict[str, tuple[int, float]]
) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    if set(left) != set(right):
        missing_left = sorted(set(right) - set(left))[:5]
        missing_right = sorted(set(left) - set(right))[:5]
        raise ValueError(f"Prediction paths differ: left missing={missing_left}, right missing={missing_right}")
    names = sorted(left)
    labels = np.asarray([left[name][0] for name in names], dtype=int)
    other_labels = np.asarray([right[name][0] for name in names], dtype=int)
    if not np.array_equal(labels, other_labels):
        raise ValueError("Labels differ between routes")
    left_scores = np.asarray([left[name][1] for name in names], dtype=float)
    right_scores = np.asarray([right[name][1] for name in names], dtype=float)
    return names, labels, left_scores, right_scores


def main() -> None:
    args = parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    alphas = np.arange(0.0, 1.0 + args.alpha_step / 2, args.alpha_step)
    all_labels: list[np.ndarray] = []
    all_skeleton: list[np.ndarray] = []
    all_vjepa: list[np.ndarray] = []
    all_fused: list[np.ndarray] = []
    fold_results: list[dict[str, object]] = []

    for fold in range(1, 5):
        skeleton_fold = args.skeleton_root / f"fold_{fold}"
        vjepa_fold = args.vjepa_root / f"fold_{fold}"
        _, val_labels, val_skeleton, val_vjepa = aligned(
            read_predictions(skeleton_fold / "val_predictions.csv"),
            read_predictions(vjepa_fold / "val_predictions.csv"),
        )
        names, test_labels, test_skeleton, test_vjepa = aligned(
            read_predictions(skeleton_fold / "test_predictions.csv"),
            read_predictions(vjepa_fold / "test_predictions.csv"),
        )

        candidates = []
        for alpha in alphas:
            val_fused = alpha * val_skeleton + (1 - alpha) * val_vjepa
            score = calculate(val_labels, val_fused >= 0.5)
            candidates.append((float(score["f1"]), float(score["balanced_accuracy"]), float(alpha)))
        # Prefer skeleton on exact ties: the extra video branch should justify itself.
        _, _, alpha = max(candidates, key=lambda item: (item[0], item[1], item[2]))
        test_fused = alpha * test_skeleton + (1 - alpha) * test_vjepa
        fused_metrics = calculate(test_labels, test_fused >= 0.5)
        fold_results.append(
            {
                "fold": fold,
                "skeleton_weight": alpha,
                "vjepa_weight": 1 - alpha,
                "validation_selection": "maximum F1, then balanced accuracy, fixed threshold 0.5",
                "test": fused_metrics,
            }
        )
        fold_dir = args.output_root / f"fold_{fold}"
        fold_dir.mkdir(parents=True, exist_ok=True)
        with (fold_dir / "test_predictions.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["path", "label", "prediction", "fall_probability", "skeleton_probability", "vjepa_probability"]
            )
            for row in zip(names, test_labels, test_fused, test_skeleton, test_vjepa, strict=True):
                name, label, fused, skeleton, vjepa = row
                writer.writerow([name, int(label), int(fused >= 0.5), fused, skeleton, vjepa])
        all_labels.append(test_labels)
        all_skeleton.append(test_skeleton)
        all_vjepa.append(test_vjepa)
        all_fused.append(test_fused)
        print(f"fold={fold} skeleton_weight={alpha:.2f} test_f1={fused_metrics['f1']:.4f}")

    labels = np.concatenate(all_labels)
    skeleton = np.concatenate(all_skeleton)
    vjepa = np.concatenate(all_vjepa)
    fused = np.concatenate(all_fused)
    summary = {
        "method": "per-fold validation-selected score fusion; test data never selects weights",
        "threshold": 0.5,
        "skeleton_only": calculate(labels, skeleton >= 0.5),
        "vjepa_only": calculate(labels, vjepa >= 0.5),
        "fused": calculate(labels, fused >= 0.5),
        "folds": fold_results,
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
