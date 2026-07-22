# 基于人体姿态的跌倒检测基准与系统原型

本项目比较三条跌倒检测路线，并为后续摄像头系统提供统一的数据、模型、评估和接口基础：

1. RTMPose + ST-GCN++
2. YOLO-Pose + ST-GCN++
3. YOLO-Pose + CTR-GCN

当前状态：数据准备、两套姿态缓存、三路线四折训练、内部/外部测试、错误分析和预录视频滑动窗口原型均已完成。下一阶段是设备接入、多人跟踪和现场数据验证。

## 快速查看结果

- 一页式项目全貌：[`项目概要.md`](项目概要.md)
- 正式内部结果：[`results/benchmark_summary.csv`](results/benchmark_summary.csv)
- 正式外部结果：[`results/mcfd_external_benchmark/summary.csv`](results/mcfd_external_benchmark/summary.csv)
- 中文阶段报告：[`results/三路线阶段实验报告.md`](results/三路线阶段实验报告.md)
- 错误与融合分析：[`results/mcfd_error_analysis/错误分析报告.md`](results/mcfd_error_analysis/错误分析报告.md)
- 典型错误视频：`outputs/mcfd_error_cases/`

固定阈值 0.5 下的核心结果：

| 路线 | GMDCSA24 Accuracy | MCFD Accuracy | MCFD Recall | MCFD F1 | MCFD ROC-AUC |
|---|---:|---:|---:|---:|---:|
| RTMPose + ST-GCN++ | **86.88%** | **62.41%** | 60.30% | 60.61% | 64.39% |
| YOLO-Pose + ST-GCN++ | 78.75% | 60.00% | **66.33%** | **61.40%** | **64.84%** |
| YOLO-Pose + CTR-GCN | 77.50% | 58.55% | 62.81% | 59.24% | 61.38% |

MCFD 是未参与训练的外部数据，性能下降反映跨数据集、跨视角和动作定义差异。不能仅凭 GMDCSA24 内部准确率决定系统模型。

## 项目结构

```text
fall_benchmark/
├─ app/                      预录视频推理、状态机和命令行入口
├─ configs/                  实验与系统参数
├─ data/
│  ├─ raw/                   原始视频，不提交 Git
│  ├─ metadata/              视频、片段和姿态缓存清单
│  ├─ splits/                固定训练/验证/测试划分
│  ├─ poses/                 RTMPose、YOLO-Pose 缓存，不提交 Git
│  └─ gcn/                   统一的 N,C,T,V,M 图卷积输入
├─ models/                   正式 ST-GCN++、CTR-GCN 实现
├─ scripts/                  数据准备、训练、评估与可视化入口
├─ tests/                    决策状态机测试
├─ results/
│  ├─ benchmark/             正式三路线 12 个四折模型和内部结果
│  ├─ mcfd_external_benchmark/ 正式权重的 MCFD 外部结果
│  ├─ mcfd_error_analysis/   错误、视角和融合分析
│  ├─ gcn_matrix/            本地早期四路线探索，不发布
│  └─ mcfd_external/         本地早期权重外部探索，不发布
├─ outputs/                  预览视频和图片，不提交 Git
└─ docs/                     复现、架构、结果和系统接口文档
```

## 数据协议

- GMDCSA24：160 个视频，81 个 ADL、79 个跌倒；4 折受试者隔离，每个视频恰好进入一次汇总测试。
- MCFD：场景 1—23 的 552 个标注片段，264 个跌倒、288 个 ADL；cam1 仅用于阈值校准，cam3 用于开发观察，cam2/4/5/6/7/8 共 415 段作为跨视角外部测试。
- 统一骨架：COCO-17，通道为归一化 `x`、`y` 和置信度。
- 统一输入：`[N, C, T, V, M] = [样本, 3, 64, 17, 1]`。
- 当前离线实验在每个视频或标注片段内均匀采样 64 个位置；尚未使用在线滑动窗口。

