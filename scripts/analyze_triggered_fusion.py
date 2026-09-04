"""Analyze a trigger-and-review fusion policy on aligned posture predictions."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent


def read(files: list[Path]) -> dict[str, dict[str, str]]:
    result = {}
    for file in files:
        with file.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                result[row["segment_id"]] = row
    return result


def main() -> None:
    skeleton = read(sorted((PROJECT / "results/posture5/rtmpose_compact_tgcn_e300").glob("fold_*/test_predictions.csv")))
    qwen_root = PROJECT / "results/posture5/qwen3vl2b_temporal8_balanced50"
    qwen = read([qwen_root / "predictions.csv"])
    qwen_summary = json.loads((qwen_root / "summary.json").read_text(encoding="utf-8"))
    rows = []
    for identifier, visual in qwen.items():
        pose = skeleton[identifier]
        pose_fall = pose["predicted_class"] == "falling"
        visual_fall = visual["predicted_class"] == "falling"
        if pose_fall and visual_fall:
            level = "level_1_confirmed_fall"
        elif pose_fall:
            level = "level_2_pose_trigger_review"
        elif visual_fall:
            level = "level_2_vlm_only_review"
        else:
            level = "no_fall_alert"
        rows.append({
            "segment_id": identifier,
            "true_class": pose["class_name"],
            "skeleton_class": pose["predicted_class"],
            "qwen_class": visual["predicted_class"],
            "alarm_level": level,
        })
    output_csv = qwen_root / "triggered_fusion_decisions.csv"
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    counts = Counter(row["alarm_level"] for row in rows)
    by_truth = {
        truth: dict(Counter(row["alarm_level"] for row in rows if row["true_class"] == truth))
        for truth in ("falling", "non_falling")
    }
    by_truth["non_falling"] = dict(Counter(
        row["alarm_level"] for row in rows if row["true_class"] != "falling"
    ))
    triggered = sum(row["skeleton_class"] == "falling" for row in rows)
    summary = {
        "policy": {
            "level_1": "skeleton=falling AND Qwen=falling",
            "level_2": "only one branch says falling; retain alert for review",
            "no_alert": "neither branch says falling",
        },
        "samples": len(rows),
        "alarm_counts": dict(counts),
        "alarm_counts_by_truth": by_truth,
        "qwen_triggered_segments": triggered,
        "qwen_always_on_segments": len(rows),
        "qwen_invocation_reduction": 1.0 - triggered / len(rows),
        "estimated_qwen_seconds_triggered": triggered * qwen_summary["mean_inference_seconds"],
        "estimated_qwen_seconds_always_on": len(rows) * qwen_summary["mean_inference_seconds"],
    }
    (qwen_root / "triggered_fusion_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
