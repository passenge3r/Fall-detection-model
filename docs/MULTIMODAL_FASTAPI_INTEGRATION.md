# Qwen3-VL 多模态复核分支集成说明

更新日期：2026-08-24

## 1. 当前接入方式

多模态模型不替换实时骨架模型，而是作为第三条异步复核分支：

```text
同一摄像头视频流
├─ RTMPose + ST-GCN++：确认已经发生的跌倒
├─ RTMPose + ST-GCN++：预测未来1/2/3秒风险
└─ 最近RGB视频缓冲 → Qwen3-VL-2B：动作类别、阶段、原因和摘要
```

当骨架分支达到 `HIGH`、`FALL_CONFIRMED` 或跌倒检测进入 `CONFIRMED` 时，系统立即保留预警，同时继续缓存2.5秒RGB画面；随后从160帧RGB缓冲区均匀选择8帧交给Qwen。`MEDIUM`仍显示给用户，但不会提前占用Qwen。推理在线程中运行，不阻塞摄像头解码与骨架检测。

## 2. 配置

先运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\安装多模态模型.ps1
```

再在 `.env` 中设置：

```env
MULTIMODAL_ENABLED=true
MULTIMODAL_MODEL=Qwen/Qwen3-VL-2B-Instruct
MULTIMODAL_DEVICE=cuda
MULTIMODAL_FRAMES=8
MULTIMODAL_BUFFER_FRAMES=160
MULTIMODAL_MAX_NEW_TOKENS=112
MULTIMODAL_COOLDOWN_SECONDS=15
MULTIMODAL_POST_TRIGGER_SECONDS=2.5
MULTIMODAL_TRIGGER_LEVELS=HIGH,FALL_CONFIRMED
MULTIMODAL_ALLOW_DOWNLOAD=false
MULTIMODAL_ADAPTER_PATH=
```

基础模型体积较大，不放入业务代码压缩包，由部署机单独下载。当前默认不加载QLoRA适配器：已有适配器在MCFD-192上的平衡准确率为69.27%，低于专用零样本提示的72.92%。

## 3. 自动触发和手动触发

自动触发后，从以下位置读取：

```text
GET /v1/streams/status
latest_result.multimodal_review
```

也可以在缓冲区至少有8帧后手动触发：

```http
POST /v1/multimodal/review
```

单独查询：

```http
GET /v1/multimodal/status
```

## 4. 输出示例

```json
{
  "status": "READY",
  "action_class": "falling",
  "fall_stage": "falling",
  "risk_level": "HIGH",
  "confidence": 0.99,
  "evidence": "visible abrupt transition toward the floor",
  "summary_zh": "人正在摔倒",
  "review_outcome": "CORROBORATED_FALL",
  "fusion_decision": "ESCALATE_CONFIRMED",
  "latency_seconds": 9.45,
  "advisory_only": true
}
```

状态含义：

- `IDLE`：等待触发。
- `RUNNING`：Qwen正在异步分析，实时骨架分支仍继续运行。
- `WAITING_POST_FRAMES`：骨架预警已产生，系统正在收集触发后2.5秒画面。
- `READY`：复核完成。
- `ERROR`：模型缺失、显存不足或推理异常；错误不会中断骨架分支。
- `DISABLED`：环境变量没有启用多模态分支。

融合字段含义：

- `ESCALATE_CONFIRMED`：RGB视频也观察到跌倒过程。
- `VISUALLY_SUPPORTED`：RGB视频观察到跌倒前或倒地后阶段。
- `SKELETON_ONLY_CONFLICT`：骨架告警没有被RGB视频确认，应进入人工复核，不能直接撤销骨架告警。
- `INCONCLUSIVE`：大模型输出无法可靠解析。

## 5. 当前实跑结果与限制

- 既有五分类平衡小样本试验：50段、每类10段，准确率与Macro Recall均为82%，跌倒类Recall为50%。
- 当前机器：RTX 4060 Laptop 8GB。
- 推荐的1秒HIGH触发路线共76段复核：68/69个真实触发得到确认，7/7个误触发未被确认。
- 作为升级确认器时：Accuracy 96.30%、Precision 100%、Recall 94.44%、F1 97.14%、Balanced Accuracy 97.22%。
- 平均推理4.71秒，中位数4.54秒；实时骨架预警不等待该结果。

因此Qwen输出只用于升级确认、语义复核和解释，不直接取消实时骨架告警。上述评估是触发级级联测试，不是家庭摄像头长时误报率；真实部署仍需继续采集数据。
