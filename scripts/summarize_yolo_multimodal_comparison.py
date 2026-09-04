"""Build CSV and plots comparing YOLO skeleton routes with V-JEPA/Qwen fusion."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent


def load(path: str) -> dict:
    return json.loads((PROJECT / path).read_text(encoding="utf-8"))


def row(name: str, metric: dict, family: str, latency: float | None, note: str) -> dict[str, object]:
    return {"route": name, "family": family, "accuracy": metric["accuracy"], "precision": metric["precision"],
            "recall": metric["recall"], "specificity": metric["specificity"], "f1": metric["f1"],
            "balanced_accuracy": metric["balanced_accuracy"], "additional_video_ms": latency, "note": note}


def main() -> None:
    benchmark = load("results/benchmark_e300_full_summary.json")
    rows = [row(name, value["pooled_test"], "300-epoch skeleton baseline", 0.0,
                f"classifier {value['latency_ms_batch1_mean']:.2f} ms; pose frontend excluded")
            for name, value in benchmark.items()]
    vj_ms = load("results/vjepa21/gmdcsa24_vjepa21b_f16_features.summary.json")["mean_seconds_per_video"] * 1000
    qw_ms = load("results/qwen3vl_binary/fullvideo_temporal8/summary.json")["mean_inference_seconds"] * 1000
    additions = [
        ("YOLO-Pose + ST-GCN++ + V-JEPA feature fusion", "results/vjepa21/yolo_stgcnpp_feature_fusion_e300/summary.json", "oof_test", "V-JEPA fusion", vj_ms, "full-video 16-frame frozen features; head trained 300 epochs/fold"),
        ("YOLO-Pose + ST-GCN++ + V-JEPA score fusion", "results/vjepa21/yolo_stgcnpp_score_fusion/summary.json", "fused", "V-JEPA fusion", vj_ms, "fusion weight selected on validation fold"),
        ("YOLO-Pose + ST-GCN++ + Qwen weighted fusion", "results/qwen3vl_binary/yolo_stgcnpp_score_fusion/summary.json", "fused", "Qwen fusion", qw_ms, "self-reported Qwen confidence; validation-selected weight"),
        ("YOLO-Pose + ST-GCN++ + Qwen safety union", "results/qwen3vl_binary/yolo_stgcnpp_rule_fusion_summary.json", "safety_union", "Qwen fusion", qw_ms, "fixed OR rule; Qwen must run always or on a broader low-threshold trigger"),
        ("YOLO-Pose + ByteTrack + ST-GCN++ + V-JEPA feature fusion", "results/vjepa21/yolo_bytetrack_stgcnpp_feature_fusion_e300/summary.json", "oof_test", "V-JEPA fusion", vj_ms, "full-video 16-frame frozen features; head trained 300 epochs/fold"),
        ("YOLO-Pose + ByteTrack + ST-GCN++ + V-JEPA score fusion", "results/vjepa21/yolo_bytetrack_stgcnpp_score_fusion/summary.json", "fused", "V-JEPA fusion", vj_ms, "fusion weight selected on validation fold"),
        ("YOLO-Pose + ByteTrack + ST-GCN++ + Qwen weighted fusion", "results/qwen3vl_binary/yolo_bytetrack_stgcnpp_score_fusion/summary.json", "fused", "Qwen fusion", qw_ms, "validation selected skeleton only in every fold"),
        ("YOLO-Pose + ByteTrack + ST-GCN++ + Qwen safety union", "results/qwen3vl_binary/yolo_bytetrack_stgcnpp_rule_fusion_summary.json", "safety_union", "Qwen fusion", qw_ms, "fixed OR rule; recovers one additional fall without new false positive"),
        ("RTMPose + ST-GCN++ + V-JEPA suspicious-window score fusion", "results/vjepa21_suspicious/rtmpose_stgcnpp_score_fusion/summary.json", "fused", "Previous V-JEPA fusion", 517.26, "previous pose-selected suspicious-window experiment"),
    ]
    for name, path, key, family, latency, note in additions:
        payload = load(path); rows.append(row(name, payload[key], family, latency, note))
    rows.sort(key=lambda item: float(item["balanced_accuracy"]), reverse=True)
    output_root = PROJECT / "results/multimodal_route_comparison"; output_root.mkdir(parents=True, exist_ok=True)
    with (output_root / "all_binary_routes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

    requested_names = [
        "yolo+stgcnpp", "YOLO-Pose + ST-GCN++ + V-JEPA feature fusion",
        "YOLO-Pose + ST-GCN++ + V-JEPA score fusion", "YOLO-Pose + ST-GCN++ + Qwen weighted fusion",
        "YOLO-Pose + ST-GCN++ + Qwen safety union",
    ]
    labels = ["YOLO baseline", "+V-JEPA\nfeature", "+V-JEPA\nscore", "+Qwen\nweighted", "+Qwen\nunion"]
    selected = [{item["route"]: item for item in rows}[name] for name in requested_names]
    top = rows[:8]
    figure, axes = plt.subplots(1, 2, figsize=(19, 7))
    x = np.arange(len(selected)); width = 0.25
    for offset, key, title in ((-width, "balanced_accuracy", "Balanced accuracy"), (0, "recall", "Fall recall"), (width, "specificity", "Specificity")):
        bars = axes[0].bar(x + offset, [item[key] for item in selected], width, label=title)
        axes[0].bar_label(bars, labels=[f"{item[key]:.1%}" for item in selected], padding=2, fontsize=8)
    axes[0].set_xticks(x, labels); axes[0].set_ylim(0, 1.08); axes[0].grid(axis="y", alpha=0.2)
    axes[0].set(title="Requested YOLO-Pose + ST-GCN++ multimodal ablation", ylabel="Metric")
    axes[0].legend(fontsize=8)
    top_labels = [str(item["route"]).replace("YOLO-Pose", "YOLO").replace("ST-GCN++", "STGCN++") for item in reversed(top)]
    values = [float(item["balanced_accuracy"]) for item in reversed(top)]
    bars = axes[1].barh(top_labels, values, color=["#d1495b" if "Qwen safety union" in label else "#3977a8" for label in top_labels])
    axes[1].bar_label(bars, labels=[f"{value:.2%}" for value in values], padding=3)
    axes[1].set_xlim(0.75, 0.92); axes[1].grid(axis="x", alpha=0.2)
    axes[1].set(title="Top binary routes by balanced accuracy", xlabel="Balanced accuracy")
    figure.tight_layout(); figure.savefig(output_root / "yolo_multimodal_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(figure)
    (output_root / "top_routes.json").write_text(json.dumps(rows[:10], ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rows[:10], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
