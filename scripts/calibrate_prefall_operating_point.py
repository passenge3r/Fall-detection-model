"""Calibrate pre-fall thresholds against event-level false-alarm budgets.

Thresholds are selected independently on each fold's validation subjects and are
then frozen before evaluating the corresponding held-out test subject.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


HORIZONS = ("1s", "2s", "3s")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def confirmed_frames(frames: list[int], max_gap: int, min_windows: int) -> list[int]:
    if not frames:
        return []
    ordered = sorted(set(frames))
    runs = [[ordered[0]]]
    for previous, current in zip(ordered, ordered[1:]):
        if current - previous > max_gap:
            runs.append([])
        runs[-1].append(current)
    return [run[min_windows - 1] for run in runs if len(run) >= min_windows]


def evaluate(
    prediction_rows: list[dict[str, str]],
    metadata: dict[str, dict[str, str]],
    horizon: str,
    threshold: float,
    stride_frames: int,
    confirm_windows: int,
) -> dict[str, float | int | None]:
    by_video: dict[str, list[dict[str, float | int]]] = defaultdict(list)
    for row in prediction_rows:
        meta = metadata[row["path"]]
        by_video[meta["video_path"]].append(
            {
                "video_label": int(meta["video_label"]),
                "label": int(float(row[f"y_{horizon}"])),
                "prediction": int(float(row[f"p_{horizon}"]) >= threshold),
                "start_frame": int(meta["start_frame"]),
                "end_seconds": float(meta["end_seconds"]),
                "lead_seconds": float(meta["lead_seconds"]) if meta["lead_seconds"] else -1.0,
            }
        )

    max_gap = int(stride_frames * 1.5)
    eligible = detected = false_episodes = 0
    lead_times: list[float] = []
    adl_seconds = 0.0
    for rows in by_video.values():
        is_fall = bool(rows[0]["video_label"])
        if is_fall:
            positive = [row for row in rows if row["label"] == 1]
            possible = confirmed_frames(
                [int(row["start_frame"]) for row in positive], max_gap, confirm_windows
            )
            if not possible:
                continue
            eligible += 1
            hits = {int(row["start_frame"]): row for row in positive if row["prediction"]}
            confirmations = confirmed_frames(list(hits), max_gap, confirm_windows)
            if confirmations:
                detected += 1
                lead_times.append(float(hits[confirmations[0]]["lead_seconds"]))
        else:
            alerts = [int(row["start_frame"]) for row in rows if row["prediction"]]
            false_episodes += len(confirmed_frames(alerts, max_gap, confirm_windows))
            adl_seconds += max(float(row["end_seconds"]) for row in rows)

    hours = adl_seconds / 3600.0
    return {
        "threshold": float(threshold),
        "eligible_fall_events": eligible,
        "detected_fall_events": detected,
        "event_recall": float(detected / eligible) if eligible else 0.0,
        "mean_lead_seconds": float(np.mean(lead_times)) if lead_times else None,
        "adl_duration_hours": hours,
        "adl_false_alarm_episodes": false_episodes,
        "adl_false_alarm_episodes_per_hour": float(false_episodes / hours) if hours else 0.0,
    }


def candidate_thresholds(rows: list[dict[str, str]], horizon: str) -> list[float]:
    scores = sorted({float(row[f"p_{horizon}"]) for row in rows})
    # Above the maximum is a valid zero-alert operating point.
    return [float(np.nextafter(score, -np.inf)) for score in scores] + [float("inf")]


def choose_operating_point(points: list[dict], budget: float) -> dict:
    feasible = [point for point in points if point["adl_false_alarm_episodes_per_hour"] <= budget]
    if not feasible:
        raise RuntimeError("candidate grid must include a zero-alert operating point")

    def rank(point: dict) -> tuple[float, float, float, float]:
        lead = point["mean_lead_seconds"] if point["mean_lead_seconds"] is not None else -1.0
        return (
            point["event_recall"],
            lead,
            -point["adl_false_alarm_episodes_per_hour"],
            -point["threshold"],
        )

    return max(feasible, key=rank)


def aggregate_fold_results(folds: list[dict]) -> dict:
    eligible = sum(int(item["eligible_fall_events"]) for item in folds)
    detected = sum(int(item["detected_fall_events"]) for item in folds)
    false_episodes = sum(int(item["adl_false_alarm_episodes"]) for item in folds)
    hours = sum(float(item["adl_duration_hours"]) for item in folds)
    lead_numerator = sum(
        float(item["mean_lead_seconds"]) * int(item["detected_fall_events"])
        for item in folds
        if item["mean_lead_seconds"] is not None
    )
    return {
        "eligible_fall_events": eligible,
        "detected_fall_events": detected,
        "event_recall": float(detected / eligible) if eligible else 0.0,
        "mean_lead_seconds": float(lead_numerator / detected) if detected else None,
        "adl_duration_hours": hours,
        "adl_false_alarm_episodes": false_episodes,
        "adl_false_alarm_episodes_per_hour": float(false_episodes / hours) if hours else 0.0,
    }


def plot_operating_points(path: Path, results: dict[str, dict]) -> None:
    figure, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharex=True)
    for axis, horizon in zip(axes, HORIZONS, strict=True):
        budgets = []
        recalls = []
        false_alarm_rates = []
        for budget_name, value in results[horizon].items():
            budgets.append(float(budget_name.removesuffix("_per_hour")))
            recalls.append(100 * value["aggregate_test"]["event_recall"])
            false_alarm_rates.append(value["aggregate_test"]["adl_false_alarm_episodes_per_hour"])
        axis.plot(budgets, recalls, "o-", color="#1976d2", label="test event recall")
        axis.set(title=f"{horizon} horizon", xlabel="Validation FA budget (/h)", ylabel="Event recall (%)")
        axis.set_ylim(-2, 102)
        axis.grid(alpha=0.25)
        twin = axis.twinx()
        twin.plot(budgets, false_alarm_rates, "s--", color="#d32f2f", label="actual test FA/h")
        twin.plot(budgets, budgets, ":", color="#777777", label="requested budget")
        twin.set_ylabel("Test false-alarm episodes/hour")
        lines = axis.lines + twin.lines
        axis.legend(lines, [line.get_label() for line in lines], fontsize=7, loc="upper left")
    figure.suptitle("Validation-calibrated pre-fall operating points (held-out subjects)")
    figure.tight_layout()
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--budgets", type=float, nargs="+", default=[5, 10, 30, 60])
    parser.add_argument("--stride-frames", type=int, default=16)
    parser.add_argument("--confirm-windows", type=int, default=2)
    parser.add_argument("--folds", type=int, nargs="+", default=[1, 2, 3, 4])
    args = parser.parse_args()

    metadata = {row["path"]: row for row in read_rows(args.manifest)}
    results: dict[str, dict] = {}
    for horizon in HORIZONS:
        by_budget: dict[str, dict] = {}
        for budget in args.budgets:
            fold_results = []
            for fold in args.folds:
                fold_dir = args.predictions_root / f"fold_{fold}"
                val_rows = read_rows(fold_dir / "val_predictions.csv")
                test_rows = read_rows(fold_dir / "test_predictions.csv")
                validation_points = [
                    evaluate(
                        val_rows, metadata, horizon, threshold,
                        args.stride_frames, args.confirm_windows,
                    )
                    for threshold in candidate_thresholds(val_rows, horizon)
                ]
                selected = choose_operating_point(validation_points, budget)
                test = evaluate(
                    test_rows, metadata, horizon, selected["threshold"],
                    args.stride_frames, args.confirm_windows,
                )
                fold_results.append({
                    "fold": fold,
                    "selected_threshold": selected["threshold"],
                    "validation": selected,
                    "test": test,
                })
            aggregate = aggregate_fold_results([item["test"] for item in fold_results])
            by_budget[f"{budget:g}_per_hour"] = {"aggregate_test": aggregate, "folds": fold_results}
        results[horizon] = by_budget

    summary = {
        "route_root": str(args.predictions_root),
        "selection": "validation event recall maximized subject to ADL false-alarm episodes/hour budget",
        "confirm_windows": args.confirm_windows,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plot_operating_points(args.output.with_suffix(".png"), results)
    compact = {
        horizon: {
            budget: value["aggregate_test"] for budget, value in budget_results.items()
        }
        for horizon, budget_results in results.items()
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
