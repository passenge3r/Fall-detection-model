"""Reparse audited Qwen outputs and create LOSO prediction folders for fusion."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))
from evaluate_qwen3vl_binary import metrics, parse_output  # noqa: E402


def read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qwen-csv", type=Path, required=True)
    parser.add_argument("--splits", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    source = read(args.qwen_csv); repaired = []
    for row in source:
        prediction, probability = parse_output(row["raw_output"])
        repaired.append({"path": row["path"], "label": int(row["label"]), "prediction": prediction,
                         "fall_probability": probability, "raw_output": row["raw_output"], "seconds": row["seconds"]})
    write(args.output_root / "predictions_reparsed.csv", repaired)
    by_path = {str(row["path"]): row for row in repaired}
    for fold in range(1, 5):
        for split in ("val", "test"):
            names = [row["path"] for row in read(args.splits / f"fold_{fold}" / f"{split}.csv")]
            selected = [{key: by_path[name][key] for key in ("path", "label", "prediction", "fall_probability")} for name in names]
            write(args.output_root / f"fold_{fold}" / f"{split}_predictions.csv", selected)
    labels = np.asarray([row["label"] for row in repaired]); predictions = np.asarray([row["prediction"] for row in repaired])
    summary = {"protocol": "Qwen3-VL zero-shot, audited placeholder reparsing", "samples": len(repaired),
               "parse_errors": int(np.sum(predictions < 0)), "metrics": metrics(labels, predictions)}
    (args.output_root / "summary_reparsed.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
