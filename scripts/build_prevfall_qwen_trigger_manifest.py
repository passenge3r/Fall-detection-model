from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build an OOF skeleton-triggered PreVFall manifest for Qwen review."
    )
    parser.add_argument(
        "--predictions-root", type=Path,
        default=project / "outputs/prevfall_rtmpose_stgcnpp_300e_b128",
    )
    parser.add_argument(
        "--window-manifest", type=Path,
        default=project / "data/metadata/prevfall_rtmpose_prefall_w64_s16_h123.csv",
    )
    parser.add_argument("--horizon", choices=("1s", "2s", "3s"), default="2s")
    parser.add_argument("--clip-seconds", type=float, default=4.0)
    parser.add_argument("--post-seconds", type=float, default=0.0)
    parser.add_argument(
        "--output", type=Path,
        default=project / "data/metadata/prevfall_qwen_oof_triggers_2s.csv",
    )
    args = parser.parse_args()

    metadata = {row["path"]: row for row in read_csv(args.window_manifest)}
    by_video: dict[str, list[dict[str, object]]] = defaultdict(list)
    for fold in range(1, 10):
        fold_dir = args.predictions_root / f"fold_{fold}"
        metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
        threshold = float(
            metrics["decision_thresholds_calibrated_on_validation"][args.horizon]
        )
        for prediction in read_csv(fold_dir / "test_predictions.csv"):
            meta = metadata[prediction["path"]]
            probability = float(prediction[f"p_{args.horizon}"])
            by_video[meta["video_path"]].append({
                "fold": fold,
                "window_path": prediction["path"],
                "video_path": meta["video_path"],
                "subject": int(meta["subject"]),
                "video_label": int(meta["video_label"]),
                "window_label": int(float(prediction[f"y_{args.horizon}"])),
                "start_frame": int(meta["start_frame"]),
                "end_frame": int(meta["end_frame"]),
                "end_seconds": float(meta["end_seconds"]),
                "lead_seconds": meta["lead_seconds"],
                "probability": probability,
                "threshold": threshold,
                "triggered": probability >= threshold,
            })

    selected = []
    skeleton_misses = []
    for video_path, rows in sorted(by_video.items()):
        rows.sort(key=lambda row: int(row["start_frame"]))
        video_label = int(rows[0]["video_label"])
        if video_label:
            # Evaluate Qwen on the first OOF alert that is truly inside the selected
            # horizon. This measures the second-stage confirmer on real skeleton TPs;
            # skeleton misses remain misses in the final 108-video metrics.
            candidates = [
                row for row in rows if row["triggered"] and row["window_label"] == 1
            ]
        else:
            candidates = [row for row in rows if row["triggered"]]
        if not candidates:
            if video_label:
                skeleton_misses.append(video_path)
            continue
        row = dict(candidates[0])
        row["clip_end_seconds"] = float(row["end_seconds"]) + args.post_seconds
        row["clip_start_seconds"] = max(
            0.0, float(row["clip_end_seconds"]) - args.clip_seconds
        )
        row["expected_review_positive"] = video_label
        selected.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(selected[0])
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(selected)
    positives = sum(int(row["video_label"]) for row in selected)
    summary = {
        "protocol": "first true-horizon OOF alert for fall videos; first OOF alert for ADL videos",
        "horizon": args.horizon,
        "clip_seconds": args.clip_seconds,
        "post_seconds": args.post_seconds,
        "videos_total": len(by_video),
        "review_jobs": len(selected),
        "skeleton_true_positive_videos": positives,
        "skeleton_false_positive_videos": len(selected) - positives,
        "skeleton_missed_fall_videos": len(skeleton_misses),
        "skeleton_misses": skeleton_misses,
        "output": str(args.output),
    }
    summary_path = args.output.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
