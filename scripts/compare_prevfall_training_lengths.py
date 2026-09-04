"""Compare the 20-epoch screening run with the 300-epoch PreVFall run."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


PROJECT = Path(__file__).resolve().parent.parent
RUNS = {
    "20 epochs (batch 32)": PROJECT / "outputs/prefall_prevfall_loso9_smoke",
    "300 epochs (batch 128)": PROJECT / "outputs/prevfall_rtmpose_stgcnpp_300e_b128",
}
OUTPUT = PROJECT / "reports/prevfall_20e_vs_300e"
METRICS = (
    ("mean_balanced_accuracy", "Balanced Accuracy"),
    ("mean_f1", "Macro-F1"),
    ("mean_pr_auc", "PR-AUC"),
)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for run, root in RUNS.items():
        for fold in range(1, 10):
            payload = json.loads((root / f"fold_{fold}" / "metrics.json").read_text(encoding="utf-8"))
            test = payload["test"]
            row: dict[str, object] = {"run": run, "fold": fold, "best_epoch": payload["best_epoch"]}
            row.update({key: float(test[key]) for key, _ in METRICS})
            rows.append(row)

    with (OUTPUT / "fold_comparison.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    summary: dict[str, object] = {}
    for run in RUNS:
        selected = [row for row in rows if row["run"] == run]
        summary[run] = {
            "best_epoch": {
                "median": float(np.median([row["best_epoch"] for row in selected])),
                "min": int(min(row["best_epoch"] for row in selected)),
                "max": int(max(row["best_epoch"] for row in selected)),
            },
            **{
                key: {
                    "mean": float(np.mean([row[key] for row in selected])),
                    "std": float(np.std([row[key] for row in selected], ddof=1)),
                }
                for key, _ in METRICS
            },
        }
    short = summary["20 epochs (batch 32)"]
    long = summary["300 epochs (batch 128)"]
    summary["300e_minus_20e"] = {
        key: float(long[key]["mean"] - short[key]["mean"]) for key, _ in METRICS
    }
    (OUTPUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    figure, axes = plt.subplots(1, 3, figsize=(14, 4.3), constrained_layout=True)
    x = np.arange(1, 10)
    for axis, (key, title) in zip(axes, METRICS, strict=True):
        for run in RUNS:
            values = [row[key] for row in rows if row["run"] == run]
            axis.plot(x, values, marker="o", linewidth=1.8, label=run)
        axis.set(title=title, xlabel="LOSO test fold", xticks=x, ylim=(0, 1.02))
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Test score")
    axes[-1].legend(fontsize=8, loc="lower right")
    figure.savefig(OUTPUT / "fold_metric_comparison.png", dpi=180)
    plt.close(figure)


if __name__ == "__main__":
    main()
