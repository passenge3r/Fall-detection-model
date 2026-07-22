from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


UPFALL_VAL_SUBJECTS = {11}
UPFALL_TEST_SUBJECTS = {2, 4, 15, 16}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["path", "label", "start", "end", "subject", "cam", "dataset"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def split_upfall(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    output = {"train": [], "val": [], "test": []}
    for row in rows:
        subject = int(row["subject"])
        if subject in UPFALL_TEST_SUBJECTS:
            split = "test"
        elif subject in UPFALL_VAL_SUBJECTS:
            split = "val"
        else:
            split = "train"
        output[split].append(row)
    return output


def split_mcfd(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    # Cross-view evaluation: cam1 train, cam3 validation, all remaining cameras test.
    output = {"train": [], "val": [], "test": []}
    for row in rows:
        camera = int(row["cam"])
        split = "train" if camera == 1 else "val" if camera == 3 else "test"
        output[split].append(row)
    return output


def audit(splits: dict[str, list[dict[str, str]]], group_field: str) -> dict:
    path_sets = {name: {row["path"] for row in rows} for name, rows in splits.items()}
    group_sets = {
        name: {int(row[group_field]) for row in rows} for name, rows in splits.items()
    }
    overlaps = {}
    names = list(splits)
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            overlaps[f"{left}_{right}_path_overlap"] = len(path_sets[left] & path_sets[right])
            overlaps[f"{left}_{right}_{group_field}_overlap"] = sorted(
                group_sets[left] & group_sets[right]
            )
    return {
        "items": {name: len(rows) for name, rows in splits.items()},
        "groups": {name: sorted(values) for name, values in group_sets.items()},
        "labels": {
            name: dict(sorted(Counter(row["label"] for row in rows).items()))
            for name, rows in splits.items()
        },
        "overlaps": overlaps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    jobs = {
        "up_fall_subject_strict": (
            args.metadata_dir / "omnifall_up_fall.csv",
            split_upfall,
            "subject",
        ),
        "mcfd_cross_view": (
            args.metadata_dir / "omnifall_mcfd.csv",
            split_mcfd,
            "cam",
        ),
    }
    summary = {}
    for protocol, (source, splitter, group_field) in jobs.items():
        splits = splitter(load_rows(source))
        protocol_dir = args.out_dir / protocol
        for split, rows in splits.items():
            write_rows(protocol_dir / f"{split}.csv", rows)
        summary[protocol] = audit(splits, group_field)

    summary_path = args.out_dir / "split_audit.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
