"""Extract frozen V-JEPA 2.1-B video features from a project manifest.

The script deliberately stores one mean-pooled embedding per video. It is a
reproducible first-stage probe, not a trained fall classifier. The cached
features can later be used by a linear probe or fused with ST-GCN++ features.
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
# Pin remote modeling code and converted weights for reproducibility.
DEFAULT_REVISION = "ea7765861aa689985c593727725afa378fc87492"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--frames", type=int, default=16)
    parser.add_argument(
        "--max-samples",
        type=int,
        default=0,
        help="Balanced pilot size; 0 processes the complete manifest.",
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", choices=("float16", "float32"), default="float16")
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face network access; default is reproducible offline cache loading.",
    )
    return parser.parse_args()


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"path", "label", "subject"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Manifest must contain {sorted(required)}: {path}")
    return rows


def balanced_prefix(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    if limit <= 0 or limit >= len(rows):
        return rows
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["label"]].append(row)
    labels = sorted(grouped)
    chosen: list[dict[str, str]] = []
    cursor = 0
    while len(chosen) < limit:
        label = labels[cursor % len(labels)]
        index = cursor // len(labels)
        if index < len(grouped[label]):
            chosen.append(grouped[label][index])
        if all(index + 1 >= len(grouped[item]) for item in labels):
            break
        cursor += 1
    return chosen


def decode_uniform_rgb(path: Path, num_frames: int) -> list[np.ndarray]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    declared = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if declared <= 0:
        capture.release()
        raise RuntimeError(f"Video reports no frames: {path}")

    targets = np.linspace(0, declared - 1, num_frames).round().astype(int)
    positions: dict[int, list[int]] = defaultdict(list)
    for output_index, frame_index in enumerate(targets.tolist()):
        positions[frame_index].append(output_index)
    frames: list[np.ndarray | None] = [None] * num_frames
    last_rgb: np.ndarray | None = None
    index = 0
    last_target = int(targets[-1])
    while index <= last_target:
        ok, frame = capture.read()
        if not ok:
            break
        if index in positions:
            last_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for output_index in positions[index]:
                frames[output_index] = last_rgb.copy()
        index += 1
    capture.release()

    if last_rgb is None:
        raise RuntimeError(f"No decodable frames: {path}")
    # A few codecs report a slightly optimistic frame count. Repeat the last
    # decoded target instead of silently returning a short tensor.
    for output_index, frame in enumerate(frames):
        if frame is None:
            frames[output_index] = last_rgb.copy()
    return [frame for frame in frames if frame is not None]


def main() -> None:
    args = parse_args()
    if args.frames < 2:
        raise ValueError("--frames must be at least 2")
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")

    rows = balanced_prefix(read_manifest(args.manifest), args.max_samples)
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
    failures: list[dict[str, str]] = []
    timings: list[float] = []

    started = time.perf_counter()
    for position, row in enumerate(rows, start=1):
        video_path = args.video_root / Path(row["path"])
        sample_started = time.perf_counter()
        try:
            frames = decode_uniform_rgb(video_path, args.frames)
            inputs = processor([frames], return_tensors="pt")
            pixel_values = inputs["pixel_values_videos"].to(
                device=args.device, dtype=dtype, non_blocking=True
            )
            with torch.inference_mode():
                output = model(pixel_values_videos=pixel_values, skip_predictor=True)
            pooled = output.last_hidden_state.mean(dim=1).float().cpu().numpy()[0]
            if not np.isfinite(pooled).all():
                raise RuntimeError("Feature contains NaN or Inf")
            features.append(pooled)
            labels.append(int(row["label"]))
            subjects.append(row["subject"])
            paths.append(row["path"])
            elapsed = time.perf_counter() - sample_started
            timings.append(elapsed)
            print(
                f"[{position}/{len(rows)}] label={row['label']} "
                f"shape={pooled.shape} time={elapsed:.2f}s {row['path']}",
                flush=True,
            )
        except Exception as error:  # keep long extraction jobs auditable
            failures.append({"path": row["path"], "error": repr(error)})
            print(f"[{position}/{len(rows)}] FAILED {row['path']}: {error}", flush=True)

    if not features:
        raise RuntimeError(f"All {len(rows)} samples failed")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        features=np.stack(features).astype(np.float16),
        labels=np.asarray(labels, dtype=np.int64),
        subjects=np.asarray(subjects),
        paths=np.asarray(paths),
    )
    peak_gib = (
        torch.cuda.max_memory_allocated(args.device) / (1024**3)
        if args.device.startswith("cuda")
        else 0.0
    )
    summary = {
        "model": args.model,
        "revision": args.revision,
        "dtype": args.dtype,
        "frames_per_video": args.frames,
        "preprocessing": "short-side resize 384, center crop 384, ImageNet normalization",
        "pooling": "mean over final encoder tokens",
        "requested_samples": len(rows),
        "successful_samples": len(features),
        "failed_samples": len(failures),
        "feature_shape": list(np.stack(features).shape),
        "mean_seconds_per_video": float(np.mean(timings)),
        "total_seconds": time.perf_counter() - started,
        "peak_cuda_memory_gib": peak_gib,
        "failures": failures,
    }
    summary_path = args.output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"Saved features: {args.output}")
    print(f"Saved summary:  {summary_path}")


if __name__ == "__main__":
    main()
