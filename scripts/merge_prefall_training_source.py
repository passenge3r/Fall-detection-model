"""Append an external pre-fall dataset to training only, preserving primary validation/test."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def read_names(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


def write_names(path: Path, names: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path"])
        writer.writerows([[name] for name in names])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary-data", type=Path, required=True)
    parser.add_argument("--supplement-data", type=Path, required=True)
    parser.add_argument("--primary-splits", type=Path, required=True)
    parser.add_argument("--output-data", type=Path, required=True)
    parser.add_argument("--output-splits", type=Path, required=True)
    args = parser.parse_args()

    with np.load(args.primary_data) as package:
        primary = {key: package[key] for key in package.files}
    with np.load(args.supplement_data) as package:
        supplement = {key: package[key] for key in package.files}
    if primary["data"].shape[1:] != supplement["data"].shape[1:]:
        raise RuntimeError(f"Tensor shape mismatch: {primary['data'].shape} vs {supplement['data'].shape}")
    duplicate_names = set(map(str, primary["names"])) & set(map(str, supplement["names"]))
    if duplicate_names:
        raise RuntimeError(f"Duplicate sample names across sources: {sorted(duplicate_names)[:3]}")

    merged = {
        "data": np.concatenate((primary["data"], supplement["data"])),
        "labels": np.concatenate((primary["labels"], supplement["labels"])),
        "names": np.concatenate((primary["names"], supplement["names"])),
        "subjects": np.concatenate((
            np.asarray([f"gmd_{value}" for value in primary["subjects"]]),
            np.asarray([f"mcfd_scenario_{value}" for value in supplement["subjects"]]),
        )),
        "lead_seconds": np.concatenate((primary["lead_seconds"], supplement["lead_seconds"])),
        "horizons": primary["horizons"],
    }
    args.output_data.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output_data, **merged)

    supplemental_names = list(map(str, supplement["names"]))
    split_summary = {}
    for fold in range(1, 5):
        source = args.primary_splits / f"fold_{fold}"
        train = read_names(source / "train.csv") + supplemental_names
        val = read_names(source / "val.csv")
        test = read_names(source / "test.csv")
        destination = args.output_splits / f"fold_{fold}"
        write_names(destination / "train.csv", train)
        write_names(destination / "val.csv", val)
        write_names(destination / "test.csv", test)
        split_summary[str(fold)] = {
            "train": len(train), "validation": len(val), "test": len(test),
            "supplemental_train_only": len(supplemental_names),
        }
    summary = {
        "primary_samples": len(primary["names"]),
        "supplement_samples": len(supplement["names"]),
        "merged_samples": len(merged["names"]),
        "validation_test_contain_supplement": False,
        "splits": split_summary,
    }
    args.output_data.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
