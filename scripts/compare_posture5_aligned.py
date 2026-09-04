"""Compare all posture routes on the exact Qwen balanced-50 segment IDs."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))
from train_vjepa21_posture5_probe import multiclass_metrics  # noqa: E402


def read_predictions(files: list[Path]) -> dict[str, tuple[int, int]]:
    rows: dict[str, tuple[int, int]] = {}
    for file in files:
        with file.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                rows[row["segment_id"]] = (int(row["label"]), int(row["prediction"]))
    return rows


def main() -> None:
    qwen_file = PROJECT / "results/posture5/qwen3vl2b_zero_shot_balanced50/predictions.csv"
    qwen = read_predictions([qwen_file])
    routes = {
        "RTMPose + compact graph-temporal (300 epochs)": read_predictions(
            sorted((PROJECT / "results/posture5/rtmpose_compact_tgcn_e300").glob("fold_*/test_predictions.csv"))
        ),
        "V-JEPA 2.1-B + linear probe (300 epochs)": read_predictions(
            sorted((PROJECT / "results/posture5/vjepa21b_linear_probe_e300").glob("fold_*/test_predictions.csv"))
        ),
        "Qwen3-VL-2B direct-video zero-shot": qwen,
    }
    identifiers = list(qwen)
    result = {
        "protocol": "exact same balanced 50 segments selected for the Qwen pilot; 10 per class",
        "sample_count": len(identifiers),
        "routes": {},
    }
    for name, predictions in routes.items():
        missing = [identifier for identifier in identifiers if identifier not in predictions]
        if missing:
            raise RuntimeError(f"{name} is missing {len(missing)} aligned segments")
        labels = [predictions[identifier][0] for identifier in identifiers]
        outputs = [predictions[identifier][1] for identifier in identifiers]
        result["routes"][name] = multiclass_metrics(np.asarray(labels), np.asarray(outputs))
    output = PROJECT / "results/posture5/aligned_balanced50_comparison.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
