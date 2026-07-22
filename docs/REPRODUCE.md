# 实验复现说明

所有命令默认从项目根目录 `fall_benchmark` 运行。

## 1. 环境

当前已验证版本：

| 组件 | 版本 |
|---|---|
| Python | 3.12.13 |
| PyTorch | 2.12.1+cu130 |
| CUDA runtime | 13.0 |
| NumPy | 2.5.1 |
| OpenCV | 5.0.0 |
| Ultralytics | 8.4.55 |
| ONNX Runtime | 1.27.0 |
| RTMLib | 0.0.15 |

```powershell
.\.venv\Scripts\Activate.ps1
$env:YOLO_CONFIG_DIR = (Resolve-Path .\.ultralytics).Path
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name())"
```

PyTorch 与 ONNX Runtime GPU 包必须根据设备和 CUDA 环境安装；不建议在另一台机器上机械复制本机 CUDA 版本。

## 2. 原始数据位置

```text
data/raw/GMDCSA24/
data/raw/MCFD/kaggle/
```

原始视频和姿态缓存体积较大，受 `.gitignore` 排除。换机器时需要单独复制，或者按 `DATA_SOURCES.md` 重新下载并验证。

## 3. 重建 GMDCSA24 清单与四折划分

```powershell
python scripts/make_gmdcsa24_manifest.py `
  --root data/raw/GMDCSA24 `
  --metadata-out data/metadata/gmdcsa24.csv `
  --splits-out data/splits/gmdcsa24_loso
```

每折使用两个受试者训练、一个受试者验证、一个受试者测试。四折测试合并后必须正好覆盖 160 个唯一视频。

## 4. 提取姿态缓存

AlphaPose 与 PyTorch OpenPose 的源码、权重受 `.gitignore` 排除，首次运行先准备：

```powershell
git clone https://github.com/MVIG-SJTU/AlphaPose.git vendor_sources/AlphaPose
gdown 1kQhnMRURFiy7NsdS8EFL-8vtqEXOgECn `
  -O models/alphapose/fast_res50_256x192.pth

git clone https://github.com/Hzzone/pytorch-openpose.git vendor_sources/pytorch-openpose
curl.exe -L https://huggingface.co/lllyasviel/Annotators/resolve/main/body_pose_model.pth `
  -o models/openpose_body_pose_model.pth
```

若直接使用 CMU Caffe 权重，可选择 `--openpose-runtime caffe`，但需要另装仍支持 Caffe 的 OpenCV 4.x；默认 PyTorch 端口可直接使用现有 CUDA 环境。

RTMPose：

```powershell
python scripts/extract_pose_cache.py `
  --manifest data/metadata/gmdcsa24.csv `
  --video-root data/raw/GMDCSA24 `
  --output-dir data/poses/rtmpose/gmdcsa24_t64 `
  --output-manifest data/metadata/gmdcsa24_rtmpose_t64.csv `
  --backend rtmpose --rtmpose-mode balanced --device cuda --frames 64
```

YOLO-Pose：

```powershell
python scripts/extract_pose_cache.py `
  --manifest data/metadata/gmdcsa24.csv `
  --video-root data/raw/GMDCSA24 `
  --output-dir data/poses/yolo_pose/gmdcsa24_t64_c010 `
  --output-manifest data/metadata/gmdcsa24_yolo_t64_c010.csv `
  --backend yolo --yolo-model models/yolo26n-pose.pt `
  --yolo-conf 0.10 --device cuda --frames 64
```

AlphaPose FastPose-ResNet50（需先按官方模型库取得配置、源码和权重）：

```powershell
python scripts/extract_pose_cache.py `
  --manifest data/metadata/gmdcsa24.csv `
  --video-root data/raw/GMDCSA24 `
  --output-dir data/poses/gmdcsa24_alphapose_t64 `
  --output-manifest data/metadata/gmdcsa24_alphapose_t64.csv `
  --backend alphapose --frames 64 --device cuda
