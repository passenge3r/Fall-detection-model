# 跌倒检测模型路线扩展对比（固定 300 轮）

更新日期：2026-07-22

## 结论

- **当前稳健单路线首选：RTMPose + ST-GCN++**。GMDCSA24 主体隔离四折 Balanced Accuracy（BA）为 **86.83%**，MCFD 未见场景固定阈值外测 BA 为 **63.08%**。它不是单项最高，但内部和跨数据集表现最均衡。
- **内部集最高：YOLO-Pose + ByteTrack + ST-GCN++**，内部 BA 为 **89.41%**；但 MCFD 外测 BA 仅 **61.75%**，且 GMDCSA24 跌倒片段的跟踪缺失显著更多，存在学习“跟踪丢失即跌倒”捷径的风险，暂不作为最终冠军。
- **高召回候选：RTMPose + PoseC3D-style**。内部 Recall **89.87%**、F1 **86.59%**，但 MCFD 外测 BA 仅 **59.97%**。
- **跨数据集单项最高：YOLO-Pose + ST-GCN++**。MCFD 固定阈值 BA **64.01%**，但内部 BA 只有 **77.53%**，稳定性不如 RTMPose + ST-GCN++。
- RTMO 和 Hourglass52 均未进入前六，最高分别为 **78.15%** 和 **76.89% BA**，因此在内部筛选阶段淘汰，不再执行耗时的 MCFD 全量推理。

## 公平实验协议

- 训练/验证/测试：GMDCSA24，4 名受试者严格隔离四折；四折测试合并后覆盖全部 160 个视频且每个视频仅测试一次。
- 外部测试：MCFD，完全不参与训练；表中外测采用 cam2/4/5/6/7/8 共 415 个片段，固定阈值 0.5。
- 输入统一为 COCO-17，张量形状 `[N,3,64,17,1]`。
- 每个组合训练 4 折，每折固定 300 轮、无早停；每轮按验证 BA 保留 `best.pt`，结束后回载最优权重测试。
- 优化器 AdamW，学习率 `3e-4`，weight decay `1e-3`，dropout `0.5`，batch size 16，AMP。
- 共完成 **15 条路线 × 4 折 × 300 轮 = 18,000 epochs**。

## GMDCSA24 内部四折合并结果

| 排名 | 路线 | BA | F1 | Recall | Specificity |
|---:|---|---:|---:|---:|---:|
| 1 | YOLO-Pose + ByteTrack + ST-GCN++ | **89.41%** | **89.57%** | **92.41%** | 86.42% |
| 2 | RTMPose + ST-GCN++ | 86.83% | 86.27% | 83.54% | **90.12%** |
| 3 | RTMPose + PoseC3D-style | 86.29% | 86.59% | 89.87% | 82.72% |
| 4 | RTMPose + CTR-GCN | 83.15% | 83.23% | 84.81% | 81.48% |
| 5 | YOLO-Pose + ByteTrack + CTR-GCN | 83.13% | 83.02% | 83.54% | 82.72% |
| 6 | YOLO-Pose + ByteTrack + PoseC3D-style | 82.56% | 83.13% | 87.34% | 77.78% |
| 7 | YOLO-Pose + CTR-GCN | 78.79% | 79.27% | 82.28% | 75.31% |
| 8 | RTMO + ST-GCN++ | 78.15% | 78.26% | 79.75% | 76.54% |
| 9 | YOLO-Pose + ST-GCN++ | 77.53% | 77.78% | 79.75% | 75.31% |
| 10 | Hourglass52 + ST-GCN++ | 76.89% | 77.02% | 78.48% | 75.31% |
| 11 | RTMO + PoseC3D-style | 76.34% | 77.65% | 83.54% | 69.14% |
| 12 | Hourglass52 + CTR-GCN | 75.72% | 77.19% | 83.54% | 67.90% |
| 13 | YOLO-Pose + PoseC3D-style | 75.69% | 76.65% | 81.01% | 70.37% |
| 14 | RTMO + CTR-GCN | 73.13% | 72.96% | 73.42% | 72.84% |
| 15 | Hourglass52 + PoseC3D-style | 71.99% | 73.99% | 81.01% | 62.96% |

