"""List or download selected external pre-fall datasets reproducibly.

The default action is metadata-only. Large payloads require ``--download`` and
can be filtered with ``--include``. Partial files are resumed with HTTP Range.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import shutil
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
PREVFALL_ARTICLE_ID = 26488216
PREVFALL_API = f"https://api.figshare.com/v2/articles/{PREVFALL_ARTICLE_ID}"
OMNIFALL_BASE = "https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/main/labels"
OMNIFALL_LABELS = (
    "label2id.csv", "up_fall.csv", "cmdfall.csv", "le2i.csv",
    "caucafall.csv", "edf.csv", "occu.csv", "mcfd.csv", "OOPS.csv",
)


def request_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "fall-benchmark/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        while block := handle.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def download_resumable(
    url: str,
    destination: Path,
    expected_size: int | None = None,
    expected_md5: str | None = None,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": "fall-benchmark/0.1"}
    if offset:
        headers["Range"] = f"bytes={offset}-"
    request = urllib.request.Request(url, headers=headers)
    mode = "ab" if offset else "wb"
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                if offset and response.status != 206:
                    raise RuntimeError(
                        f"Server ignored Range request for {destination.name}; "
                        "refusing to append duplicate bytes"
                    )
                with partial.open(mode) as handle:
                    while block := response.read(1024 * 1024):
                        handle.write(block)
            break
        except (OSError, urllib.error.URLError) as error:
            if attempt == 3:
                raise RuntimeError(f"Download failed after 3 attempts: {url}") from error
            time.sleep(2 ** attempt)
    if expected_size is not None and partial.stat().st_size != expected_size:
        raise RuntimeError(
            f"Size mismatch for {destination.name}: {partial.stat().st_size} != {expected_size}"
        )
    if expected_md5 is not None:
        actual_md5 = md5sum(partial)
        if actual_md5.lower() != expected_md5.lower():
            raise RuntimeError(
                f"MD5 mismatch for {destination.name}: {actual_md5} != {expected_md5}"
            )
    partial.replace(destination)


def download_parallel_resumable(
    url: str,
    destination: Path,
    expected_size: int,
    expected_md5: str | None,
    connections: int,
) -> None:
    """Download independent byte ranges, resume them, then assemble atomically."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    parts_dir = destination.with_suffix(destination.suffix + ".parts")
    parts_dir.mkdir(parents=True, exist_ok=True)
    chunk_size = math.ceil(expected_size / connections)

    legacy_partial = destination.with_suffix(destination.suffix + ".part")
    first_part = parts_dir / "part_000"
    if legacy_partial.exists() and not first_part.exists():
        if legacy_partial.stat().st_size > chunk_size:
            raise RuntimeError("Legacy partial is larger than the first parallel range")
        legacy_partial.replace(first_part)

    ranges = []
    for index in range(connections):
        start = index * chunk_size
        end = min(expected_size - 1, (index + 1) * chunk_size - 1)
        if start <= end:
            ranges.append((index, start, end))

    def fetch_range(spec: tuple[int, int, int]) -> None:
        index, start, end = spec
        part = parts_dir / f"part_{index:03d}"
        expected_part_size = end - start + 1
        for attempt in range(1, 9):
            offset = part.stat().st_size if part.exists() else 0
            if offset == expected_part_size:
                return
            if offset > expected_part_size:
                raise RuntimeError(f"Oversized range part: {part}")
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "fall-benchmark/0.1",
                    "Range": f"bytes={start + offset}-{end}",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=180) as response:
                    if response.status != 206:
                        raise RuntimeError(
                            f"Server ignored range {start + offset}-{end}: {response.status}"
                        )
                    with part.open("ab") as handle:
                        while block := response.read(4 * 1024 * 1024):
                            handle.write(block)
                if part.stat().st_size == expected_part_size:
                    return
            except (OSError, urllib.error.URLError):
                if attempt == 8:
                    raise
                time.sleep(min(30, 2 ** attempt))
        raise RuntimeError(f"Range did not complete: {part}")

    with ThreadPoolExecutor(max_workers=connections) as executor:
        futures = [executor.submit(fetch_range, spec) for spec in ranges]
        while not all(future.done() for future in futures):
            downloaded = sum(
                (parts_dir / f"part_{index:03d}").stat().st_size
                if (parts_dir / f"part_{index:03d}").exists()
                else 0
                for index, _, _ in ranges
            )
            print(
                f"Progress: {downloaded / 1024**3:.3f}/{expected_size / 1024**3:.3f} GiB "
                f"({100 * downloaded / expected_size:.2f}%)",
                flush=True,
            )
            time.sleep(10)
        for future in futures:
            future.result()

    assembling = destination.with_suffix(destination.suffix + ".assembling")
    digest = hashlib.md5()
    with assembling.open("wb") as output:
        for index, _, _ in ranges:
            part = parts_dir / f"part_{index:03d}"
            with part.open("rb") as source:
                while block := source.read(8 * 1024 * 1024):
                    output.write(block)
                    digest.update(block)
    if assembling.stat().st_size != expected_size:
        raise RuntimeError("Assembled file size mismatch")
    actual_md5 = digest.hexdigest()
    if expected_md5 is not None and actual_md5.lower() != expected_md5.lower():
        raise RuntimeError(f"MD5 mismatch: {actual_md5} != {expected_md5}")
    assembling.replace(destination)
    for index, _, _ in ranges:
        (parts_dir / f"part_{index:03d}").unlink()
    parts_dir.rmdir()


