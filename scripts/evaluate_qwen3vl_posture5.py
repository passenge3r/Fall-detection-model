"""Zero-shot five-class posture evaluation with Qwen3-VL-2B-Instruct."""

from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import torch
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration


CLASS_NAMES = ["walking", "standing", "sitting", "lying_sleeping", "falling"]
PROMPT = """Classify the main human posture/action in this short ordered video clip.
Choose exactly one label:
- walking: upright locomotion
- standing: upright and mostly stationary
- sitting: seated on a bed, chair, or floor
- lying_sleeping: intentionally lying or sleeping on a bed
- falling: an uncontrolled transition toward the floor or ground

Return exactly one JSON object and no markdown:
{"class":"one_label","description":"brief visual evidence"}
"""

TEMPORAL_PROMPT = """Analyze these frames as ONE ordered video sequence from earliest to latest.
Classify the main human action into exactly one label: walking, standing, sitting,
lying_sleeping, or falling.

Decision rules:
1. falling requires a visible uncontrolled or abrupt downward transition from a higher
   posture toward the floor/ground. A person already lying still is NOT sufficient.
2. lying_sleeping means intentionally or stably lying, normally supported by a bed,
   sofa, or floor, without a visible abrupt fall transition.
3. walking requires body displacement or a step cycle across time. Do not call a moving
   upright person standing merely because individual frames look upright.
4. sitting requires the trunk to be supported in a seated posture; standing is upright
   and mostly stationary.
5. Use the initial, middle, and final posture and the direction/speed of motion. Do not
   classify from the final frame alone.

Return exactly one JSON object with no markdown and keep class to the bare label:
{"class":"one_label","initial":"posture","middle":"motion","final":"posture","evidence":"brief observable evidence"}
"""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def balanced_subset(rows: list[dict[str, str]], per_class: int) -> list[dict[str, str]]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["label"])].append(row)
    selected = []
    for label in range(len(CLASS_NAMES)):
        candidates = grouped[label]
        # Round-robin by subject to prevent a small pilot from representing only one person.
        candidates.sort(key=lambda row: (int(row["subject"]), row["segment_id"]))
        by_subject: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in candidates:
            by_subject[row["subject"]].append(row)
        index = 0
        while len([row for row in selected if int(row["label"]) == label]) < min(per_class, len(candidates)):
            made_progress = False
            for subject in sorted(by_subject, key=int):
                if index < len(by_subject[subject]):
                    selected.append(by_subject[subject][index]); made_progress = True
                    if len([row for row in selected if int(row["label"]) == label]) >= per_class:
                        break
            if not made_progress:
                break
            index += 1
    return selected


def save_sampled_frames(
    video_path: Path, start_seconds: float, end_seconds: float, count: int, output: Path
) -> list[str]:
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    start = max(0, min(int(round(start_seconds * fps)), frame_count - 1))
    end = max(start, min(int(round(end_seconds * fps)) - 1, frame_count - 1))
    targets = np.linspace(start, end, count).round().astype(int)
    paths = []
    for index, target in enumerate(targets):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(target))
        ok, frame = capture.read()
        if not ok:
            capture.release(); raise RuntimeError(f"Cannot decode frame {target}: {video_path}")
        path = output / f"frame_{index:02d}.jpg"
        cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        # Transformers accepts an absolute Windows path directly.  A file:// URI
        # containing percent-encoded Chinese characters is misread as base64.
        paths.append(str(path.resolve()))
    capture.release()
    return paths


