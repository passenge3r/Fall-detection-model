# RTMPose + ST-GCN++ 最终系统演示

更新日期：2026-07-24

## 默认配置

- 姿态前端：RTMPose balanced。
- 分类器：四折 ST-GCN++ 概率平均。
- 权重：`results/sliding_window_e300_b64/rtmpose_stgcnpp/fold_*/best.pt`。
- 训练与部署均使用连续 64 帧窗口、16 帧步长。
- 平均概率阈值 0.5，至少 3/4 折同意，连续 3 个阳性窗口才确认。
- 姿态有效率低于 50% 时输出 `UNKNOWN`。

训练数据、受试者隔离指标和复现步骤见
[`SLIDING_WINDOW_TRAINING.md`](SLIDING_WINDOW_TRAINING.md)。

## 演示视频

跌倒片段：

`outputs/final_sliding_system/fall_subject1_01/annotated.mp4`

- 203 帧，9 个滑动窗口，零姿态帧为 0；
- 产生 1 次确认报警；
- 本次四任务并行复测速度约 7.21 FPS。

日常活动片段：

`outputs/final_sliding_system/adl_subject1_01/annotated.mp4`

- 245 帧，12 个滑动窗口，零姿态帧为 0；
- 全部窗口保持 `NORMAL`，确认报警为 0；
- 本次四任务并行复测速度约 7.26 FPS。

并行速度包含多个进程争用同一 GPU，不能代表单路部署吞吐量。

## 8 段整视频冒烟测试

| 类别 | 视频数 | 正确 | 错误 |
|---|---:|---:|---:|
| Fall | 4 | 4 次确认 | 0 次漏检 |
| ADL | 4 | 4 次无报警 | 0 次误报 |

测试片段为：

- Fall：S1/01、S2/12、S3/05、S4/08；
- ADL：S1/01、S2/01、S3/01、S4/01。

相较旧的均匀采样权重，新滑窗权重纠正了 S4 Fall 08 漏检和 S2 ADL 01
误报。8 段视频均无姿态缺失。

这只是系统流水线冒烟检查，不是无偏准确率：四折集成中的部分模型见过对应
Subject。正式模型性能以受试者隔离四折测试为准；设备到位后还需进行更大规模的
事件级现场测试。
