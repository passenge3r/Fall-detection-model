# 可编程设备最佳实践-摄像头SDK介绍与使用说明.md

> 可编程设备最佳实践-摄像头SDK介绍与使用说明

> 更新时间: 2025-08-20T15:40:21.000+08:00

> 文档ID: 4494 | 来源树: 云接入

---

# 摄像头SDK介绍与使用说明

## 一、SDK概述

本SDK提供摄像头设备的完整控制能力，涵盖SD卡管理、云台控制、网络配置、媒体录制、告警管理等核心功能。支持异步操作、参数配置及状态查询，适用于可编程摄像头设备的开发与维护。

## 二、核心功能模块

### 1. **存储管理**

- **SD卡操作**
  - format\_sd\_card(percentage)：异步格式化SD卡（百分比范围[0,90]）
  - get\_sd\_status()：获取SD卡状态（返回分区容量、使用率等信息）
- **文件系统操作**
  - create\_directory(path) / create\_file(path)：创建目录/文件
  - delete\_path(path)：删除路径（支持文件或目录）
  - get\_directory\_info(path)：查询目录下的文件/目录列表

### 2. **云台控制**

- **基础控制**
  - ptz\_rotate(cfg\_str)：设置云台水平/垂直角度及速度
  - ptz\_stop()：立即停止云台转动  
    -`position\_correct()：校准云台初始位置
- **预置点管理**
  - ptz\_add\_preset(preset\_index) / ptz\_del\_preset(preset\_index)：添加/删除预置点
  - ptz\_call\_preset(preset\_index)：调用指定预置点
  - ptz\_del\_preset\_all()：清空所有预置点
- **巡航控制**
  - ptz\_set\_cruise(cfg\_str)：设置巡航路径（支持1-4个预置点）
  - ptz\_cruise\_enable(enable)：开启/关闭巡航模式

### 3. **网络与WiFi**

- **WiFi配置**
  - get\_wifi\_list(count)：获取可用WiFi列表（最多10个）
  - connect\_wifi\_async(cfg\_str)：异步连接指定WiFi（需密码及加密方式）
  - disconnect\_wifi()：断开当前WiFi连接
- **网络参数**
  - get\_network\_param()：查询当前IP、网关等网络信息
  - set\_network\_parameters(cfg\_str)：手动设置IP、DNS等参数

### 4. **媒体录制与抓图**

- **视频/图片操作**
  - save\_video\_by\_time(cfg\_str)：按时间范围保存视频到SD或云端
  - start\_media\_record(cfg\_str) / stop\_media\_record(cfg\_str)：开始/停止视频录制
  - start\_local\_snapshot(cfg\_str)：摄像头抓图（支持本地或云端存储）
- **录音功能**
  - start\_mic\_record(cfg\_str) / stop\_mic\_record(cfg\_str)：开始/停止录音

### 5. **告警与OSD管理**

- **告警配置**
  - get\_alarm\_info()：查询已启用的告警类型（如人形检测、声音告警等）
  - set\_alarm\_status(cfg\_str)：开启/关闭指定告警类型
  - get\_alarm\_events()：获取最近200条告警事件记录
- **画面设置**
  - set\_wdr(cfg\_str)：设置宽动态范围（WDR）参数
  - set\_mirror(cfg\_str)：镜像翻转画面

---

## 三、典型使用示例

### 示例1：格式化SD卡并查询状态

```
# 格式化SD卡（保留10%空间）
result = format_sd_card(percentage=90)
if result == 0:
    print("格式化任务已提交")
else:
    print("格式化失败")

# 查询SD卡状态
sd_status = get_sd_status()
if sd_status != -1:
    print(f"已用空间: {sd_status['used']}%, mmc01剩余空间: {sd_status['free_mmc01']}GB")
```

### 示例2：设置WiFi并获取网络信息

```
# 连接WiFi（假设密码为"12345678"，加密方式为WPA2）
wifi_config = {
    "ssid": "TP-LINK_35EB",
    "password": "12345678",
    "security": 4  # WPA2-PSK
}
result = connect_wifi_async(cfg_str=json.dumps(wifi_config))
if result == 0:
    print("WiFi连接请求已提交")

