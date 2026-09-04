from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parent.parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a leakage-safe hard-negative ablation from out-of-fold predictions. "
            "Validation and test splits remain unchanged."
        )
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=PROJECT / "data/gcn/gmdcsa24_rtmpose_sliding_w64_s16.npz",
    )
    parser.add_argument(
        "--splits",
        type=Path,
        default=PROJECT / "data/splits/gmdcsa24_sliding_loso",
    )
    parser.add_argument(
        "--predictions-root",
        type=Path,
        default=PROJECT / "results/sliding_window_e300_b64/rtmpose_stgcnpp",
    )
    parser.add_argument(
        "--output-data",
        type=Path,
        default=PROJECT / "data/gcn/gmdcsa24_rtmpose_sliding_hardneg_w64_s16.npz",
    )
    parser.add_argument(
        "--output-splits",
        type=Path,
        default=PROJECT / "data/splits/gmdcsa24_sliding_hardneg_loso",
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_hardneg.csv",
    )
    parser.add_argument("--threshold", type=float, default=0.8)
    parser.add_argument(
        "--extra-copies",
        type=int,
        default=2,
        help="Extra training-only copies of each hard negative per eligible fold",
    )
    args = parser.parse_args()

    if not 0 <= args.threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    if args.extra_copies < 1:
        raise ValueError("extra-copies must be at least 1")

    with np.load(args.data) as package:
        data = package["data"].astype(np.float32)
        labels = package["labels"].astype(np.int64)
        names = package["names"].astype(str)
        subjects = package["subjects"].astype(str)
        cameras = package["cameras"].astype(str)
    lookup = {name: index for index, name in enumerate(names)}

    # Each subject is evaluated by exactly one held-out fold. These predictions
    # are therefore out-of-fold and are safe for ranking difficult samples.
    oof: dict[str, float] = {}
    source_fold: dict[str, int] = {}
    for fold in range(1, 5):
        prediction_path = args.predictions_root / f"fold_{fold}" / "test_predictions.csv"
        for row in read_csv(prediction_path):
            if int(row["label"]) != 0:
                continue
            probability = float(row["fall_probability"])
            if probability < args.threshold:
                continue
            name = row["path"]
            if name not in lookup:
                raise RuntimeError(f"Prediction absent from data archive: {name}")
            if name in oof:
                raise RuntimeError(f"Duplicate out-of-fold prediction: {name}")
            oof[name] = probability
            source_fold[name] = fold

    all_data = [data]
    all_labels = [labels]
    all_names = [names]
    all_subjects = [subjects]
    all_cameras = [cameras]
    manifest_rows: list[dict[str, object]] = []
    split_summary: dict[str, object] = {}

    for target_fold in range(1, 5):
        fold_dir = args.splits / f"fold_{target_fold}"
        split_rows = {split: read_csv(fold_dir / f"{split}.csv") for split in ("train", "val", "test")}
        train_names = {row["path"] for row in split_rows["train"]}
        val_names = {row["path"] for row in split_rows["val"]}
        test_names = {row["path"] for row in split_rows["test"]}
        if train_names & val_names or train_names & test_names or val_names & test_names:
            raise RuntimeError(f"Original split overlap in fold {target_fold}")

        selected = sorted(name for name in oof if name in train_names)
        augmented_train = list(split_rows["train"])
        for source_name in selected:
            index = lookup[source_name]
            for repeat in range(1, args.extra_copies + 1):
                duplicate_name = f"{source_name}#hardneg-f{target_fold}-r{repeat}"
                all_data.append(data[index : index + 1])
                all_labels.append(labels[index : index + 1])
                all_names.append(np.asarray([duplicate_name]))
                all_subjects.append(subjects[index : index + 1])
                all_cameras.append(cameras[index : index + 1])
                augmented_train.append(
                    {"path": duplicate_name, "label": "0", "subject": subjects[index]}
                )
                manifest_rows.append(
                    {
                        "path": duplicate_name,
                        "source_path": source_name,
                        "subject": subjects[index],
                        "target_fold": target_fold,
                        "source_oof_fold": source_fold[source_name],
                        "oof_fall_probability": f"{oof[source_name]:.8f}",
                        "repeat": repeat,
                    }
                )

        output_fold = args.output_splits / f"fold_{target_fold}"
        write_csv(output_fold / "train.csv", augmented_train, ["path", "label", "subject"])
        write_csv(output_fold / "val.csv", split_rows["val"], ["path", "label", "subject"])
        write_csv(output_fold / "test.csv", split_rows["test"], ["path", "label", "subject"])
        split_summary[str(target_fold)] = {
            "original_train": len(split_rows["train"]),
            "hard_negative_sources": len(selected),
            "extra_training_samples": len(selected) * args.extra_copies,
            "augmented_train": len(augmented_train),
            "validation_unchanged": len(split_rows["val"]),
            "test_unchanged": len(split_rows["test"]),
            "hard_negative_subjects": dict(Counter(str(subjects[lookup[name]]) for name in selected)),
        }

    args.output_data.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output_data,
        data=np.concatenate(all_data),
        labels=np.concatenate(all_labels),
        names=np.concatenate(all_names),
        subjects=np.concatenate(all_subjects),
        cameras=np.concatenate(all_cameras),
    )
    write_csv(
        args.output_manifest,
        manifest_rows,
        [
            "path", "source_path", "subject", "target_fold", "source_oof_fold",
            "oof_fall_probability", "repeat",
        ],
    )
    summary = {
        "method": "out-of-fold hard-negative oversampling",
        "threshold": args.threshold,
        "extra_copies": args.extra_copies,
        "unique_hard_negative_sources": len(oof),
        "original_samples": len(data),
        "output_samples": int(sum(len(part) for part in all_data)),
        "leakage_rule": "duplicates are training-only; validation and test rows are unchanged",
        "folds": split_summary,
    }
    summary_path = args.output_manifest.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