```

PyTorch OpenPose（CMU COCO Caffe 权重的直接转换版本，默认 256×256、batch 16）：

```powershell
python scripts/extract_pose_cache.py `
  --manifest data/metadata/gmdcsa24.csv `
  --video-root data/raw/GMDCSA24 `
  --output-dir data/poses/gmdcsa24_openpose_t64 `
  --output-manifest data/metadata/gmdcsa24_openpose_t64.csv `
  --backend openpose --openpose-input-size 256 `
  --openpose-batch-size 16 --frames 64 --device cuda
```

`--overwrite` 会重新推理已存在的缓存，正常续跑不要添加该参数。

## 5. 构建统一 GCN 张量

```powershell
python scripts/build_gcn_tensor.py `
  --manifest data/metadata/gmdcsa24_rtmpose_t64.csv `
  --output data/gcn/gmdcsa24_rtmpose_t64.npz `
  --project-root .

python scripts/build_gcn_tensor.py `
  --manifest data/metadata/gmdcsa24_alphapose_t64.csv `
  --output data/gcn/gmdcsa24_alphapose_t64.npz `
  --project-root .

python scripts/build_gcn_tensor.py `
  --manifest data/metadata/gmdcsa24_openpose_t64.csv `
  --output data/gcn/gmdcsa24_openpose_t64.npz `
  --project-root .

python scripts/build_gcn_tensor.py `
  --manifest data/metadata/gmdcsa24_yolo_t64_c010.csv `
  --output data/gcn/gmdcsa24_yolo_t64_c010.npz `
  --project-root .
```

归一化保留人体相对于序列起始位置的下降位移：以开头最多 8 帧的有效人体中心中位数为原点，以序列中位躯干长度为尺度。低置信度关节置零，第三通道保留置信度。

## 6. 训练与内部汇总

```powershell
python scripts/run_three_routes.py --project . --epochs 80 --patience 15 --batch-size 16
python scripts/summarize_benchmark.py --results results/benchmark --output results
```

21 路固定跑满 300 轮并保存各折验证最优模型：

```powershell
python scripts/run_three_routes.py --project . --epochs 300 --batch-size 16 `
  --no-early-stopping --output-root results/benchmark_e300_full
python scripts/summarize_benchmark.py `
  --results results/benchmark_e300_full `
  --output results/benchmark_e300_full_summary.json
python scripts/plot_learning_curves.py --results results/benchmark_e300_full
```

未指定 `--overwrite` 时，已有完整折会跳过。正式产物应包括：

```text
results/benchmark/<pose>_<model>/fold_1..4/best.pt
results/benchmark/<pose>_<model>/fold_1..4/metrics.json
results/benchmark_summary.csv
```

## 7. MCFD 外部测试

MCFD 姿态缓存和张量已存在时直接运行：

```powershell
python scripts/evaluate_mcfd_ensemble.py
```

脚本默认读取 `results/benchmark/` 的正式 12 个权重，结果写入 `results/mcfd_external_benchmark/`。每条路线对四折模型的跌倒概率取平均。

严禁用历史目录 `results/gcn_matrix/` 的权重替代正式三路线结果，也不要把 `results/mcfd_external/` 当作最终输出；它们只保留用于追溯早期实验。

## 8. 错误分析

```powershell
python scripts/analyze_mcfd_errors.py
python scripts/render_mcfd_error_cases.py
```

输出包括融合比较、按摄像头指标、全部逐片段错误类型、6 个典型案例视频和联系图。

## 9. 复现验收条件

- GMDCSA24：160 个唯一视频，81 ADL、79 跌倒。
- 每条路线：4 个 `best.pt`，内部汇总 160 条无重复测试预测。
- MCFD：552 个唯一片段；跨视角正式测试 415 段。
- 两套 MCFD 张量形状均为 `(552, 3, 64, 17, 1)`，标签和样本顺序一致。
- 所有结果必须记录固定阈值 0.5；校准阈值只能使用 cam1，不能查看跨视角测试标签后选阈值。
