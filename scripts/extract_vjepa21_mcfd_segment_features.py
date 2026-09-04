"""Extract frozen V-JEPA 2.1 features for annotated MCFD frame segments."""

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

MODEL = "apiantonio/vjepa2.1-vit-base-384"
REVISION = "ea7765861aa689985c593727725afa378fc87492"


def read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def decode(path: Path, start: int, end: int, count: int) -> list[np.ndarray]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open {path}")
    targets = np.linspace(start, end, count).round().astype(int)
    positions: dict[int, list[int]] = defaultdict(list)
    for index, frame in enumerate(targets.tolist()):
        positions[frame].append(index)
    frames: list[np.ndarray | None] = [None] * count
    capture.set(cv2.CAP_PROP_POS_FRAMES, start); last = None
    for frame_index in range(start, end + 1):
        ok, frame = capture.read()
        if not ok:
            break
        if frame_index in positions:
            last = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            for index in positions[frame_index]:
                frames[index] = last.copy()
    capture.release()
    if last is None:
        raise RuntimeError(f"No frames decoded: {path} [{start},{end}]")
    return [frame if frame is not None else last.copy() for frame in frames]


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=project / "data/metadata/mcfd_segments.csv")
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/MCFD/kaggle")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=16)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--allow-download", action="store_true")
    args = parser.parse_args(); rows = read(args.manifest)
    processor = AutoVideoProcessor.from_pretrained(MODEL, revision=REVISION, trust_remote_code=True,
                                                    local_files_only=not args.allow_download)
    model = AutoModel.from_pretrained(MODEL, revision=REVISION, trust_remote_code=True, dtype=torch.float16,
                                      attn_implementation="sdpa", local_files_only=not args.allow_download).eval().to(args.device)
    for parameter in model.parameters(): parameter.requires_grad_(False)
    features = []; labels = []; names = []; cameras = []; timings = []; started = time.perf_counter()
    for position, row in enumerate(rows, 1):
        sample_started = time.perf_counter(); start = int(row["start_frame"]); end = int(row["end_frame"])
        frames = decode(args.video_root / row["path"], start, end, args.frames)
        pixel = processor([frames], return_tensors="pt")["pixel_values_videos"].to(args.device, dtype=torch.float16)
        with torch.inference_mode():
            output = model(pixel_values_videos=pixel, skip_predictor=True)
        pooled = output.last_hidden_state.mean(1).float().cpu().numpy()[0]
        features.append(pooled); labels.append(int(row["label"])); cameras.append(str(row["cam"]))
        names.append(f"{row['path']}#f{start}-{end}"); timings.append(time.perf_counter() - sample_started)
        if position == 1 or position % 25 == 0:
            print(f"[{position}/{len(rows)}] {names[-1]} {timings[-1]:.2f}s", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output, features=np.stack(features).astype(np.float16), labels=np.asarray(labels),
                        names=np.asarray(names), cameras=np.asarray(cameras))
    summary = {"model": MODEL, "revision": REVISION, "samples": len(rows), "frames_per_segment": args.frames,
               "feature_shape": list(np.stack(features).shape), "mean_seconds": float(np.mean(timings)),
               "total_seconds": time.perf_counter() - started}
    args.output.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