# 获取当前网络参数
network_info = get_network_param()
if network_info != -1:
    print(f"IP地址: {network_info['ip_addr']}, 信号强度: {network_info['signal_strength']}")
```

### 示例3：云台巡航控制

```
# 设置巡航路径（预置点1和3）
cruise_config = {
    "preset_num": 2,
    "preset_no": [1, 3]
}
result = ptz_set_cruise(cfg_str=json.dumps(cruise_config))
if result == 0:
    # 开启巡航模式
    ptz_cruise_enable(enable=1)
```

---

## 四、注意事项

1. **参数范围校验**

   - 百分比参数（如format\_sd\_card的percentage）需在[0,90]范围内。
   - 预置点索引需在[1,12]范围内。
2. **错误处理**

   - 函数返回非0值表示操作失败，需检查输入参数或设备状态。
   - 状态查询函数（如get\_sd\_status）返回-1表示查询失败。
3. **异步操作**

   - 格式化SD卡、WiFi连接等操作为异步，需确保设备完成操作后再执行后续步骤。
4. **云存储ID查询**

   - 涉及云端存储的接口（如save\_video\_by\_time, ptz\_panoramic, start\_local\_snapshot, start\_media\_record, start\_mic\_record）需通过get\_storage\_id或get\_and\_clear\_all\_storages获取云存储ID。
5. **JSON参数格式**

   - 所有JSON参数需严格遵循文档中的字段定义，确保键名和类型正确。

---

## 五、开发建议

1. **模块化设计**：按功能模块（如存储、网络、云台）划分代码，便于维护。
2. **异常重试机制**：对关键操作（如SD卡格式化、网络连接）增加重试逻辑。
3. **日志记录**：记录关键API的输入、输出及错误信息，便于调试。

如需具体接口的详细用法，请参考对应函数的文档说明。

---

## 六、函数说明

#### **1. format\_sd\_card(percentage)**

- **描述**：异步格式化SD卡。
- **入参**：  
  percentage (int) - 格式化的百分比[0,90]。
- **返回**：0（任务已提交）；非0（操作失败）。

---

#### **2. create\_directory(path)**

- **描述**：在SD卡中创建目录。
- **入参**：  
  path (str) - 目录路径。
- **返回**：0（创建成功）；非0（创建失败）。

---

#### **3. create\_file(path)**

- **描述**：在SD卡中创建空文件。
- **入参**：  
  path (str) - 文件路径。
- **返回**：0（创建成功）；非0（创建失败）。

---

#### **4. delete\_path(path)**

- **描述**：删除SD卡中指定目录或文件。
- **入参**：  
  path (str) - 路径。
- **返回**：0（删除成功）；非0（删除失败）。

---

#### **5. save\_video\_by\_time(cfg\_str)**

- **描述**：按时间段保存视频。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "start_time": 1638400000,  // long, 开始录像时间戳
    "end_time": 1638400000,    // long, 结束录像时间戳
    "sd": 1                    // int, 1=保存到SD卡, 0=保存到云端
  }
  ```
- **返回**：0（成功）；非0（失败）。

---

#### **6. get\_sd\_status()**

- **描述**：获取SD卡状态。
- **入参**：无。
- **返回**：SD卡状态字典或-1（失败）：

  ```
  {
    "used": 1,          // int, 已用空间百分比
    "total_mmc01": 102.41, // double, mmc01分区总容量(GB)
    "free_mmc01": 65.31,  // double, mmc01分区剩余容量(GB)
    "total_mmc02": 256.00, // double, mmc02分区总容量(GB)
    "free_mmc02": 180.50, // double, mmc02分区剩余容量(GB)
    "total_mmc03": 0.00,  // double, mmc03分区总容量(GB)
    "free_mmc03": 0.00,   // double, mmc03分区剩余容量(GB)
    "total_mmc04": 0.00,  // double, mmc04分区总容量(GB)
    "free_mmc04": 0.00,   // double, mmc04分区剩余容量(GB)
    "diskStatus": 0       // int, 磁盘状态: 0=活动, 1=休眠, 2=不正常, 3=硬盘出错
  }
  ```

---

