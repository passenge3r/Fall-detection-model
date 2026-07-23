# 跌倒检测 21 路正交网格 + 2 路跟踪消融（固定 300 轮）

更新日期：2026-07-23

## 结论

- **GMDCSA24 内部冠军：YOLO-Pose + ByteTrack + ST-GCN++**，主体隔离四折合并 Balanced Accuracy（BA）为 **89.41%**。但它在 MCFD 外测只有 61.75% BA，且跟踪缺失存在类别偏置，不能直接作为稳健系统冠军。
- **当前稳健单路线首选：RTMPose + ST-GCN++**。内部 BA **86.83%**，MCFD 未见场景固定阈值外测 BA **63.08%**，内部与跨数据集表现最均衡。
- **新增 RTMPose + ByteTrack + ST-GCN++** 内部 BA 为 **86.29%**，并列第 3。它提高了 RTMPose 的 Recall（83.54% → 89.87%），但降低 Specificity（90.12% → 82.72%），总体 BA 仍比不加跟踪的 RTMPose + ST-GCN++ 低 0.54 个百分点。
- **ByteTrack v2** 用同帧 RTMPose 回接和短间隔插值把全零骨架帧从 1518 降为 0，但 BA 只有 **84.32%**、排名第 5。逐帧在“主轨姿态”和“无跟踪姿态”之间切换仍会引入时序不连续，修复缺失不等于提升分类。
- 在原 21 路正交网格中，新增姿态前端最好的是 AlphaPose + ST-GCN++，内部 BA **79.43%**。
- **OpenPose 最好搭配 CTR-GCN**，内部 BA **76.32%**；OpenPose + PoseC3D-style 最低，为 69.36%。
- 分类头不存在对所有前端都占优的绝对赢家：ST-GCN++ 在 5/7 个前端变体上最好；YOLO-Pose 与 OpenPose 更适合 CTR-GCN；RTMPose 的 PoseC3D-style 接近但仍低于其 ST-GCN++。

## 正交组合范围

核心实验统一比较 7 个姿态/跟踪前端与 3 个时序分类器，共 21 条路线；随后增加原始 `RTMPose + ByteTrack + ST-GCN++` 和丢轨回接 v2 两条消融，总计 23 条实测路线：

- 前端：RTMPose、YOLO-Pose、YOLO-Pose + ByteTrack、RTMO、Hourglass52、OpenPose、AlphaPose。
- 分类器：ST-GCN++、CTR-GCN、PoseC3D-style。
- ByteTrack 是人物关联器，不是分类器，因此作为 `YOLO-Pose + ByteTrack` 前端变体参与网格，而不是与每个底层姿态热图网络机械串联。

## 公平实验协议

- 数据集：GMDCSA24，4 名受试者严格隔离四折；四折测试合并覆盖全部 160 个视频，每个视频仅测试一次。
- 输入统一为 COCO-17，形状 `[N,3,64,17,1]`；每段均匀采样 64 帧。
- 每条路线训练 4 折，每折完整 300 轮、无早停；按验证集 BA 保存并回载 `best.pt`。
- AdamW，学习率 `3e-4`，weight decay `1e-3`，dropout `0.5`，batch size 16，AMP。
- 总训练量：**23 路 × 4 折 × 300 轮 = 27,600 epochs**，共 92 个最优折模型。
- OpenPose 使用由 CMU COCO Caffe 权重直接转换的 PyTorch 端口，在共享 YOLO 单人框内以 256×256 输入推理，并将 COCO-18 去除 neck 后映射到 COCO-17。
- AlphaPose 使用官方 FastPose-ResNet50、COCO 256×192 权重；与 Hourglass/OpenPose 共用同一 YOLO 单人框协议。

## GMDCSA24 四折合并总排名

完整 23 路的 Accuracy、Precision、Recall、Specificity、F1、BA 和 TP/TN/FP/FN 见 [`ALL_ROUTE_METRICS.md`](ALL_ROUTE_METRICS.md)。前三名为：

| 排名 | 路线 | BA | F1 | Recall | Specificity |
|---:|---|---:|---:|---:|---:|
| 1 | YOLO-Pose + ByteTrack + ST-GCN++ | **89.41%** | **89.57%** | **92.41%** | 86.42% |
| 2 | RTMPose + ST-GCN++ | 86.83% | 86.27% | 83.54% | **90.12%** |
| 3 | RTMPose + ByteTrack + ST-GCN++ | 86.29% | 86.59% | 89.87% | 82.72% |
| 3 | RTMPose + PoseC3D-style | 86.29% | 86.59% | 89.87% | 82.72% |

`PoseC3D-style` 是项目内实现：把归一化骨架渲染为时空热图体，再用 3D 残差卷积分类。它保留 PoseC3D 的核心表示思想，但不是 MMAction2 官方 SlowOnly-R50 配置。

## 每个分类头的最佳前端

| 分类头 | 最佳前端 | BA |
|---|---|---:|
| ST-GCN++ | YOLO-Pose + ByteTrack | **89.41%** |
| CTR-GCN | RTMPose | **83.15%** |
| PoseC3D-style | RTMPose | **86.29%** |

## 外部测试与筛选规则

MCFD 完全不参与训练。此前进入外测的九条路线中，固定阈值 0.5 的最佳 BA 是 YOLO-Pose + ST-GCN++ 的 64.01%，RTMPose + ST-GCN++ 为 63.08%。ByteTrack 内部冠军外测为 61.75%，说明内部最高不等于跨数据集最稳健。

OpenPose 与 AlphaPose 的六条新增路线均未进入内部前六，因此按预先采用的“两阶段筛选”规则暂不进行耗时的 MCFD 全量姿态提取，不能声称它们的跨数据集性能已经测得。

## 工程建议

1. 默认系统路线继续使用 **RTMPose + ST-GCN++**。
2. 保留 **YOLO-Pose + ByteTrack + ST-GCN++** 作为内部高分研究分支，但修复跟踪丢失偏置后再考虑上线。
3. 若需要互补实验，优先比较 RTMPose + ST-GCN++ 与 YOLO-Pose + ST-GCN++ 的概率融合；AlphaPose + ST-GCN++ 可作为第三姿态前端，但当前没有单模型精度优势。
4. 下一阶段优先采集设备现场数据，并报告事件级误报率、漏报率、报警延迟与跨场景性能，而不是继续扩大旧姿态模型数量。

原始产物：

- `results/benchmark_e300_full_summary.csv`
- `results/benchmark_e300_full_summary.json`
- `results/benchmark_e300_full/learning_curve_comparison.png`
- `results/benchmark_e300_full/<route>/learning_curves.png`
