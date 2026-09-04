"""Selectively extract remote ZIP entries through HTTP range requests."""

from __future__ import annotations

import argparse
import binascii
import csv
import json
import struct
import time
import urllib.error
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath


def request_range(url: str, start: int, end: int):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "fall-benchmark/0.1", "Range": f"bytes={start}-{end}"},
    )
    response = urllib.request.urlopen(request, timeout=180)
    if response.status != 206:
        response.close()
        raise RuntimeError(f"Expected HTTP 206, received {response.status}")
    return response


def crc32_file(path: Path) -> int:
    value = 0
    with path.open("rb") as handle:
        while block := handle.read(8 * 1024 * 1024):
            value = binascii.crc32(block, value)
    return value & 0xFFFFFFFF


def safe_destination(root: Path, archive_path: str) -> Path:
    relative = PurePosixPath(archive_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"Unsafe archive path: {archive_path}")
    return root.joinpath(*relative.parts)


def locate_data(url: str, local_header_offset: int) -> int:
    with request_range(url, local_header_offset, local_header_offset + 65535) as response:
        header = response.read(30)
    values = struct.unpack("<4s5H3L2H", header)
    if values[0] != b"PK\x03\x04":
        raise RuntimeError(f"Invalid local header at {local_header_offset}")
    return local_header_offset + 30 + values[9] + values[10]


def extract_entry(url: str, row: dict[str, str], output: Path) -> dict[str, object]:
    destination = safe_destination(output, row["path"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    compressed_size = int(row["compressed_size"])
    uncompressed_size = int(row["uncompressed_size"])
    expected_crc = int(row["crc32"], 16)
    method = int(row["method"])
    if destination.exists() and destination.stat().st_size == uncompressed_size:
        if crc32_file(destination) == expected_crc:
            return {"path": row["path"], "status": "existing", "bytes": uncompressed_size}

    compressed = destination.with_suffix(destination.suffix + ".compressed.part")
    source_marker = destination.with_suffix(destination.suffix + ".compressed.source")
    if compressed.exists():
        previous_source = (
            source_marker.read_text(encoding="utf-8") if source_marker.exists() else ""
        )
        if previous_source != url:
            compressed.unlink()
    source_marker.write_text(url, encoding="utf-8")
    for attempt in range(1, 9):
        offset = compressed.stat().st_size if compressed.exists() else 0
        if offset == compressed_size:
            break
        try:
            data_start = locate_data(url, int(row["local_header_offset"]))
            with request_range(
                url, data_start + offset, data_start + compressed_size - 1
            ) as response, compressed.open("ab") as handle:
                while block := response.read(4 * 1024 * 1024):
                    handle.write(block)
        except (OSError, urllib.error.URLError):
            if attempt == 8:
                raise
            time.sleep(min(30, 2**attempt))
    if not compressed.exists() or compressed.stat().st_size != compressed_size:
        raise RuntimeError(f"Incomplete entry: {row['path']}")

    temporary = destination.with_suffix(destination.suffix + ".extracting")
    temporary.unlink(missing_ok=True)
    if method == 0:
        compressed.replace(temporary)
    elif method == 8:
        decompressor = zlib.decompressobj(-15)
        with compressed.open("rb") as source, temporary.open("wb") as target:
            while block := source.read(8 * 1024 * 1024):
                target.write(decompressor.decompress(block))
            target.write(decompressor.flush())
        compressed.unlink()
    else:
        raise RuntimeError(f"Unsupported ZIP method {method}: {row['path']}")

    if temporary.stat().st_size != uncompressed_size:
        raise RuntimeError(f"Uncompressed size mismatch: {row['path']}")
    actual_crc = crc32_file(temporary)
    if actual_crc != expected_crc:
        raise RuntimeError(f"CRC mismatch: {row['path']}")
    temporary.replace(destination)
    source_marker.unlink(missing_ok=True)
    return {"path": row["path"], "status": "downloaded", "bytes": uncompressed_size}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extension", action="append", required=True)
    parser.add_argument("--connections", type=int, default=8, choices=range(1, 17))
    args = parser.parse_args()
    selected_extensions = {
        value.lower() if value.startswith(".") else f".{value.lower()}"
        for value in args.extension
    }
    with args.manifest.open("r", encoding="utf-8", newline="") as handle:
        rows = [
            row for row in csv.DictReader(handle)
            if row["extension"].lower() in selected_extensions
        ]
    total = sum(int(row["compressed_size"]) for row in rows)
    print(
        f"Selected {len(rows)} files, {total / 1024**3:.3f} GiB compressed",
        flush=True,
    )
    results = []
    with ThreadPoolExecutor(max_workers=args.connections) as executor:
        futures = {
            executor.submit(extract_entry, args.url, row, args.output): row
            for row in rows
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(f"[{completed}/{len(rows)}] {result['status']}: {result['path']}", flush=True)
    summary = {
        "selected_extensions": sorted(selected_extensions),
        "files": len(results),
        "bytes": sum(int(item["bytes"]) for item in results),
        "downloaded": sum(item["status"] == "downloaded" for item in results),
        "existing": sum(item["status"] == "existing" for item in results),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "selective_extract.summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
