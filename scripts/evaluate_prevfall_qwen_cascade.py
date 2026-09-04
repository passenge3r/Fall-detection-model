from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from app.multimodal import MultimodalReviewConfig, QwenVideoReviewer  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sample_clip(path: Path, start: float, end: float, count: int) -> list[np.ndarray]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = max(0.0, (total - 1) / fps) if fps > 0 and total > 0 else end
    end = min(end, duration)
    start = min(start, end)
    frames = []
    for second in np.linspace(start, end, count):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(round(second * fps)))
        ok, frame = capture.read()
        if not ok:
            capture.release()
            raise RuntimeError(f"Cannot decode {path} at {second:.3f}s")
        frames.append(frame)
    capture.release()
    return frames


def metrics(tp: int, tn: int, fp: int, fn: int) -> dict[str, float | int]:
    safe = lambda a, b: float(a / b) if b else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "accuracy": safe(tp + tn, tp + tn + fp + fn),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
    }


def summarize(rows: list[dict[str, str]], total_falls: int, total_adl: int) -> dict:
    qwen_tp = sum(int(row["video_label"]) == 1 and int(row["qwen_positive"]) == 1 for row in rows)
    qwen_fp = sum(int(row["video_label"]) == 0 and int(row["qwen_positive"]) == 1 for row in rows)
    cascade = metrics(qwen_tp, total_adl - qwen_fp, qwen_fp, total_falls - qwen_tp)
    skeleton_tp = sum(int(row["video_label"]) == 1 for row in rows)
    skeleton_fp = sum(int(row["video_label"]) == 0 for row in rows)
    skeleton = metrics(
        skeleton_tp, total_adl - skeleton_fp, skeleton_fp, total_falls - skeleton_tp
    )
    latencies = [float(row["latency_seconds"]) for row in rows]
    class_counts: dict[str, int] = {}
    for row in rows:
        name = row["action_class"]
        class_counts[name] = class_counts.get(name, 0) + 1
    return {
        "samples_completed": len(rows),
        "skeleton_only": skeleton,
        "qwen_as_strict_confirmer": cascade,
        "safe_fusion": {
            "metrics": skeleton,
            "policy": "Qwen escalates or flags conflict but never suppresses a skeleton alert",
        },
        "qwen_confirmation_rate_on_skeleton_tp": (
            qwen_tp / skeleton_tp if skeleton_tp else 0.0
        ),
        "qwen_false_confirmation_rate_on_skeleton_fp": (
            qwen_fp / skeleton_fp if skeleton_fp else 0.0
        ),
        "latency_seconds": {
            "mean": float(np.mean(latencies)) if latencies else None,
            "median": float(np.median(latencies)) if latencies else None,
            "min": float(np.min(latencies)) if latencies else None,
            "max": float(np.max(latencies)) if latencies else None,
        },
        "action_class_counts": class_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate triggered Qwen3-VL review on PreVFall OOF alerts."
    )
    parser.add_argument(
        "--manifest", type=Path,
        default=PROJECT / "data/metadata/prevfall_qwen_oof_triggers_2s.csv",
    )
    parser.add_argument(
        "--output", type=Path,
        default=PROJECT / "results/prevfall_qwen_cascade_2s/predictions.csv",
    )
    parser.add_argument("--model", default="Qwen/Qwen3-VL-2B-Instruct")
    parser.add_argument("--frames", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=112)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    jobs = read_csv(args.manifest)
    if args.limit:
        jobs = jobs[: args.limit]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    completed = read_csv(args.output) if args.output.exists() else []
    done = {row["video_path"] for row in completed}
    reviewer = QwenVideoReviewer(MultimodalReviewConfig(
        enabled=True,
        model_name=args.model,
        frames=args.frames,
        max_new_tokens=args.max_new_tokens,
        allow_download=args.allow_download,
    ))
    fieldnames = [
        "video_path", "subject", "fold", "video_label", "window_path",
        "clip_start_seconds", "clip_end_seconds", "lead_seconds",
        "skeleton_probability", "skeleton_threshold", "action_class",
        "fall_stage", "risk_level", "confidence", "qwen_positive",
        "review_outcome", "summary_zh", "evidence", "latency_seconds",
        "model_output_valid", "raw_output",
    ]
    for position, job in enumerate(jobs, 1):
        if job["video_path"] in done:
            continue
        frames = sample_clip(
            PROJECT / job["video_path"],
            float(job["clip_start_seconds"]),
            float(job["clip_end_seconds"]),
            max(args.frames, 16),
        )
        result = reviewer.review(frames, {
            "video_path": job["video_path"],
            "skeleton_probability": float(job["probability"]),
        })
        qwen_positive = int(
            result["review_outcome"]
            in {"CORROBORATED_PREFALL", "CORROBORATED_FALL", "CORROBORATED_POSTFALL"}
        )
        output = {
            "video_path": job["video_path"],
            "subject": job["subject"],
            "fold": job["fold"],
            "video_label": job["video_label"],
            "window_path": job["window_path"],
            "clip_start_seconds": job["clip_start_seconds"],
            "clip_end_seconds": job["clip_end_seconds"],
            "lead_seconds": job["lead_seconds"],
            "skeleton_probability": job["probability"],
            "skeleton_threshold": job["threshold"],
            "action_class": result["action_class"],
            "fall_stage": result["fall_stage"],
            "risk_level": result["risk_level"],
            "confidence": result["confidence"],
            "qwen_positive": qwen_positive,
            "review_outcome": result["review_outcome"],
            "summary_zh": result["summary_zh"],
            "evidence": result["evidence"],
            "latency_seconds": result["latency_seconds"],
            "model_output_valid": result["model_output_valid"],
            "raw_output": result["raw_output"],
        }
        write_header = not args.output.exists()
        with args.output.open("a", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(output)
        completed.append({key: str(value) for key, value in output.items()})
        summary = summarize(completed, total_falls=72, total_adl=36)
        args.output.with_suffix(".summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            f"[{position}/{len(jobs)}] y={job['video_label']} "
            f"qwen={qwen_positive} class={result['action_class']} "
            f"stage={result['fall_stage']} {result['latency_seconds']:.2f}s",
            flush=True,
        )
    final = summarize(completed, total_falls=72, total_adl=36)
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(final, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(final, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
