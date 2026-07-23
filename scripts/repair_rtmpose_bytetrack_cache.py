from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parent.parent


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_cache(raw_path: str, project_root: Path) -> Path:
    path = Path(raw_path)
    candidates = (path, project_root / path, project_root.parent / path)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"Cannot resolve pose cache: {raw_path}")


def pose_valid(pose: np.ndarray, threshold: float) -> bool:
    return bool(np.any(pose[:, 2] >= threshold))


def interpolate_short_gaps(
    poses: np.ndarray,
    sources: np.ndarray,
    frame_indices: np.ndarray,
    threshold: float,
    max_source_gap: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Fill only bounded missing runs whose total source-frame span is short."""
    repaired = poses.copy()
    repaired_sources = sources.copy()
    valid = np.asarray([pose_valid(pose, threshold) for pose in repaired])
    cursor = 0
    while cursor < len(repaired):
        if valid[cursor]:
            cursor += 1
            continue
        start = cursor
        while cursor < len(repaired) and not valid[cursor]:
            cursor += 1
        end = cursor - 1
        left = start - 1
        right = cursor
        if left < 0 or right >= len(repaired):
            continue
        source_span = int(frame_indices[right] - frame_indices[left])
        if source_span > max_source_gap:
            continue
        denominator = float(frame_indices[right] - frame_indices[left])
        if denominator <= 0:
            continue
        for index in range(start, end + 1):
            alpha = float(frame_indices[index] - frame_indices[left]) / denominator
            repaired[index] = (
                (1.0 - alpha) * repaired[left] + alpha * repaired[right]
            )
            repaired_sources[index] = 2
            valid[index] = True
    return repaired, repaired_sources


def repair_sequence(
    tracked: np.ndarray,
    fallback: np.ndarray,
    frame_indices: np.ndarray,
    threshold: float = 0.2,
    max_source_gap: int = 12,
) -> tuple[np.ndarray, np.ndarray]:
    """Prefer tracked poses, fall back to same-frame RTMPose, then interpolate."""
    if tracked.shape != fallback.shape or tracked.shape[1:] != (17, 3):
        raise ValueError(
            f"Expected matching [T,17,3] arrays, got {tracked.shape} and {fallback.shape}"
        )
    if len(frame_indices) != len(tracked):
        raise ValueError("frame_indices length does not match pose sequence")
    repaired = tracked.copy()
    # 0=tracked, 1=untracked RTMPose fallback, 2=interpolated, 3=still missing.
    sources = np.full(len(tracked), 3, dtype=np.uint8)
    for index in range(len(repaired)):
        if pose_valid(tracked[index], threshold):
            sources[index] = 0
        elif pose_valid(fallback[index], threshold):
            repaired[index] = fallback[index]
            sources[index] = 1
    return interpolate_short_gaps(
        repaired,
        sources,
        frame_indices,
        threshold,
        max_source_gap,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tracked-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_bytetrack_t64.csv",
    )
    parser.add_argument(
        "--fallback-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_t64.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT / "data/poses/gmdcsa24_rtmpose_bytetrack_v2_t64",
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_bytetrack_v2_t64.csv",
    )
    parser.add_argument("--project-root", type=Path, default=PROJECT)
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--max-source-gap", type=int, default=12)
    args = parser.parse_args()

    tracked_rows = read_rows(args.tracked_manifest)
    fallback_by_path = {
        row["path"]: row for row in read_rows(args.fallback_manifest)
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_rows: list[dict[str, str]] = []
    totals = {
        "tracked_frames": 0,
        "fallback_frames": 0,
        "interpolated_frames": 0,
        "remaining_zero_frames": 0,
    }

    for number, tracked_row in enumerate(tracked_rows, 1):
        path = tracked_row["path"]
        fallback_row = fallback_by_path.get(path)
        if fallback_row is None:
            raise RuntimeError(f"Fallback pose missing from manifest: {path}")
        tracked_path = resolve_cache(tracked_row["pose_path"], args.project_root)
        fallback_path = resolve_cache(fallback_row["pose_path"], args.project_root)
        with np.load(tracked_path) as tracked_cache:
            tracked = tracked_cache["keypoints"].astype(np.float32)
            tracked_indices = tracked_cache["frame_indices"].astype(np.int32)
            copied = {
                key: tracked_cache[key]
                for key in tracked_cache.files
                if key not in {"keypoints", "repair_source"}
            }
        with np.load(fallback_path) as fallback_cache:
            fallback = fallback_cache["keypoints"].astype(np.float32)
            fallback_indices = fallback_cache["frame_indices"].astype(np.int32)
        if not np.array_equal(tracked_indices, fallback_indices):
            raise RuntimeError(f"Frame indices do not match: {path}")
        repaired, sources = repair_sequence(
            tracked,
            fallback,
            tracked_indices,
            args.confidence_threshold,
            args.max_source_gap,
        )
        output_path = args.output_dir / tracked_path.name
        np.savez_compressed(
            output_path,
            keypoints=repaired,
            repair_source=sources,
            **copied,
        )
        counts = {
            "tracked_frames": int(np.sum(sources == 0)),
            "fallback_frames": int(np.sum(sources == 1)),
            "interpolated_frames": int(np.sum(sources == 2)),
            "remaining_zero_frames": int(np.sum(sources == 3)),
        }
        for key, value in counts.items():
            totals[key] += value
        confidence = repaired[:, :, 2]
        output_rows.append(
            {
                **tracked_row,
                "pose_path": output_path.relative_to(PROJECT).as_posix(),
                "backend": "rtmpose_bytetrack_v2",
                "zero_pose_frames": str(counts["remaining_zero_frames"]),
                "mean_confidence": f"{float(np.mean(confidence)):.6f}",
                **{key: str(value) for key, value in counts.items()},
            }
        )
        print(
            f"[{number}/{len(tracked_rows)}] {path} "
            f"fallback={counts['fallback_frames']} missing={counts['remaining_zero_frames']}",
            flush=True,
        )

    with args.output_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    label_summary: dict[str, dict[str, float | int]] = {}
    for label, name in (("0", "adl"), ("1", "fall")):
        rows = [row for row in output_rows if row["label"] == label]
        total_frames = len(rows) * int(rows[0]["frames"])
        missing = sum(int(row["remaining_zero_frames"]) for row in rows)
        label_summary[name] = {
            "clips": len(rows),
            "frames": total_frames,
            "remaining_zero_frames": missing,
            "zero_rate": missing / total_frames,
            "fallback_frames": sum(int(row["fallback_frames"]) for row in rows),
            "interpolated_frames": sum(
                int(row["interpolated_frames"]) for row in rows
            ),
        }
    summary = {
        "videos": len(output_rows),
        "strategy": (
            "tracked pose -> same-frame untracked RTMPose fallback "
            "-> bounded short-gap interpolation"
        ),
        "repair_source": {
            "0": "tracked",
            "1": "untracked_rtmpose_fallback",
            "2": "interpolated",
            "3": "missing",
        },
        **totals,
        "by_label": label_summary,
    }
    summary_path = args.output_manifest.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
