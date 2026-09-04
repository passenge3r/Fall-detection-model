"""Subject-disjoint QLoRA fine-tuning of Qwen3-VL-2B on GMDCSA24."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import time
from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoProcessor, BitsAndBytesConfig, Qwen3VLForConditionalGeneration


PROMPT = """The frames are one ordered activity video from earliest to latest.
Classify whether the main person undergoes a visible uncontrolled or abrupt downward
transition toward the floor. Return exactly one JSON object with keys class, risk,
and reason. class must be FALL or SAFE; risk must be high or low; reason must be brief."""


def answer(label: int) -> str:
    if label:
        return '{"class":"FALL","risk":"high","reason":"abrupt downward transition toward the floor"}'
    return '{"class":"SAFE","risk":"low","reason":"no visible uncontrolled fall transition"}'


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cache_frames(video: Path, count: int, cache_root: Path) -> list[str]:
    key = hashlib.sha1(f"{video.resolve()}|{count}".encode()).hexdigest()[:16]
    folder = cache_root / key
    paths = [folder / f"frame_{i:02d}.jpg" for i in range(count)]
    if all(p.exists() for p in paths):
        return [str(p.resolve()) for p in paths]
    folder.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    targets = np.linspace(0, max(total - 1, 0), count).round().astype(int)
    for i, target in enumerate(targets):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target)); ok, frame = cap.read()
        if not ok:
            cap.release(); raise RuntimeError(f"Cannot decode frame {target}: {video}")
        cv2.imwrite(str(paths[i]), frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
    cap.release()
    return [str(p.resolve()) for p in paths]


def content(frame_paths: list[str], max_pixels: int) -> list[dict]:
    return [
        {"type": "video", "video": frame_paths},
        {"type": "text", "text": PROMPT},
    ]


def move(batch, device: str):
    return {k: v.to(device) if hasattr(v, "to") else v for k, v in batch.items()}


def training_inputs(processor, frame_paths: list[str], label: int, max_pixels: int, device: str):
    target = answer(label)
    messages = [
        {"role": "user", "content": content(frame_paths, max_pixels)},
        {"role": "assistant", "content": [{"type": "text", "text": target}]},
    ]
    batch = processor.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=False, return_dict=True,
        return_tensors="pt", processor_kwargs={"videos_kwargs": {
            "do_sample_frames": False,
            "size": {"shortest_edge": len(frame_paths) * 4 * 32 * 32,
                     "longest_edge": len(frame_paths) * max_pixels},
        }},
    )
    labels = batch["input_ids"].clone()
    target_ids = processor.tokenizer(target, add_special_tokens=False).input_ids
    sequence = labels[0].tolist(); start = -1
    for i in range(len(sequence) - len(target_ids), -1, -1):
        if sequence[i:i + len(target_ids)] == target_ids:
            start = i; break
    if start < 0:
        raise RuntimeError("Cannot locate assistant target tokens")
    labels[:, :start] = -100
    batch["labels"] = labels
    return move(batch, device)


def inference_inputs(processor, frame_paths: list[str], max_pixels: int, device: str):
    messages = [{"role": "user", "content": content(frame_paths, max_pixels)}]
    batch = processor.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_dict=True,
        return_tensors="pt", processor_kwargs={"videos_kwargs": {
            "do_sample_frames": False,
            "size": {"shortest_edge": len(frame_paths) * 4 * 32 * 32,
                     "longest_edge": len(frame_paths) * max_pixels},
        }},
    )
    return move(batch, device)


def parse(text: str) -> int:
    try:
        value = str(json.loads(text.strip()).get("class", "")).strip().upper()
        if value == "FALL": return 1
        if value == "SAFE": return 0
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass
    upper = text.upper()
    match = __import__("re").search(r'"class"\s*:\s*"(FALL|SAFE)"', upper)
    if match: return 1 if match.group(1) == "FALL" else 0
    return 1 if upper.strip() == "FALL" else (0 if upper.strip() == "SAFE" else -1)


def classification_metrics(labels: list[int], predictions: list[int]) -> dict[str, float | int]:
    y, p = np.asarray(labels), np.asarray(predictions)
    tp = int(((y == 1) & (p == 1)).sum()); tn = int(((y == 0) & (p == 0)).sum())
    fp = int(((y == 0) & (p != 0)).sum()); fn = int(((y == 1) & (p != 1)).sum())
    div = lambda a, b: float(a / b) if b else 0.0
    f1_fall = div(2 * tp, 2 * tp + fp + fn); f1_safe = div(2 * tn, 2 * tn + fp + fn)
    recall = div(tp, tp + fn); specificity = div(tn, tn + fp)
    return {"samples": len(y), "accuracy": div(tp + tn, len(y)), "macro_f1": (f1_fall + f1_safe) / 2,
            "balanced_accuracy": (recall + specificity) / 2, "recall": recall, "specificity": specificity,
            "f1_fall": f1_fall, "f1_safe": f1_safe, "parse_errors": int((p < 0).sum()),
            "tp": tp, "tn": tn, "fp": fp, "fn": fn}


@torch.inference_mode()
def evaluate(model, processor, rows, root, cache, frames, max_pixels, device):
    model.eval(); labels, predictions, outputs = [], [], []
    for row in rows:
        paths = cache_frames(root / row["path"], frames, cache)
        batch = inference_inputs(processor, paths, max_pixels, device)
        generated = model.generate(**batch, max_new_tokens=48, do_sample=False)
        raw = processor.batch_decode(generated[:, batch["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
        pred = parse(raw); labels.append(int(row["label"])); predictions.append(pred)
        outputs.append({"path": row["path"], "label": int(row["label"]), "prediction": pred, "raw_output": raw})
    return classification_metrics(labels, predictions), outputs


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, default=project / "data/metadata/gmdcsa24.csv")
    ap.add_argument("--video-root", type=Path, default=project / "data/raw/GMDCSA24")
    ap.add_argument("--output-root", type=Path, required=True)
    ap.add_argument("--model", default="Qwen/Qwen3-VL-2B-Instruct")
    ap.add_argument("--epochs", type=int, default=3); ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--max-pixels", type=int, default=8192); ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--grad-accum", type=int, default=4); ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20260805); ap.add_argument("--max-train-samples", type=int)
    ap.add_argument("--max-val-samples", type=int); ap.add_argument("--device", default="cuda")
    args = ap.parse_args(); args.output_root.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)
    rows = read_csv(args.manifest)
    train = [r for r in rows if r["subject"] in {"1", "2", "3"}]
    val = [r for r in rows if r["subject"] == "4"]
    if args.max_train_samples: train = train[:args.max_train_samples]
    if args.max_val_samples: val = val[:args.max_val_samples]
    processor = AutoProcessor.from_pretrained(args.model, local_files_only=True)
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                               bnb_4bit_compute_dtype=torch.bfloat16)
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model, quantization_config=quant, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa")
    model = prepare_model_for_kbit_training(
        model, use_gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False})
    model = get_peft_model(model, LoraConfig(
        r=args.rank, lora_alpha=2 * args.rank, lora_dropout=.05, bias="none",
        target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM"))
    model.config.use_cache = False
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"train={len(train)} val={len(val)} trainable={trainable:,}/{total:,}", flush=True)
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=args.lr)
    cache = args.output_root / "frame_cache_f16"
    history, best = [], -1.0; started = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        model.train(); random.shuffle(train); optimizer.zero_grad(set_to_none=True); losses = []
        for step, row in enumerate(train, 1):
            paths = cache_frames(args.video_root / row["path"], args.frames, cache)
            batch = training_inputs(processor, paths, int(row["label"]), args.max_pixels, args.device)
            loss = model(**batch).loss / args.grad_accum; loss.backward(); losses.append(float(loss.item() * args.grad_accum))
            if step % args.grad_accum == 0 or step == len(train):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); optimizer.zero_grad(set_to_none=True)
            if step == 1 or step % 10 == 0:
                print(f"epoch={epoch} step={step}/{len(train)} loss={np.mean(losses[-10:]):.4f} "
                      f"gpu={torch.cuda.max_memory_allocated()/2**30:.2f}GB", flush=True)
        val_metrics, outputs = evaluate(model, processor, val, args.video_root, cache,
                                        args.frames, args.max_pixels, args.device)
        record = {"epoch": epoch, "train_loss": float(np.mean(losses)), **val_metrics}
        history.append(record); print(json.dumps(record, ensure_ascii=False), flush=True)
        epoch_dir = args.output_root / f"epoch_{epoch}"
        model.save_pretrained(epoch_dir)
        with (epoch_dir / "val_predictions.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(outputs[0])); writer.writeheader(); writer.writerows(outputs)
        if val_metrics["macro_f1"] > best:
            best = val_metrics["macro_f1"]
            model.save_pretrained(args.output_root / "best_adapter")
            (args.output_root / "best_epoch.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    write = lambda p, obj: p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    write(args.output_root / "history.json", history)
    with (args.output_root / "history.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(history[0])); writer.writeheader(); writer.writerows(history)
    fig, ax1 = plt.subplots(figsize=(7.5, 4.8)); epochs = [r["epoch"] for r in history]
    ax1.plot(epochs, [r["train_loss"] for r in history], "o-", label="train loss", color="#2878B5")
    ax1.set_xlabel("Epoch"); ax1.set_ylabel("Train loss"); ax1.set_xticks(epochs); ax1.grid(alpha=.25)
    ax2 = ax1.twinx(); ax2.plot(epochs, [100*r["macro_f1"] for r in history], "s-", label="val Macro-F1", color="#C82423")
    ax2.set_ylabel("Validation Macro-F1 (%)"); lines = ax1.lines + ax2.lines
    ax1.legend(lines, [x.get_label() for x in lines], loc="center right")
    fig.tight_layout(); fig.savefig(args.output_root / "learning_curve.png", dpi=180); plt.close(fig)
    summary = {"protocol": "GMDCSA24 subjects 1-3 train, subject 4 validation", "train_samples": len(train),
               "val_samples": len(val), "frames": args.frames, "max_pixels": args.max_pixels, "epochs": args.epochs,
               "rank": args.rank, "trainable_parameters": trainable, "best_macro_f1": best,
               "seconds": time.perf_counter() - started}
    write(args.output_root / "summary.json", summary); print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
