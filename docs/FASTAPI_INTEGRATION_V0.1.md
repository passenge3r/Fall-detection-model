# 跌倒检测 FastAPI 初版联调说明

## 1. 当前可集成范围

本版本已经实现：

```text
本地视频 / HTTP-HLS / RTSP / RTMP
  → 视频解码
  → YOLO-Pose 人体关键点
  → 64帧骨架滑动窗口
  → 4折 ST-GCN++ 集成推理
  → NORMAL / SUSPECTED / CONFIRMED / COOLDOWN
  → FastAPI 状态、事件、标注帧和 MJPEG 预览
```

建议先用 `source_type=direct` 接入。后续正式系统由统一视频接入服务只向萤石拉取一路，再将内部 RTSP/RTMP 地址传给本服务，避免每个模块分别占用萤石并发。

当前尚未完成的是“萤石加密 EZOPEN SDK 实时帧 → FastAPI”的真机闭环。萤石两路 VTDU 并发持续被占用，因此本初版不把萤石 SDK 作为业务系统联调前置条件。

## 2. 目录说明

```text
app/                         FastAPI、视频流和检测代码
models/                      ST-GCN++ 模型结构
scripts/run_fall_api.py      服务启动入口
scripts/build_gcn_tensor.py  骨架归一化
scripts/extract_pose_cache.py YOLO-Pose 推理后端
weights/yolo26n-pose.pt      YOLO 姿态权重
weights/stgcnpp/fold_*/best.pt 四折跌倒分类权重
openapi.json                 固定版本接口契约
.env.example                 环境变量模板（不含真实密钥）
requirements*.txt            Python依赖
start_api.ps1                Windows启动脚本
```

## 3. 安装与启动

推荐 Windows、Python 3.11/3.12。GPU部署应先安装与目标CUDA环境匹配的PyTorch；没有CUDA时可使用CPU，但速度较慢。

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -r requirements-api.txt
```

启动：

```powershell
$env:FALL_SERVICE_API_KEY="请替换为强随机字符串"
.\start_api.ps1 -HostAddress 127.0.0.1 -Port 8000
```

Swagger：`http://127.0.0.1:8000/docs`

健康检查无需API Key：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

跨主机部署前必须配置强随机 `FALL_SERVICE_API_KEY`，并由反向代理提供HTTPS和访问控制。不要直接把开发服务暴露到公网。

## 4. 推荐联调流程

除 `/health` 外，以下请求都需要请求头：

```http
X-API-Key: 与 FALL_SERVICE_API_KEY 相同的值
```

### 4.1 探测视频源

```http
POST /v1/streams/probe?frames=10
Content-Type: application/json
X-API-Key: ...

{
  "source_type": "direct",
  "source_url": "rtsp://内部视频服务/camera-01",
  "camera_id": "elder-room-01"
}
```

成功响应：

```json
{
  "camera_id": "elder-room-01",
  "ok": true,
  "decoded_frames": 10,
  "width": 1920,
  "height": 1080,
  "reported_fps": 25.0,
  "elapsed_seconds": 0.63
}
```

### 4.2 启动检测

```http
POST /v1/streams/start
Content-Type: application/json
X-API-Key: ...

{
  "source_type": "direct",
  "source_url": "rtsp://内部视频服务/camera-01",
  "camera_id": "elder-room-01",
  "process_every_n_frames": 1
}
```

单个服务实例当前只运行一路视频。重复启动返回 HTTP 409。

也可传服务端本地视频绝对路径进行联调：

```json
{
  "source_type": "direct",
  "source_url": "D:/test-videos/fall.mp4",
  "camera_id": "local-test"
}
```

### 4.3 查询状态

```http
GET /v1/streams/status
X-API-Key: ...
```

关键字段：

- `running`：检测线程是否运行；
- `state`：`STARTING / CONNECTING / RUNNING / ERROR / STOPPED`；
- `frames_decoded`、`frames_processed`：解码和检测帧数；
- `reconnects`：断流重连次数；
- `last_error`：最近错误，不包含视频地址或平台Token；
- `latest_result.state`：`WARMUP / NORMAL / SUSPECTED / CONFIRMED / COOLDOWN / UNKNOWN`；
- `latest_result.fall_probability`：四折平均跌倒概率；
- `latest_result.positive_folds`：四个分类模型中判断为阳性的数量；
- `latest_result.pose_valid_ratio`：当前64帧窗口姿态有效率。

服务启动后的前64个处理帧属于预热期，尚无完整分类窗口。

### 4.4 查询跌倒事件

```http
GET /v1/events?limit=50
X-API-Key: ...
```

事件响应：

```json
{
  "events": [
    {
      "event_id": "UUID",
      "camera_id": "elder-room-01",
      "created_at": "UTC ISO-8601",
      "fall_probability": 0.91,
      "pose_valid_ratio": 0.95,
      "positive_folds": 4,
      "status": "CONFIRMED",
      "route": "yolo_stgcnpp"
    }
  ]
}
```

当前事件保存在进程内存中，最多200条，服务重启后清空。业务系统初版可轮询该接口；正式版本建议增加事件回调或消息队列并持久化。

### 4.5 获取画面

- `GET /v1/frame.jpg`：最新一张带骨架和状态的JPEG；尚无处理帧时返回404。
- `GET /v1/preview.mjpg`：MJPEG连续预览，可嵌入内部管理页面。

### 4.6 停止并释放资源

```http
POST /v1/streams/stop
X-API-Key: ...
```

业务系统停止模块或切换视频源前应先调用该接口。

## 5. HTTP状态码

- `200`：请求成功；
- `401`：API Key错误；
- `404`：尚无处理后的画面；
- `409`：重复启动、检测器初始化失败或启动参数冲突；
- `422`：请求体字段缺失或格式错误；
- `502`：视频源不可用、解码失败或萤石开放API失败。

## 6. 初版限制

1. 单FastAPI进程仅支持一路检测，多摄像头需多进程/多实例部署。
2. 事件暂存内存，尚无数据库和主动回调。
3. 默认模型主要用于跌倒发生过程与倒地确认；预跌倒风险预测分支尚在开发。
4. Qwen/V-JEPA复核尚未接入本FastAPI实时主链路。
5. 萤石加密SDK实时取流尚未完成真机帧闭环；建议统一拉流后向本服务提供内部标准流。

## 7. 联调验收条件

初版满足以下条件即可认为业务系统接入成功：

1. `/health` 返回 `ok=true`；
2. `/v1/streams/probe` 能解码10帧；
3. `/v1/streams/start` 后状态进入 `RUNNING`；
4. `frames_processed` 持续增加；
5. `/v1/frame.jpg` 能返回标注画面；
6. `/v1/events` 能被业务系统解析并去重；
7. `/v1/streams/stop` 后状态为 `STOPPED`。

