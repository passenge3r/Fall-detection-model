"""Extract frozen V-JEPA 2.1 features for five-class GMDCSA24 segments."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoModel, AutoVideoProcessor

from extract_vjepa21_suspicious_window_features import (
    DEFAULT_MODEL,
    DEFAULT_REVISION,
    decode_span_rgb,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=project / "data/metadata/gmdcsa24_posture5_segments.csv",
    )
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/GMDCSA24")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--frames", type=int, default=16)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", choices=("float16", "float32"), default="float16")
    parser.add_argument("--allow-download", action="store_true")
    args = parser.parse_args()

    rows = read_csv(args.manifest)
    dtype = torch.float16 if args.dtype == "float16" else torch.float32
    processor = AutoVideoProcessor.from_pretrained(
        args.model, revision=args.revision, trust_remote_code=True,
        local_files_only=not args.allow_download,
    )
    model = AutoModel.from_pretrained(
        args.model, revision=args.revision, trust_remote_code=True, dtype=dtype,
        attn_implementation="sdpa", local_files_only=not args.allow_download,
    ).eval().to(args.device)
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    if args.device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats(args.device)

    features: list[np.ndarray] = []
    labels: list[int] = []
    subjects: list[str] = []
    paths: list[str] = []
    class_names: list[str] = []
    timings: list[float] = []
    started = time.perf_counter()
    for position, row in enumerate(rows, 1):
        sample_started = time.perf_counter()
        video_path = args.video_root / row["video_path"]
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        capture.release()
        if fps <= 0:
            raise RuntimeError(f"Invalid FPS: {video_path}")
        start = int(round(float(row["start_seconds"]) * fps))
        end = max(start, int(round(float(row["end_seconds"]) * fps)) - 1)
        frames = decode_span_rgb(video_path, start, end, args.frames)
        inputs = processor([frames], return_tensors="pt")
        pixel_values = inputs["pixel_values_videos"].to(
            device=args.device, dtype=dtype, non_blocking=True
        )
        with torch.inference_mode():
            output = model(pixel_values_videos=pixel_values, skip_predictor=True)
        pooled = output.last_hidden_state.mean(dim=1).float().cpu().numpy()[0]
        if not np.isfinite(pooled).all():
            raise RuntimeError(f"Non-finite feature: {row['segment_id']}")
        features.append(pooled)
        labels.append(int(row["label"]))
        subjects.append(row["subject"])
        paths.append(row["segment_id"])
        class_names.append(row["class_name"])
        elapsed = time.perf_counter() - sample_started
        timings.append(elapsed)
        print(
            f"[{position}/{len(rows)}] {row['class_name']} "
            f"t={row['start_seconds']}-{row['end_seconds']} {row['video_path']} {elapsed:.2f}s",
            flush=True,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    array = np.stack(features).astype(np.float16)
    np.savez_compressed(
        args.output,
        features=array,
        labels=np.asarray(labels, dtype=np.int64),
        subjects=np.asarray(subjects),
        paths=np.asarray(paths),
        class_names=np.asarray(class_names),
    )
    summary = {
        "model": args.model,
        "revision": args.revision,
        "samples": len(rows),
        "feature_shape": list(array.shape),
        "frames_per_segment": args.frames,
        "mean_seconds_per_segment": float(np.mean(timings)),
        "total_seconds": time.perf_counter() - started,
        "peak_cuda_memory_gib": (
            torch.cuda.max_memory_allocated(args.device) / (1024**3)
            if args.device.startswith("cuda") else 0.0
        ),
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
