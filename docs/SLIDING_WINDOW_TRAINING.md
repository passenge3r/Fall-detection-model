# 部署对齐的滑窗训练

更新日期：2026-07-24

## 结论

系统默认模型已切换为 **RTMPose + ST-GCN++ 连续滑窗模型**。它使用与部署一致的
64 帧连续窗口和 16 帧步长训练，替代原先“从整段视频均匀抽取 64 帧”的系统权重。

受试者隔离四折测试的合并结果：

| Accuracy | Precision | Recall | Specificity | F1 | Balanced Accuracy |
|---:|---:|---:|---:|---:|---:|
| 84.56% | 72.12% | 81.34% | 85.99% | 76.45% | 83.67% |

混淆矩阵为 TP=388、TN=921、FP=150、FN=89，共 1548 个测试窗口。

在固定的 8 段整视频冒烟测试中，新模型检测到 4/4 个跌倒片段，4/4 个 ADL
片段均未报警。旧系统的结果为 3/4 个跌倒被检测、1/4 个 ADL 误报。新模型纠正了
`Subject 4/Fall/08.mp4` 的漏检和 `Subject 2/ADL/01.mp4` 的误报。

## 数据生成规则

- 数据源：GMDCSA24 的 160 段原始视频和每个 Subject 的 `Fall.csv`。
- 姿态前端：RTMPose balanced，对全部 34,172 帧逐帧提取 COCO-17 关键点。
- 姿态完整性：仅 3 帧未检测到姿态，零姿态率约 0.0088%。
- 窗口：连续 64 帧，步长 16 帧，输入形状 `[N,C,T,V,M]=[N,3,64,17,1]`。
- ADL 视频的窗口全部标记为负类。
- Fall 视频中，跌倒开始前的窗口标记为负类。
- 与标注跌倒区间重叠不少于 0.5 秒的窗口标记为正类。
- 处于跌倒起始边界、但重叠不足 0.5 秒的窗口不参与训练和评价。

最终保留 1548 个窗口：1071 个 ADL/负类，477 个 Fall/正类；另有 36 个边界窗口被忽略。

## 受试者隔离划分

每折使用两个 Subject 训练、一个验证、一个测试；四折测试集合并后恰好覆盖全部
1548 个窗口一次。

| Fold | Train | Val | Test |
|---|---|---|---|
| 1 | 779（S3、S4） | 513（S2） | 256（S1） |
| 2 | 658（S1、S4） | 377（S3） | 513（S2） |
| 3 | 769（S1、S2） | 402（S4） | 377（S3） |
| 4 | 890（S2、S3） | 256（S1） | 402（S4） |

各折测试 Balanced Accuracy 分别为 75.06%、79.37%、92.26% 和 88.48%。
Fold 1 的跨主体泛化相对较弱，后续采集现场数据时应重点检查个体差异。

## 训练设置

| 参数 | 值 |
|---|---:|
| Epochs | 300，全部跑满 |
| Early stopping | 关闭 |
| Batch size | 64 |
| Learning rate | 3e-4 |
| Weight decay | 1e-3 |
| Dropout | 0.5 |
| Base channels | 64 |
| AMP | 开启 |
| Seeds | 2027、2028、2029、2030 |

每折按验证集 Balanced Accuracy 保存 `best.pt`，测试集只用于最终评价。模型参数量
为 1,185,798，当前机器的单窗口 batch-1 分类器平均延迟约 27.75 ms；该延迟不包含
RTMPose 的逐帧姿态推理。

四折最佳轮次分别为 62、95、69、86。学习曲线表明模型在约 100 轮内已经达到最佳
验证表现；本次仍按要求完整训练 300 轮，但部署使用的是各折最佳轮次权重，而不是
第 300 轮权重。

## 文件位置

