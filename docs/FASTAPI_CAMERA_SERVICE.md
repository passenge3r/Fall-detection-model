# 跌倒检测摄像头 FastAPI 服务

## 接入结构

```text
萤石 AppKey/AppSecret
  → AccessToken（内存缓存）
  → 设备列表
  → 路线A：加密 EZOPEN + 官方 PC SDK + 设备验证码
    或标准协议：临时 HLS/FLV/RTMP 地址（要求关闭视频加密）
  → SDK回调/FFmpeg 解码与断流重连
  → YOLO-Pose → 64帧骨架窗口 → 4折 ST-GCN++
  → NORMAL / SUSPECTED / CONFIRMED / COOLDOWN
  → REST事件接口、最新标注帧、MJPEG预览
```

账号密码不能直接调用萤石开放API。需要进入“萤石开放平台 → 控制台 → 我的应用”，获取 `AppKey` 与 `AppSecret`。服务调用：

- `POST https://open.ys7.com/api/lapp/token/get`
- `POST https://open.ys7.com/api/lapp/device/list`
- `POST https://open.ys7.com/api/lapp/v2/live/address/get`

默认请求 HLS、流畅子码流、H264兼容地址。播放地址与AccessToken不会出现在本服务状态接口中。

## 环境配置

复制 `.env.example` 的变量到部署环境，不要把真实密钥提交到Git：

```powershell
$env:YS7_APP_KEY="..."
$env:YS7_APP_SECRET="..."
$env:YS7_DEVICE_SERIAL="..."
$env:FALL_SERVICE_API_KEY="..."
```

安装并启动：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-api.txt
.venv\Scripts\python.exe scripts\run_fall_api.py --host 127.0.0.1 --port 8000
```

联调文档：`http://127.0.0.1:8000/docs`。只有在配置强随机 `FALL_SERVICE_API_KEY`、反向代理HTTPS及网络访问控制后，才能使用 `--host 0.0.0.0`。

## 真机冒烟测试

`scripts/smoke_test_ezviz_live.py` 会依次执行：设备列表查询、选择在线设备、申请临时 HLS 地址、解码探测、启动实时检测、保存脱敏摘要和最新标注帧。凭据使用一次性 JSON 文件传入；不要把该文件放进仓库，测试时建议加 `--delete-credentials`，使脚本读取后立即删除。

如果标准 HLS/FLV/RTMP 地址返回 `60019`，表示设备已开启视频加密。机身标签或快速操作指南二维码中的 6 位大写设备验证码只对 EZOPEN/官方 SDK 路线生效，不能直接作为 FFmpeg 的 HLS/FLV/RTMP 解密参数。开放平台没有读取该验证码的接口。

### 路线A：保持视频加密的官方 PC SDK

Windows 服务端可使用萤石官方 PC SDK 调用 `OpenSDK_StartRealPlayEx`，传入设备验证码，通过数据回调取得 SDK 解密、转封装后的码流，再交给跌倒检测流水线。此方式不要求关闭设备视频加密，也不修改设备设置。

当前已完成：

- 官方 Windows x64 SDK 的 Python `ctypes` 桥接；
- AccessToken、在线设备与设备验证码接入；
- P2P优先、禁止强制VTDU、码流转封装及回调落盘；
- 一次性凭据文件读取后删除，日志不回显Token、验证码或完整序列号；
- 本地视频已经贯通 `YOLO-Pose → 64帧窗口 → ST-GCN++ → FastAPI`。

真机命令：

```powershell
$env:EZVIZ_PC_SDK_ROOT="官方SDK解压目录"
.venv\Scripts\python.exe scripts\record_ezviz_sdk.py `
  --credentials-file "$env:TEMP\ys7-sdk-credentials.json" `
  --delete-credentials --duration 15
```

2026-08-11 的真机测试中，SDK成功连接平台，但预览返回 `525546`，对应 VTDU 取流并发两路已满。显式启用P2P后结果不变，说明此次连接未能建立P2P并回落到VTDU；测试没有抢占或断开其他客户端。为避免影响其他组员，不应持续重试或停止现有预览，应在其他客户端释放一路后做一次15秒验证，或让已有取流端向检测服务转发一路内部流。

## 接口

除 `/health` 外，配置API Key后均需要请求头：`X-API-Key: ...`。

### 查询萤石设备

```http
GET /v1/ezviz/devices
```

只返回序列号、名称、型号、在线状态和风险等级，不返回Token。

### 拉流探针

```http
POST /v1/streams/probe?frames=10
Content-Type: application/json

{"source_type":"ezviz","device_serial":"设备序列号","channel_no":1}
```

成功时返回实际解码帧数、尺寸、FPS与耗时，但不回显播放地址。

也可用直接流地址或本地视频测试：

```json
{"source_type":"direct","source_url":"rtsp://...","camera_id":"room-01"}
```

### 启动与停止检测

```http
POST /v1/streams/start
POST /v1/streams/stop
GET  /v1/streams/status
```

启动请求示例：

```json
{
  "source_type":"ezviz",
  "device_serial":"设备序列号",
  "channel_no":1,
  "camera_id":"elder-room-01",
  "process_every_n_frames":1
}
```

### 结果

- `GET /v1/events?limit=50`：已确认跌倒事件。
- `GET /v1/frame.jpg`：最新带骨架和状态的JPEG。
- `GET /v1/preview.mjpg`：最新结果的MJPEG预览。

事件示例：

```json
{
  "event_id":"UUID",
  "camera_id":"elder-room-01",
  "created_at":"UTC ISO-8601",
  "fall_probability":0.91,
  "pose_valid_ratio":0.95,
  "positive_folds":4,
  "status":"CONFIRMED",
  "route":"yolo_stgcnpp"
}
```

## 系统集成建议

师兄系统通过内部网络调用 `start/status/events`。生产环境推荐把检测服务与业务系统之间增加：

1. HTTPS反向代理与API Key轮换；
2. 事件回调队列或消息队列，替代高频轮询；
3. 每路摄像头独立进程/GPU任务，当前原型单实例只运行一路；
4. 播放地址到期刷新、设备离线告警和结构化日志；
5. Qwen复核作为异步二阶段任务，不能阻塞实时骨架检测。
