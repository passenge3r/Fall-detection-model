# EZUIKit SDK概述.md

> 更新时间: 2026-07-01T11:53:39.000+08:00

> 文档ID: 4274 | 来源树: SDK及示例

---

# 萤石EZUIKit SDK概述

> 该文档主要阐述EzOpen SDK（ezuikit-js）集成说明

## 接入前须知

萤石开放平台针对 Web 浏览器页面的视频接入需求，提供了完整的轻应用 UIKIT 解决方案。该方案主要包含 3 个 JavaScript SDK，其命名规则与底层协议强绑定，分别为：

- **EzOpen SDK（ezuikit-js）**：基于萤石私有 EzOpen 协议开发，由于该SDK开发开放较早，应用范围最广，功能最全，建议开发者优先集成
- **HTTP-FLV SDK（ezuikit-flv）**：基于 HTTP-FLV 标准流协议提供的 JavaScript SDK，全称萤石Web UIKit Http-FLV SDK，简称FLV SDK
- **HLS SDK（ezuikit-hls**：基于 HLS 标准流协议提供的 JavaScript SDK，全称萤石Web UIKit HLS SDK，简称HLS SDK

在集成前，开发者可以根据自身需求，及对应SDK提供功能，选择所需的SDK：[萤石开放平台音视频Web SDK功能差异说明](https://open.ys7.com/help/1772) 或者 [萤石开放平台音视频SDK集成概览](https://open.ys7.com/help/3925)

RTMP协议请使用小程序或三方播放库。

## 文档简介

本文档用于介绍萤石EzOpen SDK 集成说明，由于该SDK开发开放较早功能最全，以下所有文档不加后缀默认**轻应用**或 **UIKit** 即指萤石 EzOpen SDK，不再重复说明。若要集成Web HLS或者FLV SDK，请参考其他文档。

文档说明SDK接入方式、SDK支持的功能列表、SDK接入注意事项，以及常见问题的排查说明。

## 技术栈

*接入EZUIKit SDK可能会接触到的技术栈*

- HTML+JavaScript+CSS
- React、VUE等前端框架
- Uniapp、Taro等跨端开发框架
- WebView、iframe等WEB页面嵌入技术
- Websocket长连接
- Webpack、Vite、Rollup等构建工具
- LocalStorage、Webassembly、SharedArrayBuffer等浏览器特性
- npm、github、gitee等代码/插件管理平台

## 名词解释

| 名词 | 含义 |
| --- | --- |
| appKey | AppKey的申请可以参阅: [官网](https://open.ys7.com/console/application.html) |
| accessToken | 访问令牌，由萤石云开放平台颁发给客户端用于身份认证，获取方式可可以参阅: [OPEN API](https://open.ys7.com/help/19) |
| expire | accessToken过期时间 |
| DeviceSerial | 设备序列号 |
| ValidCode | 设备验证码 |
| CameraNo / ChannelNo | 设备通道号 |
| TalkChannelNo | 设备对讲通道号 |
| StreamType | 设备码流类型 |
| OSDTime | 视频播放当前时间 |
| PTZ | 云台控制，可以通过终端控制操作设备 |
| 硬解 | 使用PC的GPU进行画面渲染 |
| 软解 | 使用PC的CPU进行画面渲染 |
| 能力集 | 由摄像头报备的当前设备支持功能的集合 |

## 功能介绍

| 功能 | 说明 |
| --- | --- |
| 直播预览 | 直播预览，可设置直播分辨率 |
| 查看回放（SD卡、云存储、云录制2.0） | 回放 |
| 设备对讲 | 对讲（全双工） |
| 设备控制接口（云台、镜头画面） | 云台、焦距控制 |
| 直播、回放边播边录 | 播放过程中录像 |
| 直播、回放边播边截屏 | 播放过程中截屏 |
| AR实景标签展示 | 获取鹰眼相机实景标签数据 |

## 浏览器兼容情况

常见浏览器兼容情况详见文档：

| 系统/浏览器 | 内核类型 | WebAssembly 支持情况 |
| --- | --- | --- |
| 麒麟 / 银河麒麟（Kylin / NeoKylin） | 基于 Chromium / Firefox 内核 | 如果是新版 Chromium 内核（Chrome 90+），支持；老版本可能不支持或不完全支持 |
| 统信 UOS（UOS） | Chromium / Firefox | 新版本 Chromium 内核支持 |
| 深度 Deepin (DDE) | Chromium 内核 | 新版支持 |
| 中国版 IE（国产安全 IE） | Trident 内核（老 IE 核心） | 不支持 |
| 国产安全浏览器 / 360 浏览器 / 猎豹等 | 多为双核（Trident + Chromium） | Chromium 核心部分新版支持；WebAssembly 支持；老 Trident 核心不支持 |

## 隐私说明

更多隐私说明文档：[萤石开放平台音视频SDK隐私政策](https://service.ezviz.com/policy?id=248)

| 功能模块 | 收集个人信息类型 | 使用目的 |
| --- | --- | --- |
| 设备对讲 | 麦克风采集声音 | 为最终用户提供物联网硬件设备的语音对讲功能 |
| 设备预览、回放 | 客户端终端设备信息：客户端类型、客户端版本号、操作系统版本号；硬件设备信息：设备型号、设备硬件特征码、设备参数配置 | 为最终用户提供物联网硬件设备的视频预览、回放功能 |
| SDK | 生命周期执行耗时、播放模式及结果、功能执行结果 | SDK质量监测及优化 |