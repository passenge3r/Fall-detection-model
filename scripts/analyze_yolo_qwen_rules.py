"""Evaluate hard-decision YOLO-ST-GCN++/Qwen fusion rules."""

from __future__ import annotations

import csv
import argparse
import json
import sys
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))
from evaluate_qwen3vl_binary import metrics  # noqa: E402


def read(paths: list[Path]) -> dict[str, tuple[int, int]]:
    result = {}
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                result[row["path"]] = (int(row["label"]), int(row["prediction"]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skeleton-root", type=Path, default=PROJECT / "results/benchmark_e300_full/yolo_stgcnpp")
    parser.add_argument("--qwen-root", type=Path, default=PROJECT / "results/qwen3vl_binary/fullvideo_temporal8_reparsed")
    parser.add_argument("--output", type=Path, default=PROJECT / "results/qwen3vl_binary/yolo_stgcnpp_rule_fusion_summary.json")
    args = parser.parse_args()
    skeleton = read(sorted(args.skeleton_root.glob("fold_*/test_predictions.csv")))
    qwen_root = args.qwen_root
    qwen = read([qwen_root / "predictions_reparsed.csv"])
    names = sorted(skeleton)
    labels = np.asarray([skeleton[name][0] for name in names])
    sk = np.asarray([skeleton[name][1] for name in names]); qw = np.asarray([qwen[name][1] for name in names])
    summary = {
        "skeleton_only": metrics(labels, sk),
        "qwen_only": metrics(labels, qw),
        "both_confirm_intersection": metrics(labels, sk & qw),
        "safety_union": metrics(labels, sk | qw),
        "tier_counts": {
            "level_1_both_confirm": int(np.sum((sk == 1) & (qw == 1))),
            "level_2_skeleton_only_review": int(np.sum((sk == 1) & (qw == 0))),
            "level_2_qwen_only_review": int(np.sum((sk == 0) & (qw == 1))),
            "no_alert": int(np.sum((sk == 0) & (qw == 0))),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