数据来源、许可和弃用数据集见 [`DATA_SOURCES.md`](DATA_SOURCES.md)。

## 运行环境

已验证环境：Windows、Python 3.12.13、NVIDIA RTX 4060 Laptop GPU、PyTorch 2.12.1+cu130。

```powershell
cd C:\Users\HP\Documents\挑战杯\fall_benchmark
.\.venv\Scripts\Activate.ps1
$env:YOLO_CONFIG_DIR = (Resolve-Path .\.ultralytics).Path
```

依赖说明见 [`docs/REPRODUCE.md`](docs/REPRODUCE.md)。项目中的 `.venv` 已包含当前实验依赖。

## 常用命令

检查已准备的数据：

```powershell
python scripts/verify_prepared_data.py --project .
```

重新训练三条路线的四折模型：

```powershell
python scripts/run_three_routes.py --project . --epochs 80 --patience 15 --batch-size 16
python scripts/summarize_benchmark.py --results results/benchmark --output results
```

300轮上限与早停对照实验已保存在 `results/benchmark_e300/`，学习曲线和结论见
[`docs/TRAINING_E300.md`](docs/TRAINING_E300.md)。复现实验：

```powershell
python scripts/run_three_routes.py --project . --epochs 300 --patience 15 `
  --batch-size 16 --output-root results/benchmark_e300
python scripts/plot_learning_curves.py --results results/benchmark_e300
```

固定跑满300轮、不使用早停的实验位于 `results/benchmark_e300_full/`，结论见
[`docs/TRAINING_E300_FULL.md`](docs/TRAINING_E300_FULL.md)。命令：

```powershell
python scripts/run_three_routes.py --project . --epochs 300 --batch-size 16 `
  --no-early-stopping --output-root results/benchmark_e300_full
python scripts/plot_learning_curves.py --results results/benchmark_e300_full
```

用正式权重重新运行 MCFD 外部测试：

```powershell
python scripts/evaluate_mcfd_ensemble.py
```

重新生成错误分析和典型案例：

```powershell
python scripts/analyze_mcfd_errors.py
python scripts/render_mcfd_error_cases.py
```

运行预录视频系统原型：

```powershell
python -m app.cli `
  --input "data/raw/GMDCSA24/Subject 1/Fall/01.mp4" `
  --output-dir outputs/demo `
  --route yolo_stgcnpp
```

输出 `annotated.mp4`、`windows.jsonl`、`events.jsonl` 和 `summary.json`。默认使用 64 帧窗口、16 帧步长、连续 3 个窗口、至少 3/4 折模型同意才确认报警；姿态有效率低于 50% 时输出 `UNKNOWN`。

更完整的数据准备和复现实验步骤见 [`docs/REPRODUCE.md`](docs/REPRODUCE.md)。

## 系统侧当前建议

- 若优先总体均衡，使用 RTMPose + ST-GCN++ 作为单路线基线。
- 若优先少漏报，使用 YOLO-Pose + ST-GCN++，并在独立验证集校准阈值。
- 算力允许时，对两条 ST-GCN++ 路线做概率平均；当前外部测试的 Balanced Accuracy 为 62.76%，略高于任一单路线。
- 姿态完全缺失时必须输出 `UNKNOWN`、重试姿态检测或切换后端，不能把全零骨架直接分类。
- 报警应由多个连续滑动窗口确认，并保存报警前后的视频证据。

系统模块、状态机和 JSON 接口见 [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md)。

## 文档导航

| 文档 | 内容 |
|---|---|
| [`docs/REPRODUCE.md`](docs/REPRODUCE.md) | 从数据清单到训练、外部评估的复现命令 |
| [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) | 正式协议、指标、结果和已知限制 |
| [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) | 软件模块、在线流程、状态机和接口 |
| [`DATA_SOURCES.md`](DATA_SOURCES.md) | 数据来源、许可、完整性与取舍 |
