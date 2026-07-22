from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


VIDEO_PATTERN = re.compile(r"Subject (?P<subject>\d+)[\\/](?P<class>ADL|Fall)[\\/](?P<file>.+\.mp4)$")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["path", "label", "subject", "dataset"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--metadata-out", type=Path, required=True)
    parser.add_argument("--splits-out", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for video in sorted(args.root.rglob("*.mp4")):
        relative = video.relative_to(args.root).as_posix()
        match = VIDEO_PATTERN.match(relative)
        if not match:
            raise RuntimeError(f"Unexpected GMDCSA24 path: {relative}")
        rows.append(
            {
                "path": relative,
                "label": "1" if match.group("class") == "Fall" else "0",
                "subject": match.group("subject"),
                "dataset": "gmdcsa24",
            }
        )

    write_csv(args.metadata_out, rows)
    subjects = sorted({int(row["subject"]) for row in rows})
    audit = {"videos": len(rows), "subjects": subjects, "folds": {}}
    for test_subject in subjects:
        val_subject = subjects[test_subject % len(subjects)]
        split_rows = {"train": [], "val": [], "test": []}
        for row in rows:
            subject = int(row["subject"])
            split = "test" if subject == test_subject else "val" if subject == val_subject else "train"
            split_rows[split].append(row)
        fold_dir = args.splits_out / f"fold_{test_subject}"
        for split, selected in split_rows.items():
            write_csv(fold_dir / f"{split}.csv", selected)
        audit["folds"][str(test_subject)] = {
            split: {
                "items": len(selected),
                "subjects": sorted({int(row["subject"]) for row in selected}),
                "labels": dict(sorted(Counter(row["label"] for row in selected).items())),
            }
            for split, selected in split_rows.items()
        }

    audit_path = args.splits_out / "audit.json"
    audit_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(audit_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
