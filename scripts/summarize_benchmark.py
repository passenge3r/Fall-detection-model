from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


METRICS = ("accuracy", "precision", "recall", "specificity", "f1", "balanced_accuracy")


def binary_metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))
    safe = lambda a, b: float(a / b) if b else 0.0
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    precision = safe(tp, tp + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)), "precision": precision,
        "recall": recall, "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report: dict[str, object] = {}
    table: list[dict[str, object]] = []
    for route_dir in sorted(path for path in args.results.iterdir() if path.is_dir()):
        folds = []
        prediction_rows = []
        for fold in range(1, 5):
            fold_dir = route_dir / f"fold_{fold}"
            metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
            folds.append(metrics)
            with (fold_dir / "test_predictions.csv").open("r", encoding="utf-8-sig", newline="") as handle:
                prediction_rows.extend(csv.DictReader(handle))
        labels = np.asarray([int(row["label"]) for row in prediction_rows])
        predictions = np.asarray([int(row["prediction"]) for row in prediction_rows])
        pooled = binary_metrics(labels, predictions)
        fold_statistics = {
            metric: {
                "mean": float(np.mean([fold["test"][metric] for fold in folds])),
                "std": float(np.std([fold["test"][metric] for fold in folds], ddof=1)),
            }
            for metric in METRICS
        }
        route = folds[0]["route"]
        entry = {
            "route": route,
            "folds": [{"fold": fold["fold"], **fold["test"]} for fold in folds],
            "fold_statistics": fold_statistics,
            "pooled_test": pooled,
            "parameters": folds[0]["parameters"],
            "latency_ms_batch1_mean": float(np.mean([fold["latency_ms_batch1"] for fold in folds])),
            "test_samples": len(prediction_rows),
        }
        report[route] = entry
        table.append({
            "route": route,
            **{metric: pooled[metric] for metric in METRICS},
            "tp": pooled["tp"], "tn": pooled["tn"], "fp": pooled["fp"], "fn": pooled["fn"],
            "parameters": entry["parameters"],
            "latency_ms_batch1": entry["latency_ms_batch1_mean"],
        })
    table.sort(key=lambda row: float(row["balanced_accuracy"]), reverse=True)
    ranked = []
    previous_ba: float | None = None
    previous_rank = 0
    for position, row in enumerate(table, 1):
        current_ba = float(row["balanced_accuracy"])
        rank = previous_rank if previous_ba is not None and np.isclose(current_ba, previous_ba) else position
        ranked.append({"rank": rank, **row})
        previous_ba, previous_rank = current_ba, rank
    table = ranked
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.output.with_suffix(".csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    print(json.dumps(table, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
