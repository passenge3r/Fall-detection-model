# SDK-webRTC-引导

> SDK-webRTC-引导

> 更新时间: 2026-05-25T16:36:33.000+08:00

> 文档ID: 1905 | 来源树: 音视频

---

# ERTC Web 引导

> 本教程基于 ERTC Web SDK 2.x 版本

本章主要介绍如何快速地将萤石 ERTC Web SDK 集成到您的项目中。

### 支持的平台

ERTC Web SDK 基于 WebRTC 实现，目前在浏览器各端的支持如下，部分功能的兼容性如有不同，会在功能详情中特殊说明：

|  | chrome | firefox | edge | safari | opera |
| --- | --- | --- | --- | --- | --- |
| windows | 72 | 80 | 80 | - | 90 |
| mac | 72 | 99 | 80 | 14.1.1 | 90 |

### 在项目中引入

1. npm 引入

您可以在项目中使用 `npm` 安装 `ertc-web`。

```
npm install ertc-web

<!-- js -->
import ERTC from 'ertc-web'
```

2. cdn 引入

```
<!-- html -->
<script src="https://cdn.jsdelivr.net/npm/ertc-web@2.1.2/dist/build/index.js">

<!-- js -->
const { ERTC } = window.EzRTCWeb
const ertc = new ERTC()
```

### 接入demo

- 在线演示：[react接入demo](https://openstatic.ys7.com/webrtc_gw_websdk/)
- github地址：[萤石ertc-web](https://github.com/Ezviz-OpenBiz/ertc-web-demo)