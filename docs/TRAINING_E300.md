# 300轮上限与早停实验

## 实验设置

- 三条路线：RTMPose + ST-GCN++、YOLO-Pose + ST-GCN++、YOLO-Pose + CTR-GCN。
- 数据：GMDCSA24，共160段视频，沿用四折受试者独立划分。
- 最大训练轮数：300；早停耐心值：15。
- 最佳模型：验证集 Balanced Accuracy 最高的 epoch。
- 其余参数不变：batch size 16、AdamW、学习率 3e-4、weight decay 1e-3、dropout 0.5、AMP。
- 学习率仍采用 CosineAnnealingLR，`T_max=300`。

## 实际训练轮数

| 路线 | Fold 1 | Fold 2 | Fold 3 | Fold 4 |
|---|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | 最优39 / 运行54 | 最优12 / 运行27 | 最优15 / 运行30 | 最优6 / 运行21 |
| YOLO-Pose + ST-GCN++ | 最优13 / 运行28 | 最优15 / 运行30 | 最优13 / 运行28 | 最优8 / 运行23 |
| YOLO-Pose + CTR-GCN | 最优40 / 运行55 | 最优6 / 运行21 | 最优7 / 运行22 | 最优13 / 运行28 |

所有折均由早停结束，实际只运行21～55轮，说明300轮上限已经足够。

## 四折合并内部测试结果

| 路线 | Accuracy | Precision | Recall | Specificity | F1 | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | 85.63% | 87.84% | 82.28% | 88.89% | 84.97% | 85.58% |
| YOLO-Pose + ST-GCN++ | 79.38% | 77.38% | 82.28% | 76.54% | 79.75% | 79.41% |
| YOLO-Pose + CTR-GCN | 76.88% | 73.33% | 83.54% | 70.37% | 78.11% | 76.96% |

## 与80轮上限实验对比

| 路线 | 80轮 Balanced Accuracy | 300轮 Balanced Accuracy | 变化 |
|---|---:|---:|---:|
| RTMPose + ST-GCN++ | 86.83% | 85.58% | -1.25个百分点 |
| YOLO-Pose + ST-GCN++ | 78.81% | 79.41% | +0.60个百分点 |
| YOLO-Pose + CTR-GCN | 77.57% | 76.96% | -0.61个百分点 |

增加最大epoch没有带来一致提升。学习曲线显示训练损失持续下降，但不少折的验证损失较早开始波动或上升，属于小数据集上的过拟合。RTMPose + ST-GCN++仍然是三条路线中综合效果最好的路线。

需要注意，余弦退火的 `T_max` 随最大epoch从80变为300，学习率下降速度也发生了变化，因此本实验对比的是“完整训练配置”，不是只改变训练时间的严格单变量实验。

## 学习曲线文件

- `results/benchmark_e300/rtmpose_stgcnpp/learning_curves.png`
- `results/benchmark_e300/yolo_stgcnpp/learning_curves.png`
- `results/benchmark_e300/yolo_ctrgcn/learning_curves.png`
- `results/benchmark_e300/learning_curve_comparison.png`
- `results/benchmark_e300/training_summary.csv`
