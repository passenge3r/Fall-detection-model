"""Zero-shot Qwen3-VL fall recognition on annotated MCFD segments."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

PROMPT = """The frames are ordered from earliest to latest and show one short activity segment.
Answer FALL only if the person visibly undergoes an uncontrolled or abrupt downward
transition toward the floor. Answer SAFE for walking, standing, sitting, bending,
intentional lying, or already lying without a visible fall. Respond with exactly one
word: FALL or SAFE."""


def read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def frames(path: Path, start: int, end: int, count: int, output: Path) -> list[str]:
    capture = cv2.VideoCapture(str(path)); targets = np.linspace(start, end, count).round().astype(int)
    positions: dict[int, list[int]] = defaultdict(list)
    for index, target in enumerate(targets.tolist()): positions[target].append(index)
    result: list[Path | None] = [None] * count; capture.set(cv2.CAP_PROP_POS_FRAMES, start); last = None
    for frame_index in range(start, end + 1):
        ok, frame = capture.read()
        if not ok: break
        if frame_index in positions:
            last = frame
            for index in positions[frame_index]:
                target = output / f"frame_{index:02d}.jpg"; cv2.imwrite(str(target), frame); result[index] = target
    capture.release()
    if last is None: raise RuntimeError(f"No frame: {path} [{start},{end}]")
    for index, item in enumerate(result):
        if item is None:
            target = output / f"frame_{index:02d}.jpg"; cv2.imwrite(str(target), last); result[index] = target
    return [str(item.resolve()) for item in result if item is not None]


def metric(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    tp = int(np.sum((labels == 1) & (predictions == 1))); tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1))); fn = int(np.sum((labels == 1) & (predictions == 0)))
    safe = lambda a, b: float(a / b) if b else 0.0
    precision = safe(tp, tp + fp); recall = safe(tp, tp + fn); specificity = safe(tn, tn + fp)
    return {"samples": len(labels), "accuracy": safe(tp + tn, len(labels)), "balanced_accuracy": (recall + specificity) / 2,
            "precision": precision, "recall": recall, "specificity": specificity,
            "f1": safe(2 * precision * recall, precision + recall), "tp": tp, "tn": tn, "fp": fp, "fn": fn}


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=project / "data/metadata/mcfd_segments.csv")
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/MCFD/kaggle")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=8); parser.add_argument("--max-pixels", type=int, default=65536)
    parser.add_argument("--cameras", nargs="+", default=["1", "2", "4", "5", "6", "7", "8"])
    parser.add_argument("--device", default="cuda"); parser.add_argument("--allow-download", action="store_true")
    args = parser.parse_args(); args.output_root.mkdir(parents=True, exist_ok=True)
    selected = [row for row in read(args.manifest) if row["cam"] in set(args.cameras)]
    processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-2B-Instruct", local_files_only=not args.allow_download)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen3-VL-2B-Instruct", dtype=torch.bfloat16, attn_implementation="sdpa",
        local_files_only=not args.allow_download).eval().to(args.device)
    output_rows = []; started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="qwen_mcfd_") as temporary:
        root = Path(temporary)
        for position, row in enumerate(selected, 1):
            folder = root / f"sample_{position:04d}"; folder.mkdir(); start = int(row["start_frame"]); end = int(row["end_frame"])
            paths = frames(args.video_root / row["path"], start, end, args.frames, folder)
            messages = [{"role": "user", "content": [
                {"type": "video", "video": paths, "sample_fps": 8, "min_pixels": 4096, "max_pixels": args.max_pixels},
                {"type": "text", "text": PROMPT}]}]
            inputs = processor.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                                   return_dict=True, return_tensors="pt", do_sample_frames=False).to(args.device)
            sample_started = time.perf_counter()
            with torch.inference_mode(): generated = model.generate(**inputs, max_new_tokens=4, do_sample=False)
            raw = processor.batch_decode(generated[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)[0].strip()
            upper = raw.upper(); prediction = 1 if "FALL" in upper and "SAFE" not in upper else (0 if "SAFE" in upper else -1)
            elapsed = time.perf_counter() - sample_started; name = f"{row['path']}#f{start}-{end}"
            output_rows.append({"sample": name, "camera": row["cam"], "label": int(row["label"]),
                                "prediction": prediction, "raw_output": raw, "seconds": elapsed})
            if position == 1 or position % 25 == 0:
                print(f"[{position}/{len(selected)}] y={row['label']} pred={prediction} {elapsed:.2f}s", flush=True)
    with (args.output_root / "predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0])); writer.writeheader(); writer.writerows(output_rows)
    labels = np.asarray([row["label"] for row in output_rows]); predictions = np.asarray([row["prediction"] for row in output_rows])
    cameras = np.asarray([row["camera"] for row in output_rows]); masks = {"all_selected": np.ones(len(labels), dtype=bool),
        "cam1": cameras == "1", "cross_view_test": np.isin(cameras, ["2", "4", "5", "6", "7", "8"])}
    summary = {"protocol": "zero-shot Qwen, annotated 31-frame segments, cameras 1/2/4/5/6/7/8",
               "frames": args.frames, "parse_errors": int(np.sum(predictions < 0)),
               "mean_inference_seconds": float(np.mean([row["seconds"] for row in output_rows])),
               "total_seconds": time.perf_counter() - started,
               "metrics": {name: metric(labels[mask], predictions[mask]) for name, mask in masks.items()}}
    (args.output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
