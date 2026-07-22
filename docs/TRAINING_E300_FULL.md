# 固定300轮、无早停实验

## 实验设置

- 三条路线、四折受试者独立划分，共12次训练。
- 每次训练固定运行300轮，总计3600个epoch，不触发早停。
- 每轮继续计算验证集 Balanced Accuracy，指标创新高时覆盖保存 `best.pt`。
- 训练结束后回载 `best.pt`，再计算验证集和内部测试集指标。
- 其余超参数保持不变：batch size 16、AdamW、学习率3e-4、weight decay 1e-3、dropout 0.5、CosineAnnealingLR `T_max=300`、AMP。
- 总训练耗时约46分钟，使用NVIDIA RTX 4060 Laptop GPU。

## 最优epoch

| 路线 | Fold 1 | Fold 2 | Fold 3 | Fold 4 |
|---|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | 59 | 12 | 15 | 6 |
| YOLO-Pose + ST-GCN++ | 91 | 15 | 100 | 8 |
| YOLO-Pose + CTR-GCN | 40 | 6 | 76 | 185 |

全部 `history.csv` 均包含300轮。最优epoch跨度为6～185，说明固定15轮耐心值会在部分折中过早结束，但后期新高并不一定改善未知受试者测试结果。

## 四折合并内部测试结果

| 路线 | Accuracy | Precision | Recall | Specificity | F1 | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | 86.88% | 89.19% | 83.54% | 90.12% | 86.27% | 86.83% |
| YOLO-Pose + ST-GCN++ | 77.50% | 75.90% | 79.75% | 75.31% | 77.78% | 77.53% |
| YOLO-Pose + CTR-GCN | 78.75% | 76.47% | 82.28% | 75.31% | 79.27% | 78.79% |

## 三种训练制度对比

以下均为四折合并测试集 Balanced Accuracy：

| 路线 | 80轮上限+早停 | 300轮上限+早停 | 固定300轮 |
|---|---:|---:|---:|
| RTMPose + ST-GCN++ | 86.83% | 85.58% | 86.83% |
| YOLO-Pose + ST-GCN++ | 78.81% | 79.41% | 77.53% |
| YOLO-Pose + CTR-GCN | 77.57% | 76.96% | 78.79% |

固定300轮对CTR-GCN略有帮助，但没有一致改善三条路线。RTMPose + ST-GCN++仍是整体最佳路线。完整曲线显示训练损失通常在前几十轮快速下降，此后验证指标长期震荡；因此工程训练仍建议保留早停，但应把耐心值从15提高到约30～50，或配合更稳定的学习率策略，而不是常规跑满300轮。

## 结果文件

- `results/benchmark_e300_full/rtmpose_stgcnpp/learning_curves.png`
- `results/benchmark_e300_full/yolo_stgcnpp/learning_curves.png`
- `results/benchmark_e300_full/yolo_ctrgcn/learning_curves.png`
- `results/benchmark_e300_full/learning_curve_comparison.png`
- `results/benchmark_e300_full/training_summary.csv`
- `results/benchmark_e300_full_summary.csv`
