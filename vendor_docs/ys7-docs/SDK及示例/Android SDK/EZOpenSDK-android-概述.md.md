# EZOpenSDK-android-概述.md

> EZOpenSDK-android-概述

> 更新时间: 2026-06-02T14:03:35.000+08:00

> 文档ID: 4177 | 来源树: SDK及示例

---

# android SDK 概述

## 接入必读

- **已支持Google手机Android15系统16K PageSize，请升级至v5.27及以上。**
- 本SDK只包含真机调试的功能，不支持任何模拟器的调试。
- SDK支持的最低系统版本为Android 5.0、JDK 17.0以上版本。
- 适时查看[萤石开放平台官网](https://open.ys7.com/cn/s/download)的内容更新，特别是[SDK常见问题&问题反馈须知](https://open.ys7.com/help/4146) 和 [错误码文档](https://open.ys7.com/help/37)，我们对开发过程中遇到的多次被提问的问题进行汇总，文档能解决您90%的问题。
- android的Demo编译问题请自行处理，检查开发者本地Android Studio环境配置、gradle版本号、gradle插件版本号、网络等问题。

  

**SDK v5.27起，研发开发环境如下，供参考：**

- Android Studio: Android Studio Narwhal Feature Drop | 2025.1.2 Patch 2
- Gradle Version: 8.11.1 (distributionUrl=https://services.gradle.org/distributions/gradle-8.11.1-bin.zip)
- Android Gradle Plugin Version: 8.5.2 (classpath 'com.android.tools.build:gradle:8.5.2')
- Gradle JDK: JetBrains Runtime 21.0.6 - aarch64

## 简介

本文档用于说明萤石开放平台SDK Android版本接口之间的关系以及接口调用顺序，对开放平台SDK Android版本主要流程都有详细说明和代码示例。主要有功能介绍、安装说明、权限配置和主要流程介绍。

## 名词解释

| 名词 | 注解 |
| --- | --- |
| appKey | AppKey的申请可以参阅: [官网](https://open.ys7.com/console/application.html) |
| accessToken | 访问令牌，由server返回给client用于认证 |
| expire | accessToken过期时间 |
| DeviceSerial | 设备序列号，可在设备机身的标签贴纸上查看 |
| CameraNo | 设备通道号 |
| VerifyCode | 设备验证码，用于配网、预览、回放等，可在设备机身的标签贴纸上查看 |
| DeviceSerial+CameraNo | 摄像头唯一标志 |
| OSD | 视频播放当前时间 |
| PTZ | 云台控制，可以通过终端控制操作设备 |

## 功能介绍

| 功能 | 说明 |
| --- | --- |
| 账号对接(授权登录、sdk接口登录) | 授权到萤石云平台，复用萤石云平台能力 |
| 摄像头列表 | 得到对应账号下设备 |
| 直播预览 | 直播预览，可设置直播分辨率 |
| 查看回放（SD卡、硬盘录像机、云存储） | 回放 |
| 设备对讲 | 对讲（包含半双工对讲和全双工对讲） |
| 设备的设置功能 | 设备设置接口api |
| 设备控制接口（云台、镜头画面） | 云台控制 |
| WiFi配置 | 设备wifi配置 |
| 直播、回放边播边录 | 播放过程中录像 |
| 直播、回放边播边截屏 | 播放过程中截屏 |
| 告警消息 | 告警消息获取 |

## 隐私声明

### 1、收集个人信息说明

| 功能模块 | 收集个人信息类型 | 使用目的 |
| --- | --- | --- |
| 设备配网 | 物联网硬件设备信息：设备序列号、设备验证码 | 为最终用户提供物联网硬件设备的配网功能 |
| 客户端终端设备信息：客户端类型、客户端版本号、设备型号、设备硬件特征码、操作系统版本号 |
| 网络信息：WiFi账号、WiFi密码 |
| 设备对讲 | 物联网硬件设备信息：设备序列号、设备验证码 | 为最终用户提供物联网硬件设备的语音对讲功能 |
| 麦克风采集声音 |
| 设备预览、回放 | 物联网硬件设备信息：设备序列号、设备验证码 | 为最终用户提供物联网硬件设备的视频预览、回放功能 |
| 客户端终端设备信息：客户端类型、客户端版本号、设备型号、设备硬件特征码、操作系统版本号 |
| 网络信息：当前网络状态、网络连接方式 |

### 

请注意：基于不同的设备、系统及系统版本，以及开发者在集成、使用我们产品与/或服务时所决定的权限，我们实际接收到的信息可能会有所不同

### 2、权限说明

| 功能模块 | 权限名称 | 使用目的 |
| --- | --- | --- |
| 基本功能 | INTERNET 访问网络连接 | 用于网络连接 |
| READ\_PHONE\_STATE 获取手机状态 | 用于获取手机状态 |
| ACCESS\_NETWORK\_STATE 获取网络状态信息 | 用于获取网络状态信息 |
| ACCESS\_WIFI\_STATE 获取WiFi状态信息 | 用于获取WiFi状态信息息 |
| CHANGE\_NETWORK\_STATE 修改网络状态信息 | 当设备连接网络发生变化时，更改网络状态 |
| CHANGE\_WIFI\_STATE 修改WiFi状态信息 | 当设备连接网络发生变化时，更改网络状态 |
| CHANGE\_WIFI\_MULTICAST\_STATE 接收WLAN多播信息 | 当设备连接网络发生变化时，更改网络状态 |
| 设备配网 | ACCESS\_FINE\_LOCATION 访问精准定位 | 用户获取本地网络信息以完成设备配网 |
| CAMERA 相机 | 用于扫描二维码以添加物联网硬件设备 |
| 设备对讲 | RECORD\_AUDIO 录音 | 用于设备语音对讲功能，采集音频 |
| MODIFY\_AUDIO\_SETTINGS 更改音频设置 | 用于设备语音对讲功能，更改音频设置 |
| 视频通话 | CAMERA 相机 | 用于视频通话功能，采集视频 |
| RECORD\_AUDIO 录音 | 用于视频通话功能，采集音频 |
| BLUETOOTH 蓝牙 | 用于视频通话功能，蓝牙耳机连接 |