```text
data/metadata/gmdcsa24_rtmpose_sliding_w64_s16.csv
data/metadata/gmdcsa24_rtmpose_sliding_w64_s16.summary.json
data/splits/gmdcsa24_sliding_loso/fold_1..4/
data/gcn/gmdcsa24_rtmpose_sliding_w64_s16.npz
results/sliding_window_e300_b64/rtmpose_stgcnpp/fold_1..4/
results/sliding_window_e300_b64/rtmpose_stgcnpp/learning_curves.png
results/sliding_window_e300_b64_summary.csv
results/sliding_window_e300_b64_summary.json
outputs/final_sliding_system/
```

原始视频、逐帧姿态缓存、GCN 张量、模型权重和演示视频体积较大，受 `.gitignore`
排除；训练历史、指标、预测、划分和元数据可提交 Git。换机器时需要重新准备大文件。

## 复现命令

```powershell
python scripts/extract_full_video_rtmpose.py `
  --video-root data/raw/GMDCSA24 `
  --output-dir data/poses/gmdcsa24_rtmpose_full `
  --device cuda

python scripts/build_sliding_window_dataset.py `
  --video-root data/raw/GMDCSA24 `
  --pose-root data/poses/gmdcsa24_rtmpose_full `
  --tensor-out data/gcn/gmdcsa24_rtmpose_sliding_w64_s16.npz `
  --metadata-out data/metadata/gmdcsa24_rtmpose_sliding_w64_s16.csv `
  --splits-out data/splits/gmdcsa24_sliding_loso
```

训练时对 `fold_1` 至 `fold_4` 分别运行：

```powershell
python scripts/train_gcn.py `
  --tensor data/gcn/gmdcsa24_rtmpose_sliding_w64_s16.npz `
  --train-csv data/splits/gmdcsa24_sliding_loso/fold_1/train.csv `
  --val-csv data/splits/gmdcsa24_sliding_loso/fold_1/val.csv `
  --test-csv data/splits/gmdcsa24_sliding_loso/fold_1/test.csv `
  --route rtmpose+stgcnpp --model stgcnpp --fold 1 `
  --epochs 300 --batch-size 64 --learning-rate 0.0003 `
  --weight-decay 0.001 --dropout 0.5 --base-channels 64 `
  --no-early-stopping --amp --device cuda `
  --output-dir results/sliding_window_e300_b64/rtmpose_stgcnpp/fold_1
```

系统演示：

```powershell
python -m app.cli `
  --input "data/raw/GMDCSA24/Subject 1/Fall/01.mp4" `
  --output-dir outputs/demo
```

默认读取 `results/sliding_window_e300_b64/rtmpose_stgcnpp/fold_*/best.pt`。

## 困难负样本消融（2026-08-01）

使用原滑窗模型的折外预测，从 GMDCSA24 中选择110个跌倒概率不低于0.8的ADL窗口，
仅在其主体属于训练集的折中增加2份训练副本。四折仍各跑满300轮且不早停，验证集、
内部测试集和MCFD外部测试集保持不变。

MCFD跨视角固定阈值0.5下，F1由67.15%升至68.81%，Recall由69.35%升至75.38%；
但FP由74增至87、Specificity由65.74%降至59.72%，ROC-AUC也从70.86%略降至70.63%。
这说明简单过采样使模型更偏向报警，并没有实现原定的“降低误报”。原滑窗模型在cam1
校准阈值0.32后，MCFD F1达到69.55%，仍高于困难负样本模型的校准结果68.78%。

因此系统默认权重不变。完整协议、混淆矩阵和结论见
[`results/hard_negative_ablation/README.md`](../results/hard_negative_ablation/README.md)。下一轮不再
简单复制旧窗口，而是补充正常躺卧、翻身、坐床、弯腰和起身等具有动作语义的新视频。

## 解释边界

- 83.67% Balanced Accuracy 是受试者隔离的窗口级评价，可用于正式模型比较。
- 滑窗高度重叠，相邻样本相关，因此还应继续报告整视频事件级评价。
- 8 段视频的 4/4 与 0/4 只是流水线冒烟测试；四折集成中的部分模型见过对应
  Subject，不能把它当作无偏准确率。
- 设备到位后仍需建立现场验证集，评价事件召回率、每小时误报数、检测延迟、
  姿态失败率和端到端 FPS，再校准阈值与连续确认窗口数。
