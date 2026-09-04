"""Audit whether OmniFall temporal labels contain enough pre-fall context."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def audit_file(path: Path, fall_label: int = 1, horizons: tuple[float, ...] = (1, 2, 3)) -> dict:
    by_video: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(path):
        by_video[row["path"]].append(row)

    fall_events = []
    for video, rows in by_video.items():
        fall_rows = [row for row in rows if int(row["label"]) == fall_label]
        if not fall_rows:
            continue
        onset = min(float(row["start"]) for row in fall_rows)
        observed_start = min(float(row["start"]) for row in rows)
        fall_events.append(
            {
                "path": video,
                "subject": int(rows[0]["subject"]),
                "cam": int(rows[0]["cam"]),
                "onset_seconds": onset,
                "available_prefall_seconds": max(0.0, onset - observed_start),
            }
        )

    subjects = sorted({event["subject"] for event in fall_events if event["subject"] >= 0})
    unique_trials: dict[str, dict] = {}
    for event in fall_events:
        # OmniFall paths generally differ only by a trailing CameraN token.
        trial = event["path"].rsplit("Camera", 1)[0]
        current = unique_trials.get(trial)
        if current is None or event["available_prefall_seconds"] > current["available_prefall_seconds"]:
            unique_trials[trial] = event

    def eligibility(events: list[dict]) -> dict[str, int]:
        return {
            f"at_least_{horizon:g}s": sum(
                event["available_prefall_seconds"] >= horizon for event in events
            )
            for horizon in horizons
        }

    contexts = sorted(event["available_prefall_seconds"] for event in fall_events)
    return {
        "source": str(path),
        "annotated_video_views_with_fall": len(fall_events),
        "estimated_unique_fall_trials": len(unique_trials),
        "subjects": subjects,
        "eligible_video_views": eligibility(fall_events),
        "eligible_unique_trials": eligibility(list(unique_trials.values())),
        "prefall_context_seconds": {
            "min": contexts[0] if contexts else None,
            "median": contexts[len(contexts) // 2] if contexts else None,
            "max": contexts[-1] if contexts else None,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fall-label", type=int, default=1)
    args = parser.parse_args()
    summary = {path.stem: audit_file(path, args.fall_label) for path in args.labels}
    payload = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()

