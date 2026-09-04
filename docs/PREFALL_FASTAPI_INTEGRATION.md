# 跌倒预警分支 FastAPI 集成说明

更新日期：2026-08-15

## 1. 启用方式

在 `.env` 中设置：

```env
FALL_ROUTE=rtmpose_stgcnpp
PREFALL_ENABLED=true
PREFALL_CHECKPOINTS_ROOT=outputs/prevfall_rtmpose_stgcnpp_300e_b128
PREFALL_MIN_POSITIVE_FOLDS=5
```

预警权重使用 RTMPose 骨架训练，因此必须配合 `rtmpose_stgcnpp`。预警与跌倒检测复用同一摄像头连接、RTMPose结果及64帧窗口，不会额外拉取视频流。

程序会自动发现 `PREFALL_CHECKPOINTS_ROOT` 下的 `fold_*`。当前正式目录包含9折模型，采用至少5折同意的多数票规则；若折目录或权重不完整，服务会拒绝加载，避免静默缺失模型。

## 2. 获取结果

视频流启动后调用：

```http
GET /v1/streams/status
```

读取 `status.latest_result.prefall_prediction`：

```json
{
  "enabled": true,
  "risk_level": "MEDIUM",
  "prediction_active": true,
  "probabilities": {
    "1s": 0.41,
    "2s": 0.53,
    "3s": 0.61
  },
  "positive_folds": {
    "1s": 3,
    "2s": 6,
    "3s": 7
  },
  "min_positive_folds": 5,
  "ensemble_folds": 9,
  "pose_valid_ratio": 0.92,
  "experimental": true
}
```

## 3. 状态含义

- `WARMUP`：尚未积累满64帧。
- `POSE_UNAVAILABLE`：骨架有效率不足，模型被禁止推理；常见于无人、遮挡、出画或关键点提取失败。
- `NORMAL`：三个预警时距均未达到投票条件。
- `LOW`：预计3秒内存在跌倒风险。
- `MEDIUM`：预计2秒内存在跌倒风险。
- `HIGH`：预计1秒内存在跌倒风险。
- `FALL_CONFIRMED`：跌倒检测分支已经确认跌倒，转入事件处置。
- `RESPONSE_ACTIVE`：已确认事件后的持续处置阶段。

## 4. 姿态质量安全门控

预跌倒模型对全零骨架等分布外输入可能产生高置信度错误结果。因此服务在推理前检查最近64帧的有效骨架比例：低于 `min_pose_valid_ratio` 时不调用预警模型，而是返回 `POSE_UNAVAILABLE`。界面不得把该状态显示成“正常”，因为它表示当前无法可靠判断。

## 5. 当前实验指标

PreVFall 9名受试者严格LOSO、每折训练满300轮，并使用各折验证集最佳检查点：

- Macro Balanced Accuracy：0.8833 ± 0.0726
- Macro-F1：0.6681 ± 0.1401
- Macro PR-AUC：0.8314 ± 0.1592
- 1秒预警 Recall：0.8408
- 2秒预警 Recall：0.7982
- 3秒预警 Recall：0.8047

这些是模拟场景数据上的受试者独立结果，不等同于真实家庭摄像头效果。当前预警分支应先用于界面提示、事件记录和人工复核，不宜单独联动紧急外部动作；高级告警应与跌倒检测、持续倒地状态或人工确认联合触发。

