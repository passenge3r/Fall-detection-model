"""Validation-selected per-horizon late fusion for base and motion pre-fall models."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from train_prefall_multihorizon_stgcnpp import binary_metrics


HORIZONS = ("1s", "2s", "3s")
ALPHAS = np.asarray((0.0, 0.25, 0.5, 0.75, 1.0), dtype=np.float64)


def read_predictions(path: Path) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    output = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            labels = np.asarray([int(float(row[f"y_{index}s"])) for index in (1, 2, 3)], dtype=np.int64)
            scores = np.asarray([float(row[f"p_{index}s"]) for index in (1, 2, 3)], dtype=np.float64)
            output[row["path"]] = labels, scores
    return output


def align(base: dict[str, tuple[np.ndarray, np.ndarray]], motion: dict[str, tuple[np.ndarray, np.ndarray]]) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    if set(base) != set(motion):
        raise RuntimeError("Base and motion prediction sets differ")
    names = sorted(base)
    labels = np.stack([base[name][0] for name in names])
    motion_labels = np.stack([motion[name][0] for name in names])
    if not np.array_equal(labels, motion_labels):
        raise RuntimeError("Base and motion labels differ")
    return names, labels, np.stack([base[name][1] for name in names]), np.stack([motion[name][1] for name in names])


def best_f1_threshold(labels: np.ndarray, scores: np.ndarray) -> tuple[float, dict[str, float | int]]:
    candidates = np.unique(np.concatenate(([0.0], scores, [1.0])))
    best_threshold = 0.5; best_metrics = binary_metrics(labels, scores, best_threshold)
    best_key = (-1.0, -1.0, -1.0)
    for threshold in candidates:
        metrics = binary_metrics(labels, scores, float(threshold))
        key = (float(metrics["f1"]), float(metrics["balanced_accuracy"]), float(metrics["precision"]))
        if key > best_key:
            best_key = key; best_threshold = float(threshold); best_metrics = metrics
    return best_threshold, best_metrics


def select_fusion(labels: np.ndarray, base_scores: np.ndarray, motion_scores: np.ndarray) -> tuple[float, float, dict[str, float | int]]:
    selected = (0.0, 0.5, binary_metrics(labels, base_scores, 0.5)); best_key = (-1.0, -1.0, -1.0)
    for alpha in ALPHAS:
        scores = (1 - alpha) * base_scores + alpha * motion_scores
        threshold, metrics = best_f1_threshold(labels, scores)
        key = (float(metrics["f1"]), float(metrics["pr_auc"]), float(metrics["balanced_accuracy"]))
        if key > best_key:
            best_key = key; selected = (float(alpha), threshold, metrics)
    return selected


def summarize(values: list[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=np.float64)
    return {"mean": float(array.mean()), "std": float(array.std(ddof=1))}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-root", type=Path, required=True)
    parser.add_argument("--motion-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)

    fold_results = []
    prediction_rows = []
    for fold in range(1, 5):
        aligned = {}
        for split in ("val", "test"):
            base = read_predictions(args.base_root / f"fold_{fold}/{split}_predictions.csv")
            motion = read_predictions(args.motion_root / f"fold_{fold}/{split}_predictions.csv")
            aligned[split] = align(base, motion)
        val_names, val_labels, val_base, val_motion = aligned["val"]
        test_names, test_labels, test_base, test_motion = aligned["test"]
        horizons = {}
        for index, horizon in enumerate(HORIZONS):
            alpha, threshold, validation = select_fusion(
                val_labels[:, index], val_base[:, index], val_motion[:, index]
            )
            fused_test = (1 - alpha) * test_base[:, index] + alpha * test_motion[:, index]
            test = binary_metrics(test_labels[:, index], fused_test, threshold)
            base_threshold, base_validation = best_f1_threshold(val_labels[:, index], val_base[:, index])
            motion_threshold, motion_validation = best_f1_threshold(val_labels[:, index], val_motion[:, index])
            base_test = binary_metrics(test_labels[:, index], test_base[:, index], base_threshold)
            motion_test = binary_metrics(test_labels[:, index], test_motion[:, index], motion_threshold)
            horizons[horizon] = {
                "alpha_motion": alpha, "alpha_base": 1 - alpha, "threshold": threshold,
                "validation_fusion": validation, "test_fusion": test,
                "base_same_protocol": {"threshold": base_threshold, "validation": base_validation, "test": base_test},
                "motion_same_protocol": {"threshold": motion_threshold, "validation": motion_validation, "test": motion_test},
            }
            for row_index, name in enumerate(test_names):
                prediction_rows.append({
                    "fold": fold, "path": name, "horizon": horizon,
                    "label": int(test_labels[row_index, index]),
                    "base_probability": float(test_base[row_index, index]),
                    "motion_probability": float(test_motion[row_index, index]),
                    "fusion_probability": float(fused_test[row_index]),
                    "alpha_motion": alpha, "threshold": threshold,
                    "prediction": int(fused_test[row_index] >= threshold),
                })
        fold_results.append({"fold": fold, "horizons": horizons})

    aggregate = {}
    for horizon in HORIZONS:
        aggregate[horizon] = {}
        for route_key, result_key in (
            ("fusion", "test_fusion"), ("base_same_protocol", "base_same_protocol"),
            ("motion_same_protocol", "motion_same_protocol"),
        ):
            aggregate[horizon][route_key] = {
                metric: summarize([
                    float(
                        fold["horizons"][horizon][result_key][metric]
                        if result_key == "test_fusion"
                        else fold["horizons"][horizon][result_key]["test"][metric]
                    )
                    for fold in fold_results
                ])
                for metric in ("precision", "recall", "f1", "balanced_accuracy", "pr_auc")
            }
        aggregate[horizon]["selected_motion_alphas"] = [
            fold["horizons"][horizon]["alpha_motion"] for fold in fold_results
        ]

    summary = {
        "protocol": "Per-horizon alpha and F1 threshold selected on validation only; test used once",
        "alpha_grid": ALPHAS.tolist(), "folds": fold_results, "four_fold": aggregate,
    }
    (args.output / "fusion_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (args.output / "test_predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(prediction_rows[0])); writer.writeheader(); writer.writerows(prediction_rows)
    print(json.dumps({"four_fold": aggregate}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
