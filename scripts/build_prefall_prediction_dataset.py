from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np

try:
    from .build_gcn_tensor import sequence_normalize
    from .build_sliding_window_dataset import load_fall_annotations, read_rows, write_csv
    from .extract_full_video_rtmpose import cache_name
except ImportError:
    from build_gcn_tensor import sequence_normalize
    from build_sliding_window_dataset import load_fall_annotations, read_rows, write_csv
    from extract_full_video_rtmpose import cache_name


PROJECT = Path(__file__).resolve().parent.parent
DEFAULT_HORIZONS = (1.0, 2.0, 3.0)


def prediction_labels(
    end_frame: int,
    fall_onset_frame: int | None,
    fps: float,
    horizons: tuple[float, ...] = DEFAULT_HORIZONS,
) -> tuple[tuple[int, ...], float | None] | None:
    """Label a strictly pre-onset window; return None if it sees onset/future frames."""
    if fall_onset_frame is None:
        return tuple(0 for _ in horizons), None
    lead_frames = fall_onset_frame - end_frame
    if lead_frames <= 0:
        return None
    lead_seconds = lead_frames / fps
    return tuple(int(lead_seconds <= horizon + 1e-9) for horizon in horizons), lead_seconds


def risk_stage(labels: tuple[int, ...], is_fall_video: bool) -> str:
    if not is_fall_video:
        return "ADL"
    for index, label in enumerate(labels):
        if label:
            lower = 0 if index == 0 else int(DEFAULT_HORIZONS[index - 1])
            upper = int(DEFAULT_HORIZONS[index])
            return f"PRE_FALL_{lower}_{upper}S"
    return "EARLY_FALL_VIDEO"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=PROJECT / "data/metadata/gmdcsa24.csv")
    parser.add_argument("--video-root", type=Path, default=PROJECT / "data/raw/GMDCSA24")
    parser.add_argument(
        "--pose-dir", type=Path, default=PROJECT / "data/poses/gmdcsa24_rtmpose_full"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT / "data/gcn/gmdcsa24_rtmpose_prefall_w64_s16_h123.npz",
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24_rtmpose_prefall_w64_s16_h123.csv",
    )
    parser.add_argument(
        "--split-output", type=Path, default=PROJECT / "data/splits/gmdcsa24_prefall_loso"
    )
    parser.add_argument("--window-frames", type=int, default=64)
    parser.add_argument("--stride-frames", type=int, default=16)
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--subjects", type=int, nargs="+")
    parser.add_argument("--skip-splits", action="store_true")
    parser.add_argument(
        "--fold-count", type=int,
        help="Number of generic group folds; set to the subject count for true LOSO",
    )
    parser.add_argument(
        "--onset-column",
        help="Read fall onset seconds directly from this manifest column instead of dataset annotations",
    )
    parser.add_argument(
        "--onset-frame-column",
        help="Read the fall onset frame directly from this manifest column (preferred for frame annotations)",
    )
    args = parser.parse_args()

    rows = read_rows(args.manifest)
    if args.subjects:
        selected_subjects = set(args.subjects)
        rows = [row for row in rows if int(row["subject"]) in selected_subjects]
    annotations = (
        {} if args.onset_column or args.onset_frame_column
        else load_fall_annotations(args.video_root)
    )
    samples: list[np.ndarray] = []
    output_rows: list[dict[str, object]] = []
    excluded_at_or_after_onset = 0

    for number, row in enumerate(rows, 1):
        cache_path = args.pose_dir / cache_name(row["path"])
        if not cache_path.is_file():
            raise FileNotFoundError(f"Missing full-video pose cache: {cache_path}")
        with np.load(cache_path) as cache:
            poses = cache["keypoints"].astype(np.float32)
            image_size = cache["image_size"]
            fps = float(cache["fps"])

        is_fall_video = int(row["label"]) == 1
        if args.onset_frame_column:
            onset_value = row.get(args.onset_frame_column, "")
            onset_frame = int(float(onset_value)) if onset_value else None
            if is_fall_video and onset_frame is None:
                raise RuntimeError(f"Fall onset missing from {args.onset_frame_column}: {row['path']}")
            onset_seconds = onset_frame / fps if onset_frame is not None else None
        elif args.onset_column:
            onset_value = row.get(args.onset_column, "")
            onset_seconds = float(onset_value) if onset_value else None
            if is_fall_video and onset_seconds is None:
                raise RuntimeError(f"Fall onset missing from {args.onset_column}: {row['path']}")
            onset_frame = int(round(onset_seconds * fps)) if onset_seconds is not None else None
        else:
            fall_interval = annotations.get(row["path"])
            if is_fall_video and fall_interval is None:
                raise RuntimeError(f"Fall annotation missing: {row['path']}")
            onset_seconds = fall_interval[0] if fall_interval else None
            onset_frame = int(round(onset_seconds * fps)) if onset_seconds is not None else None

        for start in range(0, len(poses) - args.window_frames + 1, args.stride_frames):
            end = start + args.window_frames - 1
            result = prediction_labels(end, onset_frame, fps)
            if result is None:
                excluded_at_or_after_onset += 1
                continue
            labels, lead_seconds = result
            window = poses[start : end + 1]
            samples.append(sequence_normalize(window, image_size, args.confidence_threshold))
            name = f"{row['path']}#f{start}-{end}"
            valid_ratio = float(
                np.mean(np.max(window[:, :, 2], axis=1) >= args.confidence_threshold)
            )
            output_rows.append(
                {
                    "path": name,
                    "video_path": row["path"],
                    "subject": row["subject"],
                    "dataset": row["dataset"],
                    "video_label": int(is_fall_video),
                    "start_frame": start,
                    "end_frame": end,
                    "start_seconds": f"{start / fps:.6f}",
                    "end_seconds": f"{end / fps:.6f}",
                    "fall_onset_seconds": "" if onset_seconds is None else f"{onset_seconds:.6f}",
                    "lead_seconds": "" if lead_seconds is None else f"{lead_seconds:.6f}",
                    "y_1s": labels[0],
                    "y_2s": labels[1],
                    "y_3s": labels[2],
                    "stage": risk_stage(labels, is_fall_video),
                    "pose_valid_ratio": f"{valid_ratio:.6f}",
                }
            )
        print(f"[{number}/{len(rows)}] {row['path']}", flush=True)

    data = np.stack(samples).astype(np.float32)
    labels = np.asarray(
        [[int(row[f"y_{int(horizon)}s"]) for horizon in DEFAULT_HORIZONS] for row in output_rows],
        dtype=np.float32,
    )
    names = np.asarray([str(row["path"]) for row in output_rows])
    subjects = np.asarray([str(row["subject"]) for row in output_rows])
    lead_seconds = np.asarray(
        [np.nan if row["lead_seconds"] == "" else float(row["lead_seconds"]) for row in output_rows],
        dtype=np.float32,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        data=data,
        labels=labels,
        names=names,
        subjects=subjects,
        lead_seconds=lead_seconds,
        horizons=np.asarray(DEFAULT_HORIZONS, dtype=np.float32),
    )
    write_csv(args.output_manifest, output_rows)

    unique_subjects = sorted({str(row["subject"]) for row in output_rows})
    if args.skip_splits:
        fold_subjects = {}
    elif len(unique_subjects) == 4 and set(unique_subjects) == {"1", "2", "3", "4"}:
        fold_subjects = {
            1: {"train": {"3", "4"}, "val": {"2"}, "test": {"1"}},
            2: {"train": {"1", "4"}, "val": {"3"}, "test": {"2"}},
            3: {"train": {"1", "2"}, "val": {"4"}, "test": {"3"}},
            4: {"train": {"2", "3"}, "val": {"1"}, "test": {"4"}},
        }
    else:
        # Generic leave-one-group-out folds. Groups may be scenarios when true
        # subject identities are unavailable; callers must document this limitation.
        fold_count = args.fold_count or min(4, len(unique_subjects))
        if fold_count < 2 or fold_count > len(unique_subjects):
            raise RuntimeError(
                f"fold count must be in [2, {len(unique_subjects)}], got {fold_count}"
            )
        chunks = [set(unique_subjects[index::fold_count]) for index in range(fold_count)]
        fold_subjects = {}
        for index in range(fold_count):
            test = chunks[index]
            val = chunks[(index + 1) % fold_count]
            train = set(unique_subjects) - test - val
            fold_subjects[index + 1] = {"train": train, "val": val, "test": test}
    split_summary: dict[str, object] = {}
    for fold, split_subjects in fold_subjects.items():
        split_summary[str(fold)] = {}
        for split, selected_subjects in split_subjects.items():
            selected = [row for row in output_rows if str(row["subject"]) in selected_subjects]
            split_rows = [
                {
                    "path": row["path"],
                    "subject": row["subject"],
                    "y_1s": row["y_1s"],
                    "y_2s": row["y_2s"],
                    "y_3s": row["y_3s"],
                }
                for row in selected
            ]
            write_csv(args.split_output / f"fold_{fold}" / f"{split}.csv", split_rows)
            split_summary[str(fold)][split] = {
                "samples": len(selected),
                "positives": {
                    f"{int(horizon)}s": sum(int(row[f"y_{int(horizon)}s"]) for row in selected)
                    for horizon in DEFAULT_HORIZONS
                },
                "subjects": sorted(selected_subjects),
            }

    monotonic = bool(np.all(labels[:, 0] <= labels[:, 1]) and np.all(labels[:, 1] <= labels[:, 2]))
    fall_rows = [row for row in output_rows if int(row["video_label"]) == 1]
    strictly_pre_onset = all(float(row["lead_seconds"]) > 0 for row in fall_rows)
    summary = {
        "shape": list(data.shape),
        "windows": len(output_rows),
        "horizons_seconds": list(DEFAULT_HORIZONS),
        "positives": {
            f"{int(horizon)}s": int(np.sum(labels[:, index]))
            for index, horizon in enumerate(DEFAULT_HORIZONS)
        },
        "stages": dict(Counter(str(row["stage"]) for row in output_rows)),
        "excluded_at_or_after_onset": excluded_at_or_after_onset,
        "window_frames": args.window_frames,
        "stride_frames": args.stride_frames,
        "finite": bool(np.all(np.isfinite(data))),
        "checks": {
            "nested_labels_y1_le_y2_le_y3": monotonic,
            "all_fall_windows_strictly_pre_onset": strictly_pre_onset,
        },
        "splits": split_summary,
    }
    args.output_manifest.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
