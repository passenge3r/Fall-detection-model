"""Inspect a remote ZIP central directory using HTTP byte-range requests."""

from __future__ import annotations

import argparse
import csv
import json
import struct
import urllib.request
from collections import Counter
from pathlib import Path, PurePosixPath


def get_range(url: str, start: int, end: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "fall-benchmark/0.1", "Range": f"bytes={start}-{end}"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        if response.status != 206:
            raise RuntimeError(f"Expected HTTP 206, received {response.status}")
        return response.read()


def zip64_values(extra: bytes) -> list[int]:
    cursor = 0
    while cursor + 4 <= len(extra):
        field_id, field_size = struct.unpack_from("<HH", extra, cursor)
        cursor += 4
        payload = extra[cursor : cursor + field_size]
        cursor += field_size
        if field_id == 0x0001:
            return [value[0] for value in struct.iter_unpack("<Q", payload[: len(payload) // 8 * 8])]
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("size", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tail_size = min(args.size, 256 * 1024)
    tail_start = args.size - tail_size
    tail = get_range(args.url, tail_start, args.size - 1)
    eocd_at = tail.rfind(b"PK\x05\x06")
    if eocd_at < 0:
        raise RuntimeError("End-of-central-directory record not found")
    eocd = struct.unpack_from("<4s4H2LH", tail, eocd_at)
    entries, cd_size, cd_offset = eocd[4], eocd[5], eocd[6]

    if entries == 0xFFFF or cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        locator_at = tail.rfind(b"PK\x06\x07", 0, eocd_at)
        if locator_at < 0:
            raise RuntimeError("ZIP64 locator not found")
        _, _, zip64_offset, _ = struct.unpack_from("<4sLQL", tail, locator_at)
        zip64 = get_range(args.url, zip64_offset, zip64_offset + 55)
        record = struct.unpack_from("<4sQ2H2L4Q", zip64)
        entries, cd_size, cd_offset = record[7], record[8], record[9]

    directory = get_range(args.url, cd_offset, cd_offset + cd_size - 1)
    rows = []
    cursor = 0
    while cursor + 46 <= len(directory):
        fixed = struct.unpack_from("<4s6H3L5H2L", directory, cursor)
        if fixed[0] != b"PK\x01\x02":
            break
        flags, method = fixed[3], fixed[4]
        compressed, uncompressed = fixed[8], fixed[9]
        name_len, extra_len, comment_len = fixed[10], fixed[11], fixed[12]
        local_offset = fixed[16]
        start = cursor + 46
        name_bytes = directory[start : start + name_len]
        extra = directory[start + name_len : start + name_len + extra_len]
        encoding = "utf-8" if flags & 0x800 else "cp437"
        name = name_bytes.decode(encoding, errors="replace")
        values = iter(zip64_values(extra))
        if uncompressed == 0xFFFFFFFF:
            uncompressed = next(values)
        if compressed == 0xFFFFFFFF:
            compressed = next(values)
        if local_offset == 0xFFFFFFFF:
            local_offset = next(values)
        rows.append(
            {
                "path": name,
                "extension": PurePosixPath(name).suffix.lower(),
                "method": method,
                "crc32": f"{fixed[7]:08x}",
                "compressed_size": compressed,
                "uncompressed_size": uncompressed,
                "local_header_offset": local_offset,
            }
        )
        cursor += 46 + name_len + extra_len + comment_len

    if len(rows) != entries:
        raise RuntimeError(f"Parsed {len(rows)} entries, central directory reports {entries}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    extensions = Counter()
    for row in rows:
        item = extensions[row["extension"]]
        extensions[row["extension"]] = (
            item[0] + 1 if isinstance(item, tuple) else 1,
            item[1] + row["compressed_size"] if isinstance(item, tuple) else row["compressed_size"],
        )
    summary = {
        "entries": len(rows),
        "central_directory_bytes": cd_size,
        "extensions": {
            extension or "<none>": {"files": count, "compressed_bytes": size}
            for extension, (count, size) in extensions.most_common()
        },
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