#### **7. get\_directory\_info(path)**

- **描述**：获取指定路径下的文件和目录信息。
- **入参**：  
  `path` (str) - 查询路径。
- **返回**：文件/目录信息字典或-1（失败）：

  ```
  {
    "num_files": 4,        // int, 文件数量
    "num_directories": 5,  // int, 目录数量
    "files": ["all.pem", "config.txt", ...], // list[str], 文件列表
    "directories": ["voice", "certs", ...]   // list[str], 目录列表
  }
  ```

---

#### **8. get\_ptz\_capa()**

- **描述**：获取云台能力。
- **入参**：无。
- **返回**：云台能力字典或-1（失败）：

  ```
  {
    "pan_angle_min": -340, // int, 水平转动最小角度
    "pan_angle_max": 340,  // int, 水平转动最大角度
    "tilt_angle_min": -60, // int, 垂直转动最小角度
    "tilt_angle_max": 60,  // int, 垂直转动最大角度
    "speed_min": 1,        // int, 最小速度
    "speed_max": 3         // int, 最大速度
  }
  ```

---

#### **9. ptz\_rotate(cfg\_str)**

- **描述**：云台转动。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "pan_angle": 10, // int, 水平旋转角度
    "tilt_angle": 20, // int, 垂直旋转角度
    "speed": 1        // int, 转动速度
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **10. ptz\_stop()**

- **描述**：停止云台转动。
- **入参**：无。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **11. position\_correct()**

- **描述**：校准云台位置。
- **入参**：无。
- **返回**：0（校准成功）；非0（校准失败）。

---

#### **12. ptz\_add\_preset(preset\_index)**

- **描述**：新增预置点。
- **入参**：  
  preset\_index (int) - 预置位索引[1,12]。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **13. ptz\_del\_preset(preset\_index)**

- **描述**：删除指定预置点。
- **入参**：  
  preset\_index (int) - 预置位索引[1,12]。
- **返回**：0（删除成功）；非0（操作失败）。

---

#### **14. ptz\_del\_preset\_all()**

- **描述**：清空所有预置点。
- **入参**：无。
- **返回**：0（清空成功）；非0（操作失败）。

---

#### **15. ptz\_call\_preset(preset\_index)**

- **描述**：调用指定预置点。
- **入参**：  
  preset\_index (int) - 预置位索引[1,12]。
- **返回**：0（调用成功）；非0（操作失败）。

---

#### **16. ptz\_get\_preset()**

- **描述**：查询当前配置的预置点信息。
- **入参**：无。
- **返回**：预置点信息字典或-1（失败）：

  ```
  {
    "preset_num": 1,     // int, 预置点数量
    "preset_index": [1]  // list[int], 预置点索引列表
  }
  ```

---

#### **17. ptz\_panoramic(cfg\_str)**

