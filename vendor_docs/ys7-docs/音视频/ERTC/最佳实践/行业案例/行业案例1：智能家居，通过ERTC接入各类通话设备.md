# 行业案例1：智能家居，通过ERTC接入各类通话设备

> 行业案例：智能家居，通过ERTC接入各类通话设备

> 更新时间: 2026-05-25T16:36:25.000+08:00

> 文档ID: 4927 | 来源树: 音视频

---

# 行业案例：智能家居，通过ERTC接入各类通话设备

> 该文档阐述萤石ERTC行业案例：实现智能家居设备的视频通话能力

# 行业背景

随着传统安防音视频能力的不断升级，传统安防音视频能力面临几个问题：

- 弱网环境通信：尤其是出海的海外环境
- 双向音视频：比如摄像头带一块屏幕，如何实现双向通话
- 低功耗

# 业务场景

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjsYJyAa5EQAAPndFGEHEs195.png)

| 场景 | 设备类型 | ERTC能力 |
| --- | --- | --- |
| 家庭监控 | 普通摄像头 | 1、视频监控升级；2、视频通话（挥手呼叫等） |
| 家庭视频通话 | 带屏摄像头 | 视频通话（双向通话） |
| 远程入户 | 智能门铃门锁等 | 与门铃、门锁等入户设备实现远程通话 |
| 移动交互 | 手表等 | 与手表等移动设备实现智能视频通话等 |

已经集成的ERTC 设备列表：<https://open.ys7.com/help/4922>

# 萤石ERTC提供能力

目前萤石ERTC产品主要提供针对设备端、客户端的各类能力升级，为IoT硬件设备提供核心场景价值

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jsYLKAFRGIAADXDkjEmJw988.png)

主要分为以下能力：

### 1、设备端SDK

萤石设备出厂自带ERTC能力，开发者只需要集成客户端SDK，即可完成各类设备的通话能力

同时也针对三方设备开放ERTC能力，具体可咨询[小助手](https://resource.eziot.com/group2/M00/00/DC/CtwQF2YnpAuAHlIaAACTVBcQxAg541.png)

### 2、音视频处理体验

萤石自研音频3A处理引擎：AEC、ANS、AGC
AI降噪：滤除环境中的非稳态噪声，如键盘声、嘈杂的背景人声

萤石自研3A处理算法，提供AI降噪能力

### 3、抗弱网能力

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjsYYyAG09GAAIbZaxJJhw892.png)

萤石ERTC为设备提供传输抗弱网策略

### 4、全球物联网节点

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jsYnyAL-IkAAPLWeqXVlU541.png)

### 5、智能家居生态设备全互联

针对海康威视、萤石网络大量设备，通过一个SDK，即可完成与所有设备的全互联，只需要一个SDK，就可以与超过10亿+设备实现无缝互联。