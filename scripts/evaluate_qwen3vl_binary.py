"""Zero-shot binary fall review with Qwen3-VL on the complete GMDCSA24 manifest."""

from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration


PROMPT = """Analyze these frames as one ordered video from earliest to latest.
Decide whether the main person performs a FALL during the observed sequence.

Definitions:
- falling: a visible uncontrolled or abrupt downward transition from standing/sitting
  toward the floor or ground, including impact and the immediate aftermath.
- not_falling: walking, standing, sitting, bending, intentional lying down, sleeping,
  exercising, or a person already lying without a visible abrupt fall transition.

Use temporal change, not the last frame alone. Return exactly one JSON object with no
markdown. The class must be the bare label and confidence must be between 0 and 1:
{"class":"falling_or_not_falling","confidence":0.00,"evidence":"brief visible evidence"}
"""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sample_frames(path: Path, count: int, output: Path) -> list[str]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    targets = np.linspace(0, max(total - 1, 0), count).round().astype(int)
    paths = []
    for index, target in enumerate(targets):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(target))
        ok, frame = capture.read()
        if not ok:
            capture.release(); raise RuntimeError(f"Cannot decode frame {target}: {path}")
        frame_path = output / f"frame_{index:02d}.jpg"
        cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        paths.append(str(frame_path.resolve()))
    capture.release()
    return paths


def parse_output(text: str) -> tuple[int, float]:
    label: str | None = None; confidence = 0.5
    try:
        payload = json.loads(text.strip())
        label = str(payload.get("class", "")).strip().lower()
        confidence = float(payload.get("confidence", 0.5))
    except (json.JSONDecodeError, TypeError, ValueError):
        match = re.search(r'"class"\s*:\s*"([a-z_]+)"', text.lower())
        label = match.group(1) if match else None
        score_match = re.search(r'"confidence"\s*:\s*([01](?:\.\d+)?)', text.lower())
        confidence = float(score_match.group(1)) if score_match else 0.5
    confidence = min(max(confidence, 0.0), 1.0)
    if label in {"falling", "falling_or_not_falling"}:
        return 1, confidence
    if label in {"not_falling", "not_falling_or_not_falling"}:
        return 0, 1.0 - confidence
    return -1, 0.5


def metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    tp = int(np.sum((labels == 1) & (predictions == 1))); tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1))); fn = int(np.sum((labels == 1) & (predictions == 0)))
    safe = lambda a, b: float(a / b) if b else 0.0
    precision = safe(tp, tp + fp); recall = safe(tp, tp + fn); specificity = safe(tn, tn + fp)
    return {"accuracy": safe(tp + tn, len(labels)), "precision": precision, "recall": recall,
            "specificity": specificity, "f1": safe(2 * precision * recall, precision + recall),
            "balanced_accuracy": (recall + specificity) / 2, "tp": tp, "tn": tn, "fp": fp, "fn": fn}


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=project / "data/metadata/gmdcsa24.csv")
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/GMDCSA24")
    parser.add_argument("--model", default="Qwen/Qwen3-VL-2B-Instruct")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--max-pixels", type=int, default=128 * 32 * 32)
    parser.add_argument("--max-new-tokens", type=int, default=40)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args(); args.output_root.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.manifest)
    processor = AutoProcessor.from_pretrained(args.model, local_files_only=not args.allow_download)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model, dtype=torch.bfloat16, attn_implementation="sdpa", local_files_only=not args.allow_download,
    ).eval().to(args.device)
    predictions = []; started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="qwen3vl_binary_") as temporary:
        root = Path(temporary)
        for position, row in enumerate(rows, 1):
            sample = root / f"sample_{position:03d}"; sample.mkdir()
            frame_paths = sample_frames(args.video_root / row["path"], args.frames, sample)
            messages = [{"role": "user", "content": [
                {"type": "video", "video": frame_paths, "sample_fps": 2,
                 "min_pixels": 4 * 32 * 32, "max_pixels": args.max_pixels},
                {"type": "text", "text": PROMPT},
            ]}]
            inputs = processor.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_dict=True,
                return_tensors="pt", do_sample_frames=False,
            ).to(args.device)
            sample_started = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
            raw = processor.batch_decode(
                generated[:, inputs.input_ids.shape[1]:], skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            prediction, probability = parse_output(raw); elapsed = time.perf_counter() - sample_started
            predictions.append({"path": row["path"], "label": int(row["label"]), "subject": row["subject"],
                                "prediction": prediction, "fall_probability": probability,
                                "raw_output": raw, "seconds": elapsed})
            print(f"[{position}/{len(rows)}] y={row['label']} p={prediction} score={probability:.2f} {elapsed:.2f}s", flush=True)
    with (args.output_root / "predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0])); writer.writeheader(); writer.writerows(predictions)
    labels = np.asarray([row["label"] for row in predictions]); outputs = np.asarray([row["prediction"] for row in predictions])
    summary = {"model": args.model, "protocol": "zero-shot binary, full-video ordered uniform sampling",
               "samples": len(rows), "frames": args.frames, "parse_errors": int(np.sum(outputs < 0)),
               "mean_inference_seconds": float(np.mean([row["seconds"] for row in predictions])),
               "total_seconds": time.perf_counter() - started, "metrics": metrics(labels, outputs)}
    (args.output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
