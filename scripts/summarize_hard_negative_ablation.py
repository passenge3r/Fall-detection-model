from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
BASELINE_INTERNAL = PROJECT / "results/sliding_window_e300_b64/rtmpose_stgcnpp"
HARDNEG_INTERNAL = PROJECT / "results/sliding_window_hardneg_e300_b64/rtmpose_stgcnpp"
BASELINE_EXTERNAL = PROJECT / "results/mcfd_external_sliding_e300_b64/rtmpose_stgcnpp/result.json"
HARDNEG_EXTERNAL = PROJECT / "results/mcfd_external_hardneg_e300_b64/rtmpose_stgcnpp/result.json"
OUTPUT = PROJECT / "results/hard_negative_ablation"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def calculate(rows: list[dict[str, str]]) -> dict[str, float | int]:
    labels = [int(row["label"]) for row in rows]
    predictions = [int(row["prediction"]) for row in rows]
    tp = sum(label == 1 and prediction == 1 for label, prediction in zip(labels, predictions))
    tn = sum(label == 0 and prediction == 0 for label, prediction in zip(labels, predictions))
    fp = sum(label == 0 and prediction == 1 for label, prediction in zip(labels, predictions))
    fn = sum(label == 1 and prediction == 0 for label, prediction in zip(labels, predictions))
    safe = lambda a, b: a / b if b else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "samples": len(rows),
        "accuracy": safe(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def internal(root: Path) -> tuple[dict[str, float | int], list[int]]:
    rows: list[dict[str, str]] = []
    best_epochs = []
    for fold in range(1, 5):
        fold_dir = root / f"fold_{fold}"
        rows.extend(read_csv(fold_dir / "test_predictions.csv"))
        metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
        if metrics["epochs_ran"] != 300:
            raise RuntimeError(f"Fold {fold} did not run 300 epochs")
        best_epochs.append(int(metrics["best_epoch"]))
    return calculate(rows), best_epochs


def external(path: Path, mode: str) -> dict[str, float | int]:
    result = json.loads(path.read_text(encoding="utf-8"))
    group = "groups_fixed_0p5" if mode == "fixed_0p5" else "groups_calibrated"
    output = dict(result[group]["cross_view_test"])
    output["selected_threshold"] = (
        0.5 if mode == "fixed_0p5" else result["threshold_selection"]["selected"]
    )
    return output


def delta(after: dict[str, float | int], before: dict[str, float | int]) -> dict[str, float | int]:
    return {key: after[key] - before[key] for key in before if key in after}


def pct(value: float | int) -> str:
    return f"{100 * float(value):.2f}%"


def main() -> None:
    baseline_internal, baseline_epochs = internal(BASELINE_INTERNAL)
    hardneg_internal, hardneg_epochs = internal(HARDNEG_INTERNAL)
    baseline_fixed = external(BASELINE_EXTERNAL, "fixed_0p5")
    hardneg_fixed = external(HARDNEG_EXTERNAL, "fixed_0p5")
    baseline_cal = external(BASELINE_EXTERNAL, "calibrated")
    hardneg_cal = external(HARDNEG_EXTERNAL, "calibrated")
    summary = {
        "protocol": {
            "route": "RTMPose + ST-GCN++",
            "epochs": 300,
            "early_stopping": False,
            "hard_negative_threshold": 0.8,
            "extra_copies": 2,
            "validation_and_test_unchanged": True,
        },
        "internal": {
            "baseline": baseline_internal,
            "hard_negative": hardneg_internal,
            "delta": delta(hardneg_internal, baseline_internal),
            "baseline_best_epochs": baseline_epochs,
            "hard_negative_best_epochs": hardneg_epochs,
        },
        "mcfd_cross_view_fixed_0p5": {
            "baseline": baseline_fixed,
            "hard_negative": hardneg_fixed,
            "delta": delta(hardneg_fixed, baseline_fixed),
        },
        "mcfd_cross_view_calibrated": {
            "baseline": baseline_cal,
            "hard_negative": hardneg_cal,
            "delta": delta(hardneg_cal, baseline_cal),
        },
        "decision": (
            "Do not replace the balanced default. The ablation improves recall and F1 at "
            "threshold 0.5, but increases false positives and slightly reduces accuracy/AUC. "
            "Retain it as a high-recall candidate."
        ),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    markdown = f"""# 困难负样本重训练消融

更新日期：2026-08-01

## 实验设计

- 路线：RTMPose + ST-GCN++；4折，每折固定训练300轮，不早停。
- 从原滑窗模型的折外预测中选择跌倒概率不低于0.8的ADL窗口，共110个。
- 每个困难窗口仅在其主体属于训练集的折中增加2份训练副本。
- 验证集、内部测试集和MCFD外部测试集均不改变；MCFD没有加入训练。

## 结果

| 数据与指标 | 原滑窗模型 | 困难负样本模型 | 变化 |
|---|---:|---:|---:|
| GMDCSA24 Accuracy | {pct(baseline_internal['accuracy'])} | {pct(hardneg_internal['accuracy'])} | {pct(hardneg_internal['accuracy']-baseline_internal['accuracy'])} |
| GMDCSA24 Recall | {pct(baseline_internal['recall'])} | {pct(hardneg_internal['recall'])} | {pct(hardneg_internal['recall']-baseline_internal['recall'])} |
| GMDCSA24 Specificity | {pct(baseline_internal['specificity'])} | {pct(hardneg_internal['specificity'])} | {pct(hardneg_internal['specificity']-baseline_internal['specificity'])} |
| GMDCSA24 F1 | {pct(baseline_internal['f1'])} | {pct(hardneg_internal['f1'])} | {pct(hardneg_internal['f1']-baseline_internal['f1'])} |
| GMDCSA24 Balanced Accuracy | {pct(baseline_internal['balanced_accuracy'])} | {pct(hardneg_internal['balanced_accuracy'])} | {pct(hardneg_internal['balanced_accuracy']-baseline_internal['balanced_accuracy'])} |
| MCFD固定0.5 Accuracy | {pct(baseline_fixed['accuracy'])} | {pct(hardneg_fixed['accuracy'])} | {pct(hardneg_fixed['accuracy']-baseline_fixed['accuracy'])} |
| MCFD固定0.5 Recall | {pct(baseline_fixed['recall'])} | {pct(hardneg_fixed['recall'])} | {pct(hardneg_fixed['recall']-baseline_fixed['recall'])} |
| MCFD固定0.5 Specificity | {pct(baseline_fixed['specificity'])} | {pct(hardneg_fixed['specificity'])} | {pct(hardneg_fixed['specificity']-baseline_fixed['specificity'])} |
| MCFD固定0.5 F1 | {pct(baseline_fixed['f1'])} | {pct(hardneg_fixed['f1'])} | {pct(hardneg_fixed['f1']-baseline_fixed['f1'])} |

MCFD固定阈值0.5的混淆矩阵变化：FP {baseline_fixed['fp']}→{hardneg_fixed['fp']}，
FN {baseline_fixed['fn']}→{hardneg_fixed['fn']}。困难负样本模型少漏报12段，但多误报13段。

## 结论

本轮没有达到“降低误报”的原目标，但形成了一个更偏向召回的模型：MCFD F1提高
{100*(hardneg_fixed['f1']-baseline_fixed['f1']):.2f}个百分点、Recall提高
{100*(hardneg_fixed['recall']-baseline_fixed['recall']):.2f}个百分点；与此同时Specificity下降、
FP增加，Accuracy与ROC-AUC略降。因此暂不替换当前均衡主模型，可保留为“少漏报模式”候选。

下一轮应测试较弱的过采样（1份副本），或同时加入折外困难正样本，以寻找Recall与
Specificity更平衡的工作点。阈值校准也应与训练策略分开评估。
"""
    (OUTPUT / "README.md").write_text(markdown, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