`PoseC3D-style` 是项目内实现：把归一化骨架渲染为时空热图体，再使用 3D 残差卷积分类。它保留 PoseC3D 的核心表示思想，但不是 MMAction2 官方 SlowOnly-R50 配置，报告中不得写成官方模型复现。

## MCFD 跨数据集固定阈值结果

RTMO 和 Hourglass52 在内部筛选中落后，未进入外测。其余九条路线如下：

| 路线 | 外测 BA | 外测 F1 |
|---|---:|---:|
| YOLO-Pose + ST-GCN++ | **64.01%** | **62.28%** |
| RTMPose + CTR-GCN | 63.48% | 61.38% |
| RTMPose + ST-GCN++ | 63.08% | 61.65% |
| YOLO-Pose + ByteTrack + ST-GCN++ | 61.75% | 61.31% |
| YOLO-Pose + CTR-GCN | 60.28% | 57.29% |
| YOLO-Pose + ByteTrack + PoseC3D-style | 60.22% | 56.61% |
| RTMPose + PoseC3D-style | 59.97% | 56.23% |
| YOLO-Pose + ByteTrack + CTR-GCN | 59.74% | 56.08% |
| YOLO-Pose + PoseC3D-style | 59.58% | 56.85% |

## ByteTrack 诊断

ByteTrack 是人物关联器，不是跌倒分类器。它位于 `YOLO-Pose → ByteTrack → 时序分类器` 中间。GMDCSA24 中普通 YOLO 缓存有 305 个零姿态帧，而 ByteTrack 主轨迹缓存有 1521 个零姿态帧；跌倒片段为 1233 个、ADL 为 288 个。模型很容易把跟踪中断当作类别信号。

MCFD 的 ByteTrack 主轨迹平均覆盖率只有 67.42%，零姿态帧为 11496/35328（32.54%）。内部高分未能转化为跨数据集优势，因此下一版若继续使用 ByteTrack，应保留多轨迹、加入轨迹插值/重识别，并对“骨架缺失模式”做消融。

## 其他候选的实测状态

| 候选 | 定位 | 本机实测状态 | 是否进入精度排名 |
|---|---|---|---|
| RTMO | 单阶段多人姿态 | 官方 ONNX 权重已下载，CUDA 冒烟与全量缓存通过，三种分类头已完成 300 轮四折训练 | 是 |
| ByteTrack | 多目标跟踪 | 已通过 Ultralytics `bytetrack.yaml` 完成 GMDCSA24/MCFD 全量缓存和三种分类头训练 | 是 |
| PoseC3D | 热图体动作分类 | 项目内 PoseC3D-style 已实现；完成五种姿态前端的内部训练，并纳入九路外测 | 是，但注明 style |
| OpenPose | 多人姿态 | 官方源码已拉取；本机缺少 CMake 和 MSVC，无法构建 Windows C++/CUDA 工程；许可证仅允许非商业研究 | 否 |
| AlphaPose | 多人姿态 | 官方源码已拉取；Windows 默认禁用多项 CUDA 扩展，依赖旧 `timm==0.1.20`、额外检测器/姿态权重；许可证仅允许非商业研究 | 否 |
| Stacked Hourglass | 姿态骨干 | 已建立隔离MMPose环境，官方Hourglass52-COCO完成CUDA全量缓存和三种分类头四折300轮训练；最高BA 76.89% | 是 |

未进入排名不等于精度一定差，而是当前没有在同一 COCO-17、同一帧采样、同一划分协议下得到可复现实测值。若确实要继续三种旧模型，应在独立 Conda/Docker 环境中输出统一 `.npz` 缓存，再复用本项目分类器；不要改动现有可复现环境。

## 最终建议

系统默认使用 **RTMPose + ST-GCN++**，同时保留 **YOLO-Pose + ST-GCN++** 作为跨视角对照。ByteTrack 只用于多人身份维持，不把“跟踪消失”直接作为跌倒证据；PoseC3D-style 作为高召回研究分支。下一轮比继续堆叠旧姿态模型更重要的是：设备现场数据、困难负样本、多人轨迹修复、滑动窗口事件级指标与跨数据集微调。

原始汇总文件：

- `results/benchmark_e300_full_summary.csv`
- `results/benchmark_e300_full/learning_curve_comparison.png`
- `results/mcfd_external_e300_full/summary.csv`
