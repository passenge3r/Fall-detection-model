"""Extract V-JEPA 2.1 features from pose-selected suspicious video windows.

The temporal selector is an out-of-fold sliding-window ST-GCN++ model: every
video is scored only by the fold where its subject was held out.  This keeps
test labels out of window selection while focusing the RGB encoder on the
interval that the skeleton branch considers most fall-like.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoModel, AutoVideoProcessor


DEFAULT_MODEL = "apiantonio/vjepa2.1-vit-base-384"
DEFAULT_REVISION = "ea7765861aa689985c593727725afa378fc87492"


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--window-manifest",
        type=Path,
        default=project / "data/metadata/gmdcsa24_rtmpose_sliding_w64_s16.csv",
    )
    parser.add_argument(
        "--prediction-root",
        type=Path,
        default=project / "results/sliding_window_e300_b64/rtmpose_stgcnpp",
    )
    parser.add_argument(
        "--video-root", type=Path, default=project / "data/raw/GMDCSA24"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--frames", type=int, default=16)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", choices=("float16", "float32"), default="float16")
    parser.add_argument("--allow-download", action="store_true")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def select_oof_windows(
    manifest_path: Path, prediction_root: Path
) -> list[dict[str, str | float]]:
    manifest = {row["path"]: row for row in read_csv(manifest_path)}
    predictions: list[dict[str, str]] = []
    for fold in range(1, 5):
        path = prediction_root / f"fold_{fold}" / "test_predictions.csv"
        if not path.is_file():
            raise FileNotFoundError(path)
        predictions.extend(read_csv(path))

    best: dict[str, dict[str, str | float]] = {}
    for prediction in predictions:
        window_name = prediction["path"]
        if window_name not in manifest:
            raise KeyError(f"Prediction is missing from window manifest: {window_name}")
        row = manifest[window_name]
        video_path = row["video_path"]
        score = float(prediction["fall_probability"])
        if video_path not in best or score > float(best[video_path]["selector_score"]):
            best[video_path] = {**row, "selector_score": score}

    subjects = {str(row["subject"]) for row in best.values()}
    if subjects != {"1", "2", "3", "4"}:
        raise RuntimeError(f"Unexpected selected subjects: {sorted(subjects)}")
    return sorted(best.values(), key=lambda row: str(row["video_path"]))


def decode_span_rgb(
    path: Path, start_frame: int, end_frame: int, num_frames: int
) -> list[np.ndarray]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    declared = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if declared <= 0:
        capture.release()
        raise RuntimeError(f"Video reports no frames: {path}")
    start_frame = max(0, min(start_frame, declared - 1))
    end_frame = max(start_frame, min(end_frame, declared - 1))
    targets = np.linspace(start_frame, end_frame, num_frames).round().astype(int)
    positions: dict[int, list[int]] = defaultdict(list)
    for output_index, frame_index in enumerate(targets.tolist()):
        positions[frame_index].append(output_index)
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames: list[np.ndarray | None] = [None] * num_frames
    last_rgb: np.ndarray | None = None
    for frame_index in range(start_frame, end_frame + 1):
        ok, frame = capture.read()
        if not ok:
            break
        if frame_index in positions:
            last_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for output_index in positions[frame_index]:
                frames[output_index] = last_rgb.copy()
    capture.release()
    if last_rgb is None:
        raise RuntimeError(f"No decodable frames in [{start_frame}, {end_frame}]: {path}")
    for index, frame in enumerate(frames):
        if frame is None:
            frames[index] = last_rgb.copy()
    return [frame for frame in frames if frame is not None]


def main() -> None:
    args = parse_args()
    if args.frames < 2:
        raise ValueError("--frames must be at least 2")
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    selected = select_oof_windows(args.window_manifest, args.prediction_root)
    dtype = torch.float16 if args.dtype == "float16" else torch.float32
    processor = AutoVideoProcessor.from_pretrained(
        args.model,
        revision=args.revision,
        trust_remote_code=True,
        local_files_only=not args.allow_download,
    )
    model = AutoModel.from_pretrained(
        args.model,
        revision=args.revision,
        trust_remote_code=True,
        dtype=dtype,
        attn_implementation="sdpa",
        local_files_only=not args.allow_download,
    ).eval().to(args.device)
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    if args.device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats(args.device)

    features: list[np.ndarray] = []
    labels: list[int] = []
    subjects: list[str] = []
    paths: list[str] = []
    selection_rows: list[dict[str, str | float]] = []
    timings: list[float] = []
    started = time.perf_counter()
    for position, row in enumerate(selected, 1):
        sample_started = time.perf_counter()
        video_path = args.video_root / str(row["video_path"])
        frames = decode_span_rgb(
            video_path, int(str(row["start_frame"])), int(str(row["end_frame"])), args.frames
        )
        inputs = processor([frames], return_tensors="pt")
        pixel_values = inputs["pixel_values_videos"].to(
            device=args.device, dtype=dtype, non_blocking=True
        )
        with torch.inference_mode():
            output = model(pixel_values_videos=pixel_values, skip_predictor=True)
        pooled = output.last_hidden_state.mean(dim=1).float().cpu().numpy()[0]
        if not np.isfinite(pooled).all():
            raise RuntimeError(f"Non-finite feature: {video_path}")
        features.append(pooled)
        labels.append(int(str(row["label"])))
        subjects.append(str(row["subject"]))
        paths.append(str(row["video_path"]))
        elapsed = time.perf_counter() - sample_started
        timings.append(elapsed)
        selection_rows.append(row)
        print(
            f"[{position}/{len(selected)}] p={float(row['selector_score']):.4f} "
            f"f{row['start_frame']}-{row['end_frame']} {row['video_path']} {elapsed:.2f}s",
            flush=True,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    feature_array = np.stack(features).astype(np.float16)
    np.savez_compressed(
        args.output,
        features=feature_array,
        labels=np.asarray(labels, dtype=np.int64),
        subjects=np.asarray(subjects),
        paths=np.asarray(paths),
    )
    selection_path = args.output.with_suffix(".selection.csv")
    with selection_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selection_rows[0]))
        writer.writeheader()
        writer.writerows(selection_rows)
    summary = {
        "model": args.model,
        "revision": args.revision,
        "selector": "out-of-fold RTMPose + ST-GCN++ maximum-probability 64-frame window",
        "selector_predictions": str(args.prediction_root),
        "samples": len(features),
        "feature_shape": list(feature_array.shape),
        "frames_per_window": args.frames,
        "mean_seconds_per_video": float(np.mean(timings)),
        "total_seconds": time.perf_counter() - started,
        "peak_cuda_memory_gib": (
            torch.cuda.max_memory_allocated(args.device) / (1024**3)
            if args.device.startswith("cuda")
            else 0.0
        ),
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