def matches(name: str, patterns: list[str]) -> bool:
    return not patterns or any(fnmatch.fnmatch(name.lower(), pattern.lower()) for pattern in patterns)


def handle_prevfall(args: argparse.Namespace) -> None:
    article_url = PREVFALL_API
    if args.version is not None:
        article_url += f"/versions/{args.version}"
    article = request_json(article_url)
    files = article.get("files", [])
    manifest = {
        "dataset": "Pre-VFall",
        "article_id": article.get("id"),
        "requested_version": args.version,
        "title": article.get("title"),
        "license": article.get("license"),
        "version": article.get("version"),
        "files": [
            {key: item.get(key) for key in ("id", "name", "size", "download_url", "computed_md5")}
            for item in files
        ],
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "figshare_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for item in files:
        print(f"{item['name']}\t{item['size'] / 1024**3:.3f} GiB")
    if not args.download:
        print("Metadata saved. Add --download and optional --include patterns to fetch payloads.")
        return
    selected = [item for item in files if matches(item["name"], args.include)]
    total_gb = sum(item["size"] for item in selected) / 1024**3
    if total_gb > args.max_gb:
        raise RuntimeError(f"Selected payload is {total_gb:.2f} GiB, above --max-gb={args.max_gb}")
    for item in selected:
        print(f"Downloading {item['name']} ({item['size'] / 1024**3:.3f} GiB)", flush=True)
        destination = args.output / item["name"]
        if args.connections > 1:
            download_parallel_resumable(
                item["download_url"], destination, item["size"],
                item.get("computed_md5"), args.connections,
            )
        else:
            download_resumable(
                item["download_url"], destination, item["size"],
                item.get("computed_md5"),
            )


def handle_omnifall(args: argparse.Namespace) -> None:
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "dataset": "OmniFall labels",
        "source": "simplexsigil2/omnifall",
        "license": "CC BY-NC 4.0 for benchmark annotations; source videos retain original licenses",
        "files": list(OMNIFALL_LABELS),
    }
    (args.output / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not args.download:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        print("Manifest saved. Add --download to fetch labels.")
        return
    for name in OMNIFALL_LABELS:
        if matches(name, args.include):
            print(f"Downloading {name}", flush=True)
            download_resumable(f"{OMNIFALL_BASE}/{name}", args.output / name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", choices=("prevfall", "omnifall-labels"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--version", type=int, help="Figshare article version (Pre-VFall only)")
    parser.add_argument("--connections", type=int, default=1, choices=range(1, 17))
    parser.add_argument("--include", action="append", default=[], help="case-insensitive glob; repeatable")
    parser.add_argument("--max-gb", type=float, default=25.0)
    args = parser.parse_args()
    if args.output is None:
        args.output = PROJECT / "data/external" / args.dataset.replace("-labels", "_labels")
    if args.dataset == "prevfall":
        handle_prevfall(args)
    else:
        handle_omnifall(args)


if __name__ == "__main__":
    main()
