# V-JEPA 2.1 视频语义分支接入与融合实验

## 结论

已完成 V-JEPA 2.1-B 冻结视频编码器的接入、160 条 GMDCSA24 视频特征提取、
4 折受试者隔离分类，以及与 RTMPose + ST-GCN++ 的两种融合实验。

当前版本**不替换默认系统**。V-JEPA 单路具有一定识别能力，但简单融合没有超过
RTMPose + ST-GCN++；它更适合作为后续“疑似跌倒窗口语义复核器”，而不是直接对整段
视频给出跌倒概率。

## 路线原理

现有骨架路线只观察关键点随时间如何移动，优点是轻量、对背景不敏感，但看不到床、椅子、
地面和人与物体的交互。V-JEPA 2.1 直接读取 RGB 视频，输出包含动作和场景语义的特征。

本实验将两类模型都冻结，只训练很小的二分类头：

```text
RGB 视频 -- V-JEPA 2.1-B --> 768维视频语义特征 --┐
                                                   ├--> 小型融合分类头 --> ADL / Fall
关键点 -- RTMPose -- ST-GCN++ --> 256维骨架特征 ---┘
```

这样可以先验证视频语义是否真正补足骨架信息，避免在 160 条小数据集上微调 1 亿参数造成
严重过拟合。

## 实验协议

- 数据：GMDCSA24，160 条视频，81 条 ADL、79 条 Fall，4 名受试者。
- 划分：4 折 leave-one-subject-out；每折 1 人测试、下一人验证、其余 2 人训练。
- V-JEPA 输入：每条视频均匀取 16 帧，短边缩放至 384，再做 384×384 中心裁剪和
  ImageNet 归一化。
- V-JEPA 输出：最终 token 取均值，得到 768 维特征。
- 训练：分类探针或融合头训练 300 轮，不早停；按验证集选择最优轮次，测试集不参与调参。
- 冻结模型：V-JEPA 2.1-B 与既有 ST-GCN++ 均不更新参数。

模型权重来自 Meta 发布的 `vjepa2_1_vitb_dist_vitG_384.pt`，本地通过经过数值等价验证的
Transformers 格式转换加载。固定快照为 `ea7765861aa689985c593727725afa378fc87492`；
本地 `model.safetensors` SHA-256 为
`D9ADB48EEF8880A5F019F9FC577927B13793E4745AFD2B88E01747989894F806`。

## 结果

以下均为 160 条视频的四折 OOF 测试汇总，阈值固定为 0.5：

| 路线 | Accuracy | Precision | Recall | Specificity | F1 | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | **86.88%** | **89.19%** | 83.54% | **90.12%** | **86.27%** | **86.83%** |
| V-JEPA 2.1-B + 线性探针 | 70.63% | 67.78% | 77.22% | 64.20% | 72.19% | 70.71% |
| 验证集选权重的分数融合 | 78.13% | 72.00% | **91.14%** | 65.43% | 80.45% | 78.29% |
| 骨架特征 + V-JEPA 特征融合 | **86.88%** | **89.19%** | 83.54% | **90.12%** | **86.27%** | **86.83%** |

特征融合的四折都选择了 epoch 0，即保留原 ST-GCN++ 决策；后续训练轮次没有在验证集上
形成更好的融合头。分数融合提高了 Recall，但新增 20 个假阳性，F1 明显下降。

## 实际运行情况

- 160/160 条视频特征提取成功，失败 0 条。
- 特征矩阵：`160 × 768`。
- RTX 4060 Laptop 上总提取时间 114.30 秒，平均 0.714 秒/视频。
- 单样本提取阶段记录的 CUDA 峰值分配约 0.336 GiB（模型以 FP16 + SDPA 推理）。
- ST-GCN++ 新增 `forward_features()` 后的前向等价检查最大误差为 0，输出维度为 256。

## 结果文件

- 冻结特征：`results/vjepa21/gmdcsa24_vjepa21b_f16_features.npz`
- 提取摘要：`results/vjepa21/gmdcsa24_vjepa21b_f16_features.summary.json`
- V-JEPA 单路探针：`results/vjepa21/linear_probe_e300/`
- 分数融合：`results/vjepa21/rtmpose_stgcnpp_score_fusion/`
- 特征融合：`results/vjepa21/rtmpose_stgcnpp_feature_fusion_e300/`

## 复现命令

```powershell
python -m pip install -r requirements-vjepa.txt

python scripts/extract_vjepa21_features.py `
  --manifest data/metadata/gmdcsa24.csv `
  --video-root data/raw/GMDCSA24 `
  --output results/vjepa21/gmdcsa24_vjepa21b_f16_features.npz `
  --frames 16 --device cuda --dtype float16

python scripts/train_vjepa21_probe.py `
  --features results/vjepa21/gmdcsa24_vjepa21b_f16_features.npz `
  --output-root results/vjepa21/linear_probe_e300 --epochs 300

python scripts/evaluate_vjepa_skeleton_fusion.py `
  --skeleton-root results/benchmark_e300_full/rtmpose_stgcnpp `
  --vjepa-root results/vjepa21/linear_probe_e300 `
  --output-root results/vjepa21/rtmpose_stgcnpp_score_fusion

python scripts/train_vjepa_stgcnpp_feature_fusion.py `
  --skeleton-data data/gcn/gmdcsa24_rtmpose_t64.npz `
  --splits data/splits/gmdcsa24_loso `
  --skeleton-checkpoints results/benchmark_e300_full/rtmpose_stgcnpp `
  --vjepa-features results/vjepa21/gmdcsa24_vjepa21b_f16_features.npz `
  --output-root results/vjepa21/rtmpose_stgcnpp_feature_fusion_e300 `
  --epochs 300
```

首次下载模型时，在特征提取命令末尾加 `--allow-download`；下载完成后默认离线加载固定快照。

## 下一轮改进

1. 不再对整条视频均匀取帧；先由滑窗 ST-GCN++ 找到疑似跌倒区间，再截取区间前后多个
   16 帧 RGB 片段。
2. V-JEPA 只复核 `FALL_PENDING` 或骨架置信度接近阈值的窗口，不进入每帧主链路。
3. 用多片段的平均/最大/注意力聚合做消融，并重点统计 Subject 1 的 ADL 假阳性。
4. 只有内部 F1 不低于 86.27% 且假阳性不增加时，才进入 MCFD 外部测试和系统默认配置。

## 来源

- Meta 官方代码与模型说明：https://github.com/facebookresearch/vjepa2
- V-JEPA 2.1 论文：https://arxiv.org/abs/2603.14482
- 本实验使用的 Transformers 格式转换与数值验证：
  https://huggingface.co/apiantonio/vjepa2.1-vit-base-384

