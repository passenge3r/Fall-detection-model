from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

from tqdm import tqdm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-dir", default="data/raw/MCFD/chute-zip")
    parser.add_argument("--out-dir", default="data/raw/MCFD/extracted")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    zip_dir = Path(args.zip_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    archives = sorted(zip_dir.glob("chute*.zip"))
    if not archives:
        raise RuntimeError(f"No MCFD ZIP files found in {zip_dir}")
    for archive in tqdm(archives, desc="extract MCFD"):
        marker = out_dir / archive.stem / ".extracted"
        if marker.exists() and not args.overwrite:
            continue
        with ZipFile(archive) as zf:
            zf.extractall(out_dir)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
    print(f"Extracted {len(archives)} MCFD archives to {out_dir}")


if __name__ == "__main__":
    main()
