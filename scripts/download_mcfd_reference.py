from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import requests
from tqdm import tqdm


BASE_URL = "https://www.iro.umontreal.ca/~labimage/Dataset/chute-zip"


def is_valid_zip(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        with ZipFile(path) as zf:
            return zf.testzip() is None
    except BadZipFile:
        return False


def download_file(url: str, out_path: Path, overwrite: bool = False, position: int = 0) -> str:
    if out_path.exists() and not overwrite and is_valid_zip(out_path):
        return f"skip valid {out_path.name}"
    if out_path.exists() and not overwrite and not is_valid_zip(out_path):
        out_path.unlink()
    tmp_path = out_path.with_suffix(out_path.suffix + ".part")
    if tmp_path.exists():
        tmp_path.unlink()
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with tmp_path.open("wb") as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=out_path.name,
            position=position,
            leave=False,
        ) as pbar:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    tmp_path.rename(out_path)
    if not is_valid_zip(out_path):
        out_path.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded file is not a valid ZIP: {out_path}")
    return f"downloaded {out_path.name}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="data/raw/MCFD/chute-zip")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    links = [f"{BASE_URL}/chute{i:02d}.zip" for i in range(1, 25)]
    print(f"Found {len(links)} MCFD scenario archives.")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(download_file, url, out_dir / Path(url).name, args.overwrite, i % args.workers): url
            for i, url in enumerate(links)
        }
        for future in as_completed(futures):
            print(future.result())
    print(f"Downloaded MCFD archives to {out_dir}")


if __name__ == "__main__":
    main()