def parse_class(text: str) -> str | None:
    try:
        payload = json.loads(text.strip())
        value = str(payload.get("class", "")).strip().lower()
        if value in CLASS_NAMES:
            return value
        for name in CLASS_NAMES:
            if value.startswith(name + ":"):
                return name
    except json.JSONDecodeError:
        pass
    match = re.search(r'"class"\s*:\s*"([a-z_]+)"', text.lower())
    return match.group(1) if match and match.group(1) in CLASS_NAMES else None


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=project / "data/metadata/gmdcsa24_posture5_segments.csv")
    parser.add_argument("--video-root", type=Path, default=project / "data/raw/GMDCSA24")
    parser.add_argument("--model", default="Qwen/Qwen3-VL-2B-Instruct")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--per-class", type=int, default=10)
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--max-pixels", type=int, default=128 * 32 * 32)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--prompt-mode", choices=("basic", "temporal"), default="basic")
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    rows = balanced_subset(read_csv(args.manifest), args.per_class)
    processor = AutoProcessor.from_pretrained(
        args.model, local_files_only=not args.allow_download
    )
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model, dtype=torch.bfloat16, attn_implementation="sdpa",
        local_files_only=not args.allow_download,
    ).eval().to(args.device)
    predictions = []
    started = time.perf_counter()
    # Keep temporary frame paths ASCII-only: the Transformers 5.14 image loader
    # treats Windows paths containing non-ASCII workspace names as base64 text.
    with tempfile.TemporaryDirectory(prefix="qwen3vl_posture5_") as temporary:
        temporary_root = Path(temporary)
        for position, row in enumerate(rows, 1):
            sample_dir = temporary_root / f"sample_{position:03d}"; sample_dir.mkdir()
            frame_uris = save_sampled_frames(
                args.video_root / row["video_path"], float(row["start_seconds"]),
                float(row["end_seconds"]), args.frames, sample_dir,
            )
            messages = [{"role": "user", "content": [
                {"type": "video", "video": frame_uris, "sample_fps": 2,
                 "min_pixels": 4 * 32 * 32, "max_pixels": args.max_pixels},
                {"type": "text", "text": TEMPORAL_PROMPT if args.prompt_mode == "temporal" else PROMPT},
            ]}]
            inputs = processor.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_dict=True, return_tensors="pt", do_sample_frames=False,
            ).to(args.device)
            sample_started = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
            trimmed = generated[:, inputs.input_ids.shape[1]:]
            raw = processor.batch_decode(
                trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]
            predicted_name = parse_class(raw)
            predicted_label = CLASS_NAMES.index(predicted_name) if predicted_name else -1
            elapsed = time.perf_counter() - sample_started
            predictions.append({
                "segment_id": row["segment_id"], "subject": row["subject"],
                "label": row["label"], "class_name": row["class_name"],
                "prediction": predicted_label, "predicted_class": predicted_name or "parse_error",
                "raw_output": raw, "seconds": elapsed,
            })
            print(
                f"[{position}/{len(rows)}] true={row['class_name']} pred={predicted_name} "
                f"time={elapsed:.2f}s", flush=True,
            )
    output_csv = args.output_root / "predictions.csv"
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0])); writer.writeheader(); writer.writerows(predictions)
    labels = np.asarray([int(row["label"]) for row in predictions])
    predicted = np.asarray([int(row["prediction"]) for row in predictions])
    confusion = np.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=int)
    for label, prediction in zip(labels, predicted, strict=True):
        if prediction >= 0: confusion[label, prediction] += 1
    recalls = [confusion[i, i] / confusion[i].sum() if confusion[i].sum() else 0 for i in range(len(CLASS_NAMES))]
    summary = {
        "model": args.model, "protocol": f"balanced zero-shot pilot, {args.per_class} per class",
        "prompt_mode": args.prompt_mode,
        "classes": CLASS_NAMES, "samples": len(rows), "frames_per_segment": args.frames,
        "max_pixels_per_frame": args.max_pixels,
        "max_new_tokens": args.max_new_tokens,
        "accuracy": float(np.mean(labels == predicted)), "macro_recall": float(np.mean(recalls)),
        "per_class_recall": dict(zip(CLASS_NAMES, recalls, strict=True)),
        "confusion_matrix": confusion.tolist(), "parse_errors": int(np.sum(predicted < 0)),
        "mean_inference_seconds": float(np.mean([row["seconds"] for row in predictions])),
        "total_seconds": time.perf_counter() - started,
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
