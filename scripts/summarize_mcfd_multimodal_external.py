from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "multimodal_external_comparison"
CROSS_VIEW = {2, 4, 5, 6, 7, 8}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def metrics(y: np.ndarray, p: np.ndarray) -> dict:
    tp = int(((y == 1) & (p == 1)).sum())
    tn = int(((y == 0) & (p == 0)).sum())
    fp = int(((y == 0) & (p == 1)).sum())
    fn = int(((y == 1) & (p == 0)).sum())
    recall = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    return {
        "samples": int(len(y)), "accuracy": float((p == y).mean()),
        "balanced_accuracy": (recall + specificity) / 2,
        "precision": precision, "recall": recall, "specificity": specificity,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def evaluate_pair(name: str, path: Path, qwen_by_sample: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    aligned, y, skeleton, qwen = [], [], [], []
    for row in read_csv(path):
        if int(row["camera"]) not in CROSS_VIEW or row["sample"] not in qwen_by_sample:
            continue
        q = qwen_by_sample[row["sample"]]
        assert int(row["label"]) == int(q["label"])
        aligned.append({**row, "qwen_prediction": q["prediction"], "qwen_raw_output": q["raw_output"]})
        y.append(int(row["label"]))
        skeleton.append(int(row["prediction_0p5"]))
        qwen.append(int(q["prediction"]))
    y_a, s_a, q_a = map(lambda x: np.asarray(x, dtype=int), (y, skeleton, qwen))
    variants = {
        name: s_a,
        "Qwen3-VL zero-shot": q_a,
        f"{name} + Qwen OR": np.maximum(s_a, q_a),
        f"{name} + Qwen AND": np.minimum(s_a, q_a),
    }
    rows = [{"route": route, **metrics(y_a, pred)} for route, pred in variants.items()]
    return aligned, rows


def pct(v: float) -> str:
    return f"{100*v:.2f}%"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    qwen_dir = ROOT / "results" / "qwen3vl_external" / "mcfd_temporal8"
    qwen_rows = read_csv(qwen_dir / "predictions.csv")
    qwen_by_sample = {r["sample"]: r for r in qwen_rows}
    base = ROOT / "results" / "mcfd_external_e300_full"
    pairs = [
        ("YOLO-Pose + ST-GCN++", base / "yolo_stgcnpp" / "predictions.csv"),
        ("YOLO-Pose + ByteTrack + ST-GCN++", base / "yolo_bytetrack_stgcnpp" / "predictions.csv"),
    ]
    all_rows: list[dict] = []
    for name, path in pairs:
        aligned, rows = evaluate_pair(name, path, qwen_by_sample)
        write_csv(OUT / ("aligned_" + path.parent.name + ".csv"), aligned)
        all_rows.extend(rows)

    unique = {row["route"]: row for row in all_rows}
    for short, label in [
        ("yolo_stgcnpp", "YOLO-Pose + ST-GCN++ + V-JEPA feature"),
        ("yolo_bytetrack_stgcnpp", "YOLO-Pose + ByteTrack + ST-GCN++ + V-JEPA feature"),
    ]:
        obj = json.loads((ROOT / "results" / "vjepa21_external" /
                          f"{short}_feature_fusion_result.json").read_text(encoding="utf-8"))
        unique[label] = {"route": label, **obj["fixed_0p5"]["cross_view_test"]}
    result = sorted(unique.values(), key=lambda r: float(r["balanced_accuracy"]), reverse=True)
    write_csv(OUT / "all_mcfd_routes.csv", result)
    (OUT / "fusion_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    internal_rows = read_csv(ROOT / "results" / "multimodal_route_comparison" / "all_binary_routes.csv")
    internal = {r["route"]: float(r["balanced_accuracy"]) for r in internal_rows}
    aliases = {
        "YOLO-Pose + ST-GCN++": "yolo+stgcnpp",
        "YOLO-Pose + ST-GCN++ + V-JEPA feature": "YOLO-Pose + ST-GCN++ + V-JEPA feature fusion",
        "YOLO-Pose + ST-GCN++ + Qwen OR": "YOLO-Pose + ST-GCN++ + Qwen safety union",
        "YOLO-Pose + ByteTrack + ST-GCN++": "yolo_bytetrack+stgcnpp",
        "YOLO-Pose + ByteTrack + ST-GCN++ + V-JEPA feature": "YOLO-Pose + ByteTrack + ST-GCN++ + V-JEPA feature fusion",
        "YOLO-Pose + ByteTrack + ST-GCN++ + Qwen OR": "YOLO-Pose + ByteTrack + ST-GCN++ + Qwen safety union",
    }
    selected = []
    for row in result:
        if row["route"] in aliases:
            selected.append({**row, "internal": internal[aliases[row["route"]]]})
    selected.sort(key=lambda r: r["internal"], reverse=True)
    write_csv(OUT / "internal_external_selected.csv", selected)

    labels = [r["route"].replace("YOLO-Pose + ", "") for r in selected]
    positions = np.arange(len(selected))
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.barh(positions + .18, [r["internal"] * 100 for r in selected], height=.34,
            label="GMDCSA24 internal LOSO")
    ax.barh(positions - .18, [r["balanced_accuracy"] * 100 for r in selected], height=.34,
            label="MCFD external cross-view")
    ax.set_yticks(positions, labels)
    ax.invert_yaxis(); ax.set_xlim(50, 95)
    ax.set_xlabel("Balanced accuracy (%)")
    ax.set_title("Internal validation vs external cross-view validation")
    ax.grid(axis="x", alpha=.25); ax.legend(loc="lower right")
    for i, row in enumerate(selected):
        ax.text(row["internal"] * 100 + .3, i + .18, f'{row["internal"]*100:.1f}', va="center", fontsize=8)
        ax.text(row["balanced_accuracy"] * 100 + .3, i - .18,
                f'{row["balanced_accuracy"]*100:.1f}', va="center", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "internal_external_comparison.png", dpi=180); plt.close(fig)

    lookup = {r["route"]: r for r in result}
    q, top = lookup["Qwen3-VL zero-shot"], result[0]
    qwen_summary = json.loads((qwen_dir / "summary.json").read_text(encoding="utf-8"))
    report = f"""# 多模态跌倒检测路线：MCFD 外部验证（2026-08-04）

## 验证协议

- 训练来源：GMDCSA24；MCFD 不参与模型训练。
- 外部正式测试：MCFD 摄像机 2、4、5、6、7、8，共 415 个标注片段；摄像机 1 仅作开发参考，摄像机 3 不计入正式测试。
- 骨架与 V-JEPA 路线使用固定 0.5 阈值；Qwen3-VL 使用固定提示词，将每个 31 帧事件片段均匀采样为 8 帧，只输出 `FALL` 或 `SAFE`。
- Qwen3-VL 共完成 484 个开发/测试片段，解析错误 0，平均推理 {qwen_summary['mean_inference_seconds']:.3f} 秒/片段。

## 正式跨视角结果

| 路线 | 平衡准确率 | 召回率 | 特异度 | 精确率 | F1 |
|---|---:|---:|---:|---:|---:|
"""
    for row in result:
        report += (f'| {row["route"]} | {pct(row["balanced_accuracy"])} | {pct(row["recall"])} | '
                   f'{pct(row["specificity"])} | {pct(row["precision"])} | {pct(row["f1"])} |\n')
    report += f"""

## 结论

1. 外部测试当前最高路线是 **{top['route']}**，平衡准确率 **{pct(top['balanced_accuracy'])}**。
2. Qwen3-VL 单路平衡准确率为 **{pct(q['balanced_accuracy'])}**，精确率 **{pct(q['precision'])}**、特异度 **{pct(q['specificity'])}**，但召回率仅 **{pct(q['recall'])}**。它擅长确认明显跌倒，但不适合单独负责漏检敏感的实时告警。
3. ByteTrack 路线内部平衡准确率较高，但在 MCFD 跨视角测试中下降明显，说明跟踪与骨架序列对摄像机视角、遮挡和数据分布敏感，内部冠军不能直接视为最终路线。
4. V-JEPA 特征融合在无跟踪 YOLO 路线上带来小幅外部增益；在 ByteTrack 路线上没有改善。多模态模块不是稳定的“即插即涨点”，需要按前端路线分别验证。
5. 推荐下一轮保留三条候选：Qwen3-VL 单路作为高置信确认器、YOLO-Pose + ST-GCN++ + V-JEPA 作为低成本连续筛查、以及两路的可学习/分级融合。现阶段不建议把简单 OR 或 AND 规则直接定为最终方案。

![内部与外部结果对比](../results/multimodal_external_comparison/internal_external_comparison.png)
"""
    (ROOT / "docs" / "多模态路线MCFD外部验证_20260804.md").write_text(report, encoding="utf-8")
    for row in result:
        print(f'{row["route"]}: BA={pct(row["balanced_accuracy"])}, R={pct(row["recall"])}, S={pct(row["specificity"])}')


if __name__ == "__main__":
    main()
