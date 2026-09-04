"""Evaluate event recall, lead time, and false alarm episodes/hour."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


HORIZONS = ("1s", "2s", "3s")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def confirmed_frames(frames: list[int], max_gap: int, min_windows: int) -> list[int]:
    if not frames:
        return []
    ordered = sorted(set(frames)); runs = [[ordered[0]]]
    for previous, current in zip(ordered, ordered[1:]):
        if current - previous > max_gap:
            runs.append([])
        runs[-1].append(current)
    return [run[min_windows - 1] for run in runs if len(run) >= min_windows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stride-frames", type=int, default=16)
    parser.add_argument("--confirm-windows", type=int, default=1)
    parser.add_argument("--folds", type=int, nargs="+", default=[1, 2, 3, 4])
    args = parser.parse_args()

    metadata_rows = read_rows(args.manifest)
    metadata = {row["path"]: row for row in metadata_rows}
    predictions = []
    for fold in args.folds:
        fold_dir = args.predictions_root / f"fold_{fold}"
        metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
        thresholds = metrics["decision_thresholds_calibrated_on_validation"]
        for row in read_rows(fold_dir / "test_predictions.csv"):
            predictions.append((fold, row, thresholds))

    results = {}
    for horizon in HORIZONS:
        by_video: dict[str, list[dict[str, object]]] = defaultdict(list)
        for fold, row, thresholds in predictions:
            meta = metadata[row["path"]]
            probability = float(row[f"p_{horizon}"])
            by_video[meta["video_path"]].append({
                "path": row["path"], "subject": meta["subject"],
                "video_label": int(meta["video_label"]),
                "label": int(float(row[f"y_{horizon}"])),
                "prediction": probability >= float(thresholds[horizon]),
                "probability": probability, "start_frame": int(meta["start_frame"]),
                "end_seconds": float(meta["end_seconds"]),
                "lead_seconds": None if meta["lead_seconds"] == "" else float(meta["lead_seconds"]),
            })

        eligible_falls = 0; detected_falls = 0; lead_times = []
        adl_false_episodes = 0; adl_alert_windows = 0; adl_windows = 0; adl_seconds = 0.0
        early_fall_false_episodes = 0
        per_video = []
        for video, rows in by_video.items():
            is_fall = bool(rows[0]["video_label"])
            if is_fall:
                positive_rows = [row for row in rows if row["label"] == 1]
                positive_frames = [int(row["start_frame"]) for row in positive_rows]
                possible_confirmations = confirmed_frames(
                    positive_frames, int(args.stride_frames * 1.5), args.confirm_windows
                )
                if possible_confirmations:
                    eligible_falls += 1
                    hit_rows = {int(row["start_frame"]): row for row in positive_rows if row["prediction"]}
                    confirmations = confirmed_frames(
                        list(hit_rows), int(args.stride_frames * 1.5), args.confirm_windows
                    )
                    if confirmations:
                        detected_falls += 1
                        lead = float(hit_rows[confirmations[0]]["lead_seconds"])
                        lead_times.append(lead)
                    else:
                        lead = None
                    early_false = [int(row["start_frame"]) for row in rows if row["label"] == 0 and row["prediction"]]
                    early_episodes = len(confirmed_frames(
                        early_false, int(args.stride_frames * 1.5), args.confirm_windows
                    ))
                    early_fall_false_episodes += early_episodes
                    per_video.append({"video": video, "detected": bool(confirmations), "lead_seconds": lead,
                                      "early_false_episodes": early_episodes})
            else:
                alert_frames = [int(row["start_frame"]) for row in rows if row["prediction"]]
                episodes = len(confirmed_frames(
                    alert_frames, int(args.stride_frames * 1.5), args.confirm_windows
                ))
                adl_false_episodes += episodes; adl_alert_windows += len(alert_frames); adl_windows += len(rows)
                adl_seconds += max(float(row["end_seconds"]) for row in rows)
                per_video.append({"video": video, "false_alarm_episodes": episodes,
                                  "alert_windows": len(alert_frames), "windows": len(rows)})

        safe = lambda numerator, denominator: float(numerator / denominator) if denominator else 0.0
        results[horizon] = {
            "eligible_fall_events": eligible_falls, "detected_fall_events": detected_falls,
            "event_recall": safe(detected_falls, eligible_falls),
            "lead_time_seconds": {
                "mean": float(np.mean(lead_times)) if lead_times else None,
                "median": float(np.median(lead_times)) if lead_times else None,
                "min": float(np.min(lead_times)) if lead_times else None,
                "max": float(np.max(lead_times)) if lead_times else None,
            },
            "adl_duration_hours": adl_seconds / 3600,
            "adl_false_alarm_episodes": adl_false_episodes,
            "adl_false_alarm_episodes_per_hour": safe(adl_false_episodes, adl_seconds / 3600),
            "adl_alert_window_rate": safe(adl_alert_windows, adl_windows),
            "early_false_alarm_episodes_in_fall_videos": early_fall_false_episodes,
            "per_video": per_video,
        }

    summary = {"route_root": str(args.predictions_root), "confirm_windows": args.confirm_windows, "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    compact = {horizon: {key: value for key, value in result.items() if key != "per_video"} for horizon, result in results.items()}
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
