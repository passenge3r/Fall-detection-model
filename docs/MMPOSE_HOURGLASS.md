# MMPose Stacked Hourglass 复现说明

## 已验证环境

- Windows、Python 3.12.13
- PyTorch 2.12.1+cu130、RTX 4060 Laptop GPU
- MMPose 1.3.2（官方仓库源码）
- MMEngine 0.10.7、mmcv-lite 2.1.0、MMDetection 3.2.0
- Hourglass52 COCO 256×256 官方权重，参数量 94,847,889

MMPose 1.x 对应 mmcv 2.x。MMDetection 3.2.0 要求 mmcv `<2.2.0`，因此最终固定为 mmcv-lite 2.1.0。不要在同一个环境同时安装 `mmcv` 与 `mmcv-lite`。

Hourglass52 使用标准 PyTorch 卷积、残差块和上采样，不依赖 `mmcv._ext`。MMPose 1.3.2 会无条件导入需要编译算子的 EDPose；`scripts/extract_pose_cache.py` 仅在检测不到 `mmcv._ext` 时跳过这个未使用的注册，不修改 Hourglass 网络、权重或输出。

## 隔离安装

建议保留主环境，另建 `.venv-mmpose`。本机实验为了避免重复安装数GB的PyTorch，让新环境通过 `.pth` 只读复用 `.venv/Lib/site-packages`，MMPose相关包仍安装在独立环境。也可以在新环境中单独安装与设备匹配的PyTorch。

```powershell
git clone --depth 1 https://github.com/open-mmlab/mmpose.git vendor_sources/mmpose
.\.venv\Scripts\python.exe -m venv .venv-mmpose
$basePackages = (Resolve-Path .\.venv\Lib\site-packages).Path
Set-Content .\.venv-mmpose\Lib\site-packages\fall_benchmark_base.pth $basePackages
.\.venv-mmpose\Scripts\python.exe -m pip install -r requirements-mmpose.txt
.\.venv-mmpose\Scripts\python.exe -m pip install --no-deps -e vendor_sources\mmpose
```

## 姿态缓存

路线为 `YOLO26n-Pose人体框 → Hourglass52-COCO → COCO-17关键点`。YOLO只提供人物框，关键点来自Hourglass。

```powershell
.\.venv-mmpose\Scripts\python.exe scripts\extract_pose_cache.py `
  --manifest data\metadata\gmdcsa24.csv `
  --video-root data\raw\GMDCSA24 `
  --output-dir data\poses\hourglass\gmdcsa24_t64 `
  --output-manifest data\metadata\gmdcsa24_hourglass_t64.csv `
  --backend hourglass --frames 64 --device cuda --yolo-conf 0.1

.\.venv\Scripts\python.exe scripts\build_gcn_tensor.py `
  --manifest data\metadata\gmdcsa24_hourglass_t64.csv `
  --output data\gcn\gmdcsa24_hourglass_t64.npz --project-root .
```

全量缓存：160个视频、10240个采样帧、305个零姿态帧（2.98%）、平均关键点置信度0.6359。提取耗时约22分钟。

## 固定300轮结果

| 路线 | BA | F1 | Recall | Specificity |
|---|---:|---:|---:|---:|
| Hourglass52 + ST-GCN++ | **76.89%** | 77.02% | 78.48% | **75.31%** |
| Hourglass52 + CTR-GCN | 75.72% | **77.19%** | **83.54%** | 67.90% |
| Hourglass52 + PoseC3D-style | 71.99% | 73.99% | 81.01% | 62.96% |

三条路线均按主体隔离四折，每折固定300轮且无早停，共3600个epoch。最高结果76.89%，低于RTMPose + ST-GCN++的86.83%，也未超过YOLO-Pose + CTR-GCN的78.79%。因此Hourglass在内部筛选阶段淘汰，没有继续执行MCFD全量外测。