- **描述**：设置全景图保存路径、命名规则及存储类型。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "path": "/mnt/mmc02/.../pano", // str, 存储路径
    "pic_name": "pano",            // str, 全景图命名前缀
    "type": 0                      // int, 0=本地存储, 1=云端存储
  }
  ```
- **补充说明**：
  - 生成12张图：pic\_name1.jpg 到 pic\_name12.jpg。
  - type=1 时可用 get\_storage\_id 查询云存储ID。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **18. ptz\_set\_cruise(cfg\_str)**

- **描述**：新增/修改巡航路径。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "preset_num": 2,      // int, 预置点个数(1-4)
    "preset_no": [1, 2]   // list[int], 预置点编号
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **19. ptz\_del\_cruise()**

- **描述**：删除巡航路径。
- **入参**：无。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **20. ptz\_cruise\_enable(enable)**

- **描述**：开启/停止巡航。
- **入参**：  
  enable (int) - 1=开启, 0=停止。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **21. ptz\_get\_cruise()**

- **描述**：查询巡航轨迹信息。
- **入参**：无。
- **返回**：巡航信息字典或-1（失败）：

  ```
  {
    "preset_num": 2,      // int, 预置点数量
    "preset_no": [1, 3],  // list[int], 预置点索引
    "enable": 1           // int, 巡航状态: 1=开启, 0=停止
  }
  ```

---

#### **22. set\_privacy\_enable(enable)**

- **描述**：开启/关闭隐私遮蔽。
- **入参**：  
  enable (int) - 1=开启, 0=关闭。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **23. get\_wifi\_list(count)**

- **描述**：获取WiFi列表。
- **入参**：  
  count (int) - 获取列表个数(1-10)。
- **返回**：WiFi信息列表或-1（失败）：

  ```
  [
    {
      "ssid": "TP-LINK_35EB",  // str, WiFi名称
      "mode": 0,               // int, 模式
      "security": 4,           // int, 加密方式: 0=不加密,1=wep,2=wpa-psk,3=wpa-Enterprise,4=wpa2-psk
      "channel": 161,          // int, 信道
      "signal_strength": 100,  // int, 信号强度
      "speed": 150,            // int, WiFi速率(Mbps)
      "ap_address": "04:f9:f8:f1:35:ed", // str, AP物理地址
      "rssi": -35,             // int, 真实信号强度(0~-100, 0最强)
      "res": 0                 // int, 预留字段
    }
  ]
  ```

---

#### **24. connect\_wifi\_async(cfg\_str)**

- **描述**：设置WiFi配置。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "ssid": "TP-LINK_35EB", // str, WiFi名称
    "password": "12345678", // str, 密码
    "security": 4           // int, 加密方式(0-4)
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **25. disconnect\_wifi()**

- **描述**：断开WiFi连接。
- **入参**：无。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **26. get\_network\_param()**

- **描述**：获取当前连接网络信息。
- **入参**：无。
- **返回**：网络信息字典或-1（失败）：

  ```
  {
    "ip_addr": "XXX.XXX.3.1",      // str, IP地址
    "gateway": "XXX.XXX.3.1",      // str, 网关地址
    "pri_dns": "XXX.XXX.3.1",      // str, 主DNS地址
    "sec_dns": "",                 // str, 备用DNS地址
    "ssid": "EZVIZ-11-11",         // str, WiFi名称
    "mode": 0,                     // int, 模式
    "security": 4,                 // int, 加密方式(0-4)
    "channel": 161,                // int, 信道
    "signal_strength": 100,        // int, 信号强度
    "speed": 150,                  // int, WiFi速率(Mbps)
    "ap_address": "04:f9:f8:f1:35:ed" // str, AP物理地址
  }
  ```

---

#### **27. set\_network\_parameters(cfg\_str)**

- **描述**：设置网络参数。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "ip_addr": "XXX.XXX.3.1", // str, IP地址
    "gateway": "XXX.XXX.3.1", // str, 网关地址
    "pri_dns": "XXX.XXX.3.1", // str, 主DNS地址
    "sec_dns": "XXX.XXX.3.1"  // str, 备用DNS地址
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **28. start\_local\_snapshot(cfg\_str)**

- **描述**：摄像头抓图。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "type": 0,                     // int, 存储类型: 0=本地, 1=云端
    "dest_addr": "/mnt/mmc02/.../xxx.jpg", // str, 存储路径
    "resolution": 0                // int, 分辨率类型: 0=720p, 1=1080p, 2=2K
  }
  ```
- **补充说明**：  
  type=1 时可用 get\_storage\_id 查询云存储ID。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **29. led\_control(enable)**

- **描述**：开启/关闭LED指示灯。
- **入参**：  
  enable (int) - 1=开启, 0=关闭。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **30. white\_led\_control(enable)**

- **描述**：开启/关闭白光灯。
- **入参**：  
  enable (int) - 极1=开启, 0=关闭。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **31. infrared\_control(enable)**

- **描述**：开启/关闭红外灯。
- **入参**：  
  enable (int) - 1=开启, 0=关闭。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **32. start\_media\_record(cfg\_str)**

- **描述**：开始视频存储。
- **入参**：  
  cfg\_str (极str) - JSON字符串：

  ```
  {
    "stream_idx": 0,               // int, 码流索引: 0=主码流, 1=子码流
    "type": 0,                     // int, 存储类型: 0=本地, 1=云端
    "pack_type": 1,                // int, 封装类型: 0=ps流, 1=mp4
    "dest_addr": "/mnt/mmc02/.../xxx.mp4" // str, 目标存储地址
  }
  ```
