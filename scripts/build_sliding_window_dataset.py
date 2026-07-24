from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

try:
    from .build_gcn_tensor import sequence_normalize
    from .extract_full_video_rtmpose import cache_name
except ImportError:
    from build_gcn_tensor import sequence_normalize
    from extract_full_video_rtmpose import cache_name


PROJECT = Path(__file__).resolve().parent.parent
FALL_INTERVAL = re.compile(
    r"Fall(?:ing)?[^\[]*\[\s*([0-9.]+)\s*(?:to\s*)?([0-9.]+)\s*\]",
    re.IGNORECASE,
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_fall_interval(text: str) -> tuple[float, float]:
    match = FALL_INTERVAL.search(text)
    if match is None:
        raise ValueError(f"Cannot parse fall interval: {text}")
    start, end = map(float, match.groups())
    if end < start:
        raise ValueError(f"Invalid fall interval [{start}, {end}]: {text}")
    return start, end


def load_fall_annotations(video_root: Path) -> dict[str, tuple[float, float]]:
    annotations: dict[str, tuple[float, float]] = {}
    for subject_dir in sorted(video_root.glob("Subject *")):
        annotation_path = subject_dir / "Fall.csv"
        if not annotation_path.is_file():
            continue
        for row in read_rows(annotation_path):
            classes = next(value for key, value in row.items() if key.strip() == "Classes")
            relative = f"{subject_dir.name}/Fall/{row['File Name']}"
            annotations[relative] = parse_fall_interval(classes)
    return annotations


def window_label(
    start: int,
    end: int,
    fall_onset_frame: int | None,
    min_overlap_frames: int,
) -> int | None:
    if fall_onset_frame is None:
        return 0
    overlap = max(0, end - max(start, fall_onset_frame) + 1)
    if overlap >= min_overlap_frames:
        return 1
    if end < fall_onset_frame:
        return 0
    return None


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24.csv",
    )
    parser.add_argument(
        "--video-root",
        type=Path,
        default=PROJECT / "data/raw/GMDCSA24",
    )
    parser.add_argument(
        "--pose-dir",
        type=Path,
        default=PROJECT / "data/poses/gmdcsa24_rtmpose_full",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT / "data/gcn/gmdcsa24_rtmpose_sliding_w64_s16.npz",
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_sliding_w64_s16.csv",
    )
    parser.add_argument(
        "--split-output",
        type=Path,
        default=PROJECT / "data/splits/gmdcsa24_sliding_loso",
    )
    parser.add_argument("--window-frames", type=int, default=64)
    parser.add_argument("--stride-frames", type=int, default=16)
    parser.add_argument("--min-fall-overlap-seconds", type=float, default=0.5)
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    args = parser.parse_args()

    rows = read_rows(args.manifest)
    annotations = load_fall_annotations(args.video_root)
    samples: list[np.ndarray] = []
    output_rows: list[dict[str, object]] = []
    ignored = 0

    for number, row in enumerate(rows, 1):
        cache_path = args.pose_dir / cache_name(row["path"])
        if not cache_path.is_file():
            raise FileNotFoundError(f"Missing full-video pose cache: {cache_path}")
        with np.load(cache_path) as cache:
            poses = cache["keypoints"].astype(np.float32)
            image_size = cache["image_size"]
            fps = float(cache["fps"])
        fall_interval = annotations.get(row["path"])
        if int(row["label"]) == 1 and fall_interval is None:
            raise RuntimeError(f"Fall annotation missing: {row['path']}")
        onset_seconds = fall_interval[0] if fall_interval else None
        onset_frame = int(round(onset_seconds * fps)) if onset_seconds is not None else None
        min_overlap = max(1, int(round(args.min_fall_overlap_seconds * fps)))
        for start in range(0, len(poses) - args.window_frames + 1, args.stride_frames):
            end = start + args.window_frames - 1
            label = window_label(start, end, onset_frame, min_overlap)
            if label is None:
                ignored += 1
                continue
            window = poses[start : end + 1]
            samples.append(
                sequence_normalize(window, image_size, args.confidence_threshold)
            )
            name = f"{row['path']}#f{start}-{end}"
            valid_ratio = float(
                np.mean(np.max(window[:, :, 2], axis=1) >= args.confidence_threshold)
            )
            output_rows.append(
                {
                    "path": name,
                    "video_path": row["path"],
                    "label": label,
                    "subject": row["subject"],
                    "dataset": row["dataset"],
                    "start_frame": start,
                    "end_frame": end,
                    "start_seconds": f"{start / fps:.6f}",
                    "end_seconds": f"{end / fps:.6f}",
                    "fall_onset_seconds": (
                        "" if onset_seconds is None else f"{onset_seconds:.6f}"
                    ),
                    "pose_valid_ratio": f"{valid_ratio:.6f}",
                }
            )
        print(f"[{number}/{len(rows)}] {row['path']}", flush=True)

    data = np.stack(samples).astype(np.float32)
    labels = np.asarray([int(row["label"]) for row in output_rows], dtype=np.int64)
    names = np.asarray([str(row["path"]) for row in output_rows])
    subjects = np.asarray([str(row["subject"]) for row in output_rows])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        data=data,
        labels=labels,
        names=names,
        subjects=subjects,
        cameras=np.asarray([""] * len(names)),
    )
    write_csv(args.output_manifest, output_rows)

    fold_subjects = {
        1: {"train": {"3", "4"}, "val": {"2"}, "test": {"1"}},
        2: {"train": {"1", "4"}, "val": {"3"}, "test": {"2"}},
        3: {"train": {"1", "2"}, "val": {"4"}, "test": {"3"}},
        4: {"train": {"2", "3"}, "val": {"1"}, "test": {"4"}},
    }
    split_summary: dict[str, object] = {}
    for fold, split_subjects in fold_subjects.items():
        split_summary[str(fold)] = {}
        for split, selected_subjects in split_subjects.items():
            selected_rows = [
                row for row in output_rows if str(row["subject"]) in selected_subjects
            ]
            split_rows = [
                {"path": row["path"], "label": row["label"], "subject": row["subject"]}
                for row in selected_rows
            ]
            write_csv(args.split_output / f"fold_{fold}" / f"{split}.csv", split_rows)
            split_summary[str(fold)][split] = {
                "samples": len(split_rows),
                "labels": dict(Counter(str(row["label"]) for row in split_rows)),
                "subjects": sorted(selected_subjects),
            }

    summary = {
        "shape": list(data.shape),
        "windows": len(output_rows),
        "labels": {
            "adl": int(np.sum(labels == 0)),
            "fall": int(np.sum(labels == 1)),
        },
        "ignored_boundary_windows": ignored,
        "window_frames": args.window_frames,
        "stride_frames": args.stride_frames,
        "min_fall_overlap_seconds": args.min_fall_overlap_seconds,
        "finite": bool(np.all(np.isfinite(data))),
        "splits": split_summary,
    }
    summary_path = args.output_manifest.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
