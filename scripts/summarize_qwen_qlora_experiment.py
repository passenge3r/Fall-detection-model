"""Summarize the Qwen3-VL QLoRA experiment and aligned MCFD comparisons."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from train_qwen3vl_qlora import classification_metrics


ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "results/qwen3vl_qlora/gmd_subject123_37_f16_r16_e3"
BASE = ROOT / "results/qwen3vl_qlora/mcfd192_base_f16"
ADAPTER = ROOT / "results/qwen3vl_qlora/mcfd192_best_adapter_f16"
OUT = ROOT / "results/qwen3vl_qlora/comparison"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    qlora = read(ADAPTER / "predictions.csv"); keys = {r["sample"] for r in qlora}
    base = {r["sample"]: r for r in read(BASE / "predictions.csv")}
    old = {r["sample"]: r for r in read(ROOT / "results/qwen3vl_external/mcfd_temporal8/predictions.csv")}
    skeleton = {r["sample"]: r for r in read(ROOT / "results/mcfd_external_e300_full/yolo_stgcnpp/predictions.csv")}
    assert keys <= base.keys() and keys <= old.keys() and keys <= skeleton.keys()
    y = [int(r["label"]) for r in qlora]
    preds = {
        "Qwen base, structured prompt (16f)": [int(base[r["sample"]]["prediction"]) for r in qlora],
        "Qwen zero-shot, FALL/SAFE prompt (8f)": [int(old[r["sample"]]["prediction"]) for r in qlora],
        "Qwen + QLoRA, structured prompt (16f)": [int(r["prediction"]) for r in qlora],
        "YOLO-Pose + ST-GCN++": [int(skeleton[r["sample"]]["prediction_0p5"]) for r in qlora],
    }
    preds["Skeleton + zero-shot Qwen OR"] = [max(a, b) for a, b in zip(
        preds["YOLO-Pose + ST-GCN++"], preds["Qwen zero-shot, FALL/SAFE prompt (8f)"])]
    preds["Skeleton + QLoRA Qwen OR"] = [max(a, b) for a, b in zip(
        preds["YOLO-Pose + ST-GCN++"], preds["Qwen + QLoRA, structured prompt (16f)"])]
    rows = [{"route": name, **classification_metrics(y, pred)} for name, pred in preds.items()]
    rows.sort(key=lambda r: r["balanced_accuracy"], reverse=True)
    with (OUT / "aligned_mcfd192_comparison.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(10, 5.5)); labels = [r["route"] for r in rows]
    y_pos = list(range(len(rows))); width = .25
    ax.barh([i + width for i in y_pos], [100*r["balanced_accuracy"] for r in rows], width, label="Balanced accuracy")
    ax.barh(y_pos, [100*r["recall"] for r in rows], width, label="Fall recall")
    ax.barh([i - width for i in y_pos], [100*r["specificity"] for r in rows], width, label="Specificity")
    ax.set_yticks(y_pos, labels); ax.invert_yaxis(); ax.set_xlim(0, 105); ax.set_xlabel("Percent (%)")
    ax.set_title("Qwen3-VL QLoRA: aligned MCFD-192 external comparison"); ax.grid(axis="x", alpha=.2)
    ax.legend(ncol=3, loc="lower right"); fig.tight_layout(); fig.savefig(OUT / "mcfd192_comparison.png", dpi=180); plt.close(fig)

    history = read(TRAIN / "history.csv"); q = next(r for r in rows if r["route"].startswith("Qwen + QLoRA"))
    z = next(r for r in rows if r["route"].startswith("Qwen zero-shot")); b = next(r for r in rows if r["route"].startswith("Qwen base"))
    report = f"""# Qwen3-VL-2B + QLoRA 跌倒识别实跑报告（2026-08-05）

## 实验设置

- 数据隔离：GMDCSA24 Subject 1–3 共 123 条训练，Subject 4 共 37 条验证；MCFD 不参与训练或选轮次。
- QLoRA：4-bit NF4、double quantization、LoRA rank 16、alpha 32，仅语言模型 `q_proj/v_proj`，可训练参数 3,211,264。
- 输入：每条视频均匀抽取 16 帧，每帧最大 32,768 像素；batch size 1，梯度累积 4，共 3 轮。
- 外部测试：MCFD 摄像机 2/4/5/6/7/8 固定平衡子集 192 段，96 fall + 96 safe，随机种子 20260805。

## 训练结果

| 轮次 | 训练损失 | 验证 Macro-F1 | 验证平衡准确率 | 跌倒召回率 | 特异度 |
|---:|---:|---:|---:|---:|---:|
"""
    for r in history:
        report += f"| {r['epoch']} | {float(r['train_loss']):.4f} | {100*float(r['macro_f1']):.2f}% | {100*float(r['balanced_accuracy']):.2f}% | {100*float(r['recall']):.2f}% | {100*float(r['specificity']):.2f}% |\n"
    report += f"""

第1轮与第2轮验证 Macro-F1 同为 86.45%；按同分取更早轮次的规则选择第1轮，避免使用外部测试集选模型。第3轮下降，已出现轻微过拟合。

![训练曲线](../gmd_subject123_37_f16_r16_e3/learning_curve.png)

## MCFD-192 对齐外部测试

| 路线 | Macro-F1 | 平衡准确率 | 召回率 | 特异度 | 解析错误 |
|---|---:|---:|---:|---:|---:|
"""
    for r in rows:
        report += f"| {r['route']} | {100*r['macro_f1']:.2f}% | {100*r['balanced_accuracy']:.2f}% | {100*r['recall']:.2f}% | {100*r['specificity']:.2f}% | {r['parse_errors']} |\n"
    report += f"""

![外部测试对比](mcfd192_comparison.png)

## 判断

1. QLoRA 将结构化提示下的解析错误从 {b['parse_errors']} 降到 {q['parse_errors']}，外部 Macro-F1 从 {100*b['macro_f1']:.2f}% 提升到 {100*q['macro_f1']:.2f}%，证明它有效学习了任务格式和判定指令。
2. 但同一 MCFD-192 上，专用 `FALL/SAFE` 零样本提示的平衡准确率为 {100*z['balanced_accuracy']:.2f}%，仍高于 QLoRA 的 {100*q['balanced_accuracy']:.2f}%。本次 QLoRA 没有提升跨数据集分类泛化。
3. QLoRA 输出的原因基本是训练模板复述，不是样本级事实解释；现有二分类标签无法监督更细的动作阶段、方向、倒地后状态或具体原因。
4. 当前适配器适合用于稳定输出接口的原型，不应替换零样本 Qwen 或现有融合冠军。若继续，应先构建人工核验的多类别/事件阶段/个性化理由标注，再训练并做概率校准。
5. 数值置信度本轮不输出：`FALL` 与 `SAFE` 的 token 长度不同，未经序列概率归一化和验证集校准的单 token softmax 会有系统偏差。
"""
    (ROOT / "docs/Qwen3VL_QLoRA跌倒识别实跑_20260805.md").write_text(report, encoding="utf-8")
    for r in rows: print(r["route"], r["balanced_accuracy"], r["macro_f1"])


if __name__ == "__main__": main()
