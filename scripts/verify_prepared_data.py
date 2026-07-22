from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_gmdcsa(root: Path, manifest_path: Path, splits_root: Path) -> dict:
    manifest = read_csv(manifest_path)
    missing = [row["path"] for row in manifest if not (root / row["path"]).is_file()]
    empty = [row["path"] for row in manifest if (root / row["path"]).is_file() and (root / row["path"]).stat().st_size == 0]
    split_errors = []
    for fold in sorted(splits_root.glob("fold_*")):
        sets = {name: {row["path"] for row in read_csv(fold / f"{name}.csv")} for name in ("train", "val", "test")}
        if sets["train"] & sets["val"] or sets["train"] & sets["test"] or sets["val"] & sets["test"]:
            split_errors.append(f"{fold.name}: path overlap")
        if set().union(*sets.values()) != {row["path"] for row in manifest}:
            split_errors.append(f"{fold.name}: does not cover manifest")
    return {
        "manifest_rows": len(manifest),
        "missing_videos": missing,
        "empty_videos": empty,
        "split_errors": split_errors,
        "ok": len(manifest) == 160 and not missing and not empty and not split_errors,
    }


def verify_mcfd_archive(path: Path) -> dict:
    if not path.exists():
        return {"status": "not_started"}
    try:
        with ZipFile(path) as archive:
            bad = archive.testzip()
            video_count = sum(name.lower().endswith(".avi") for name in archive.namelist())
        return {"status": "complete", "bad_member": bad, "avi_files": video_count, "ok": bad is None and video_count == 192}
    except BadZipFile:
        return {"status": "downloading_or_invalid", "bytes": path.stat().st_size, "ok": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    project = args.project
    report = {
        "gmdcsa24": verify_gmdcsa(
            project / "data/raw/GMDCSA24",
            project / "data/metadata/gmdcsa24.csv",
            project / "data/splits/gmdcsa24_loso",
        ),
        "mcfd": verify_mcfd_archive(project / "data/raw/MCFD/mcfd_kaggle.zip"),
    }
    output = project / "data/metadata/preparation_status.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
