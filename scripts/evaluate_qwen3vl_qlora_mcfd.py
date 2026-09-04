"""Evaluate base or QLoRA Qwen3-VL on a fixed balanced MCFD subset/full cross-view set."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import torch
from peft import PeftModel
from transformers import AutoProcessor, BitsAndBytesConfig, Qwen3VLForConditionalGeneration

from train_qwen3vl_qlora import PROMPT, classification_metrics, content, parse


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cache_segment(video: Path, start: int, end: int, count: int, root: Path) -> list[str]:
    key = hashlib.sha1(f"{video.resolve()}|{start}|{end}|{count}".encode()).hexdigest()[:20]
    folder = root / key; paths = [folder / f"frame_{i:02d}.jpg" for i in range(count)]
    if all(p.exists() for p in paths): return [str(p.resolve()) for p in paths]
    folder.mkdir(parents=True, exist_ok=True); cap = cv2.VideoCapture(str(video))
    targets = np.linspace(start, end, count).round().astype(int)
    positions: dict[int, list[int]] = defaultdict(list)
    for i, target in enumerate(targets.tolist()): positions[target].append(i)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start); last = None
    for index in range(start, end + 1):
        ok, frame = cap.read()
        if not ok: break
        last = frame
        for i in positions.get(index, []): cv2.imwrite(str(paths[i]), frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
    cap.release()
    if last is None: raise RuntimeError(f"Cannot decode {video} [{start},{end}]")
    for path in paths:
        if not path.exists(): cv2.imwrite(str(path), last, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return [str(p.resolve()) for p in paths]


def fixed_subset(rows: list[dict[str, str]], size: int, seed: int) -> list[dict[str, str]]:
    if not size or size >= len(rows): return rows
    if size % 2: raise ValueError("Balanced subset size must be even")
    rng = random.Random(seed); selected = []
    for label in ("0", "1"):
        group = [r for r in rows if r["label"] == label]
        group.sort(key=lambda r: (int(r["cam"]), r["path"], int(r["start_frame"])))
        rng.shuffle(group); selected.extend(group[:size // 2])
    return sorted(selected, key=lambda r: (int(r["cam"]), r["path"], int(r["start_frame"])))


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=project / "data/metadata/mcfd_segments.csv")
    ap.add_argument("--video-root", type=Path, default=project / "data/raw/MCFD/kaggle")
    ap.add_argument("--output-root", type=Path, required=True); ap.add_argument("--adapter", type=Path)
    ap.add_argument("--cache-root", type=Path)
    ap.add_argument("--subset-size", type=int, default=192); ap.add_argument("--seed", type=int, default=20260805)
    ap.add_argument("--frames", type=int, default=16); ap.add_argument("--max-pixels", type=int, default=32768)
    ap.add_argument("--device", default="cuda"); args = ap.parse_args(); args.output_root.mkdir(parents=True, exist_ok=True)
    formal = [r for r in read_csv(args.manifest) if r["cam"] in {"2", "4", "5", "6", "7", "8"}]
    rows = fixed_subset(formal, args.subset_size, args.seed)
    with (args.output_root / "test_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-2B-Instruct", local_files_only=True)
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                               bnb_4bit_compute_dtype=torch.bfloat16)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen3-VL-2B-Instruct", quantization_config=quant, device_map={"": 0},
        local_files_only=True, attn_implementation="sdpa")
    if args.adapter: model = PeftModel.from_pretrained(model, args.adapter)
    model.eval(); model.config.use_cache = True
    outputs, labels, predictions, times = [], [], [], []
    cache = args.cache_root or (args.output_root / "frame_cache_f16")
    started = time.perf_counter()
    for pos, row in enumerate(rows, 1):
        start, end = int(row["start_frame"]), int(row["end_frame"])
        paths = cache_segment(args.video_root / row["path"], start, end, args.frames, cache)
        messages = [{"role": "user", "content": content(paths, args.max_pixels)}]
        batch = processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt",
            processor_kwargs={"videos_kwargs": {"do_sample_frames": False,
                "size": {"shortest_edge": len(paths) * 4 * 32 * 32,
                         "longest_edge": len(paths) * args.max_pixels}}})
        batch = {k: v.to(args.device) if hasattr(v, "to") else v for k, v in batch.items()}
        tick = time.perf_counter()
        with torch.inference_mode(): generated = model.generate(**batch, max_new_tokens=48, do_sample=False)
        elapsed = time.perf_counter() - tick
        raw = processor.batch_decode(generated[:, batch["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
        pred = parse(raw); payload = {}
        try: payload = json.loads(raw)
        except json.JSONDecodeError: pass
        labels.append(int(row["label"])); predictions.append(pred); times.append(elapsed)
        outputs.append({"sample": f"{row['path']}#f{start}-{end}", "camera": row["cam"],
                        "label": row["label"], "prediction": pred, "risk": payload.get("risk", ""),
                        "reason": payload.get("reason", ""), "raw_output": raw, "seconds": elapsed})
        if pos == 1 or pos % 20 == 0: print(f"[{pos}/{len(rows)}] y={row['label']} p={pred} {elapsed:.2f}s", flush=True)
    with (args.output_root / "predictions.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(outputs[0])); writer.writeheader(); writer.writerows(outputs)
    summary = {"protocol": "MCFD cameras 2/4/5/6/7/8, fixed balanced subset" if args.subset_size else "MCFD full cross-view",
               "adapter": str(args.adapter) if args.adapter else None, "samples": len(rows), "seed": args.seed,
               "frames": args.frames, "max_pixels_per_frame": args.max_pixels,
               "mean_inference_seconds": float(np.mean(times)), "total_seconds": time.perf_counter() - started,
               "metrics": classification_metrics(labels, predictions)}
    (args.output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