- **补充说明**：  
  type=1 时可用 get\_storage\_id 查询云存储ID。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **33. stop\_media\_record(cfg\_str)**

- **描述**：异步停止媒体录制。
- **入参**：  
  cfg\_str (str) - JSON字符串（需与开始录制参数一致）：

  ```
  {
    "stream_idx": 0,
    "type": 0,
    "pack_type": 1,
    "dest_addr": "/mnt/mmc02/.../xxx.mp4"
  }
  ```
- **返回**：0（停止请求已受理）；非0（操作失败）。

---

#### **34. start\_media\_preview(cfg\_str)**

- **描述**：媒体预览推流。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "stream_idx": 0,       // int, 码流类型(必须为1)
    "enable": 0,           // int, 使能: 0=关闭, 1=开启
    "url": "rtmp://xxx.xxx.xxx.xxx/live/xxx" // str, 推流地址
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **35. start\_mic\_record(cfg\_str)**

- **描述**：开始录音。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "type": 0,                     // int, 存储类型: 0=本地, 1=云存
    "dest_addr": "/mnt/mmc02/.../XXXX.aac" // str, 存储地址
  }
  ```
- **补充说明**：  
  type=1 时可用`get\_storage\_id 查询云存储ID。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **36. stop\_mic\_record(cfg\_str)**

- **描述**：异步停止录音。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "type": 0,
    "dest_addr": "/mnt/mmc02/.../XXXX.aac"
  }
  ```
- **返回**：0（停止请求已受理）；非0（操作失败）。

---

#### **37. get\_storage\_id(dest\_addr)**

- **描述**：根据存储地址查询云存储ID。
- **入参**：  
  dest\_addr (str) - 文件存储地址。
- **返回**：  
  storage\_id (str) - 文件存储ID（查询不到时返回空字符串）。
- **数据来源**：  
  save\_video\_by\_time, ptz\_panoramic, start\_local\_snapshot,`start\_media\_record,start\_mic\_record。

---

#### **38. get\_and\_clear\_all\_storages()**

- **描述**：查询所有云存储ID。
- **入参**：无。
- **返回**：云存储ID字典或空字典：

  ```
  {
    "/XXX/XXX1.jpg": "E1$0$11$0$PY4O4B~$N1$BF4904736-1$00$0a81",
    "/XXX/XXX2.jpg": "E1$0$12$0$PY4O4B~$N1$BF4904736-1$00$0a86"
  }
  ```
- **数据来源**：同 get\_storage\_id。

---

#### **39. set\_wdr(cfg\_str`**

- **描述**：设置宽动态使能和等级。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "enable": 0, // int, 使能: 0=关闭, 1=开启, 2=自动
    "level": 10  // int, 宽动态等级(0-100)
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **40. get\_wdr()**

- **描述**：获取宽动态使能和等级。
- **入参**：无。
- **返回**：宽动态配置字典或-1（失败）：

  ```
  {
    "enable": 1,  // int, 使能状态
    "level": 10   // int, 宽动态等级
  }
  ```

---

#### **41. get\_alarm\_info()**

- **描述**：获取告警状态列表。
- **入参**：无。
- **返回**：告警状态列表或空列表：

  ```
  [
    {
      "appid": "app_human_detect", // str, 告警标识
      "enable": 1                  // int, 开关状态: 1=开启
    },
    {
      "appid": "app_db_detect", 
      "enable": 1
    }
  ]
  ```
- **告警标识说明**：  
  app\_video\_change（画面变化）, app\_human\_detect（人形告警）, app\_db\_detect（大噪声检测）, app\_babycry\_detect（哭声检测）, app\_fix\_gesture\_recognize（手势识别）。

---

#### **42. set\_alarm\_status(cfg\_str)**

- **描述**：告警状态设置。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "appid": "app_db_detect", // str, 告警标识
    "enable": 1               // int, 开关状态: 1=开启
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **43. get\_alarm\_status(cfg\_str)**

