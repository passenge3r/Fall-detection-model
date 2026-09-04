# EZOpenSDK-harmony-权限配置.md

> EZOpenSDK-harmony-权限配置

> 更新时间: 2026-06-02T14:03:54.000+08:00

> 文档ID: 4190 | 来源树: SDK及示例

---

# 权限配置

权限配置是在工程的module.json5文件中进行配置。

路径为：工程目录->entry->src->main->module.json5

### 1. 应用数据存储持久化

SDK内部需要保证设备唯一性，生成一个随机的UUID保存在本地

```
// 允许应用存储持久化的数据，该数据直到设备恢复出厂设置或重装系统才会被清除。
    {
      "name": "ohos.permission.STORE_PERSISTENT_DATA",
      "reason": "$string:dependency_reason_wifi",
      "usedScene": {
        "abilities": [
          "EntryAbility"
        ],
        "when": "inuse"
      }
    },
```

### 2. 相册权限

如果需要使用开放平台播放器录像和截图并保存的功能，就需要配置相册权限。

```
// 媒体权限，用于将图片、录像保存至相册
    {
      "name": "ohos.permission.WRITE_IMAGEVIDEO",
      "reason": "{}",
      "usedScene": {
      }
    },
    {
      "name": "ohos.permission.READ_IMAGEVIDEO",
      "reason": "{}",
      "usedScene": {}
    }
```

### 3. 麦克风权限

如果需要使用设备对讲功能，就需要配置麦克风权限。务必在发起对讲前向系统申请麦克风权限，否则将导致第一次对讲异常。

```
// 麦克风权限，用于设备对讲
    {
      "name": "ohos.permission.MICROPHONE",
      "reason": "$string:dependency_reason_microphone",
      "usedScene": {
        "abilities": [
          "EntryAbility"
        ],
        "when": "inuse"
      }
    },
```

### 4. 摄像头权限

如果需要仿照demo实现扫码添加设备功能，就需要配置摄像头权限。

```
// 相机权限，用于扫描设备二维码
    {
      "name": "ohos.permission.CAMERA",
      "reason": "$string:dependency_reason_camera",
      "usedScene": {
        "abilities": [
          "EntryAbility"
        ],
        "when": "inuse"
      }
    },
```

### 5. WiFi权限

配网功能需要

```
// Wifi权限，用于设备WiFi配网
    {
      "name": "ohos.permission.SET_WIFI_INFO",
      "reason": "$string:dependency_reason_wifi",
      "usedScene": {
        "abilities": [
          "EntryAbility"
        ],
        "when": "inuse"
      }
    },
    // 获取Wifi状态
    {
      "name": "ohos.permission.GET_NETWORK_INFO",
      "reason": "$string:dependency_reason_internet",
      "usedScene": {
        "abilities": [
          "EntryAbility"
        ],
        "when": "inuse"
      }
    },
```