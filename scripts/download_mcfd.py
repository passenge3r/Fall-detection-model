from __future__ import annotations

import argparse
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from zipfile import BadZipFile, ZipFile


BASE_URL = "https://www.iro.umontreal.ca/~labimage/Dataset/chute-zip"
USER_AGENT = "Mozilla/5.0 fall-benchmark-dataset-preparation/1.0"


def is_valid_zip(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        with ZipFile(path) as archive:
            return archive.testzip() is None
    except BadZipFile:
        return False


def download_one(index: int, output_dir: Path) -> str:
    name = f"chute{index:02d}.zip"
    target = output_dir / name
    if is_valid_zip(target):
        return f"skip valid {name} ({target.stat().st_size / 1024**2:.1f} MiB)"

    partial = target.with_suffix(".zip.part")
    partial.unlink(missing_ok=True)
    request = urllib.request.Request(
        f"{BASE_URL}/{name}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as handle:
        shutil.copyfileobj(response, handle, length=1024 * 1024)
    partial.replace(target)
    if not is_valid_zip(target):
        target.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded file is not a valid ZIP: {name}")
    return f"downloaded {name} ({target.stat().st_size / 1024**2:.1f} MiB)"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(download_one, i, output_dir): i for i in range(1, 25)}
        for future in as_completed(futures):
            index = futures[future]
            try:
                print(future.result(), flush=True)
            except Exception as exc:  # keep other downloads running
                failures.append(f"chute{index:02d}.zip: {exc}")
                print(f"FAILED chute{index:02d}.zip: {exc}", flush=True)

    valid = sum(is_valid_zip(output_dir / f"chute{i:02d}.zip") for i in range(1, 25))
    print(f"valid archives: {valid}/24", flush=True)
    if failures or valid != 24:
        raise SystemExit("\n".join(failures) or "Not all archives are valid")


if __name__ == "__main__":
    main()