- **描述**：告警状态查询。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "appid": "app_db_detect" // str, 告警标识
  }
  ```
- **返回**：告警状态字典或空字典：

  ```
  {
    "appid": "app_db_detect",
    "enable": 1
  }
  ```

---

#### **44. get\_alarm\_events()**

- **描述**：获取告警事件（最多200条）。
- **入参**：无。
- **返回**：告警事件列表或空列表：

  ```
  [
    {
      "app_id": "app_db_detect",  // str, 告警标识
      "alarm_time": 1754632006    // long, 告警时间戳
    },
    {
      "app_id": "app_human_detect",
      "alarm_time": 1754632010
    }
  ]
  ```

---

#### **45. set\_mirror(cfg\_str)**

- **描述**：镜像翻转画面。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "channel": 1,       // int, 通道(主码流)
    "mode": "CENTER",   // str, 翻转模式(仅支持CENTER)
    "enable": 1         // int, 开关: 1=开启
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **46. get\_osd\_param()**

- **描述**：获取OSD配置参数。
- **入参**：无。
- **返回**：OSD参数字典或空字典：

  ```
  {
    "attribute": 4,  // int, OSD属性: 1=透明闪烁, 2=透明不闪烁, 3=不透明闪烁, 4=不透明不闪烁
    "datetime_overlay": {
      "enabled": 1,     // int, 开关
      "clock_type": 极0,  // int, 时间类型: 0=24小时制
      "positionx": 576, // int, 日期横坐标
      "positiony": 8732, // int, 日期纵坐标
      "type": 0,        // int, OSD格式类型(0-5)
      "display_week": 0 // int, 是否显示星期: 0=不显示
    },
    "channame_overlay": {
      "enabled": 0,     // int, 开关
      "positionx": 608, // int, 通道名横坐标
      "positiony": 514, // int, 通道名纵坐标
      "name": "Camera_BF4904736" // str, 通道名称
    }
  }
  ```

---

#### **47.set\_osd\_param(cfg\_str)**

- **描述**：设置OSD参数。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "attribute": 4,
    "bDateTimeOverlay": 1,      // int, 时间OSD开关(仅设置用)
    "bchannelNameOverlay": 1,   // int, 通道名称OSD开关(仅设置用)
    "datetime_overlay": { ... }, // 同get_osd_param
    "channame_overlay": { ... }  // 同get_osd_param
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **48. set\_audio\_volume(cfg\_str)**

- **描述**：设置音频参数。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "mic_volume": 10,     // int, 麦克风音量(0-100)
    "speaker_volume": 50  // int, 扬声器音量(0-100)
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **49. get\_audio\_volume()**

- **描述**：获取音频参数。
- **入参**：无。
- **返回**：音频配置字典或-1（失败）：

  ```
  {
    "mic_volume": 10,
    "speaker_volume": 50
  }
  ```

---

#### **50. set\_image\_style(cfg\_str)**

- **描述**：设置画面风格模式。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "mode": 1 // int, 模式: 1=标准, 2=写实, 3=艳丽, 4=明亮
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **51. get\_image\_style()**

- **描述**：获取画面风格模式。
- **入参**：无。
- **返回**：风格模式字典或-1（失败）：

  ```
  {
    "mode": 1
  }
  ```

---

#### **52. set\_media\_resolution(cfg\_str)**

- **描述**：设置分辨率（仅主码流）。
- **入参**：  
  cfg\_str (str) - JSON字符串：

  ```
  {
    "resolution": 1 // int, 分辨率: 0=1080P, 1=2304*1296, 2=2592*1944, 3=4064*3040
  }
  ```
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **53. get\_media\_resolution()**

- **描述**：获取分辨率。
- **入参**：无。
- **返回**：分辨率字典或-1（失败）：

  ```
  {
    "resolution": 1
  }
  ```

---

#### **54. start\_play\_file\_speaker(path)**

- **描述**：播放音频文件（仅支持AAC格式）。
- **入参**：  
  path (str) - 音频文件绝对路径。
- **返回**：0（操作成功）；非0（操作失败）。

---

#### **55. stop\_play\_speaker()**

- **描述**：停止语音或文件播报。
- **入参**：无。
- **返回**：0（操作成功）；非0（操作失败）。