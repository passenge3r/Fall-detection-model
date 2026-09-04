# 3D数字人-Windows 端渲染SDK 接入说明

> Windows 端渲染SDK 接入说明

> 更新时间: 2026-05-25T16:37:55.000+08:00

> 文档ID: 2431 | 来源树: AI

---

# Windows 端渲染SDK 接入说明

# 操作手册

## 第一章 系统综述

### 1.1 概述

萤石智能数字人软件是萤石自主研发，能够以图文信息合成语音面部表情、肢体动作等多种输出信息，结合多模态决策机制，实现实时交互的能力。同时借助文本、语音等多种唇形驱动方式，以及表情和动作的多维度编排能力，提升拟人交互能力，保障与人互动交互的效果与体验。

### 1.2 功能简介

数字人形象以及商显大屏+摄像头结合全新打造的硬件产品，与开发者共同服务于多行业，实现迎宾接待、产品介绍、实时咨询、实时互动等功能

### 1.3 运行环境

Windows 10+

## 第二章 登录

### 2.1 功能概述

注册码，也被称为许可证密钥或产品密钥，是一个用于软件许可的特殊代码，通常由字母和数字组合而成。当你购买购买软件后，生产商会通常会提供一个注册码。

以下是注册码的一些主要功能：

验证合法性: 注册码的主要功能是确保软件是从开发者或正规渠道购买的，这样开发者就能控制其软件的分发，并确保自身利益得到保障。

激活软件: 在你购买并安装软件后，通常需要输入注册码来激活和启用全功能。在成功输入注册码并由软件认证后，限制将被移除。

防止软件盗版: 通过将注册码与唯一的硬件设备ID或用户账户关联起来，软件开发者可以避免其软件被非法复制和分发。

提供许可信息: 注册码可能会包含信息，比如，许可证持有人的信息，软件版本，许可数量(多用户许可证)等等。

![](https://resource.eziot.com/group1/M00/01/29/CtwQE2ZoYWyANiWCAAAw5_qQkcM734.png)

### 2.2 注册码获取操作说明

2.2.1.进入引导页面[萤石开放平台-为企业客户提供全球化、一站式硬件智能方案](https://open.ys7.com/cn/s/beginnerGuide)

![](https://resource.eziot.com/group1/M00/01/29/CtwQEmZoYXWAQjSIAADZaWmJqto432.png)

2.2.2、用户注册[萤石开放平台](https://open.ys7.com/view/register/register.html)

![](https://resource.eziot.com/group1/M00/01/29/CtwQE2ZoYa-ASiLNAAIToTvg0Nk634.png)

2.2.3、**注册码**：使用EZVIZ\_Win\_MetaHuman\_FingerPrint\_Console.exe 程序，在电脑上运行，会生成一个fingerprint.txt 文件，将文件交给对接人即可。对接人将此信息，生成对应的注册码。

2.2.4.将注册码复制到数字人程序的编辑框，点击确定

2.2.5.进入程序

## 第三章 配置项

### 3.1功能概述

在和数字人交互之前，需要想定义好协议，根据协议和数字人进行交互

**3.1.1 UDP Socket 协议要求**

此框架结构包含主控程序、数字人端程序、web端程序。

其中主控程序与数字人端程序交互使用Socket UDP + JSON的方式，由数字人端程序作为服务端，主控程序作为客户端，可以使用Socket Tool 工具作为主控，也可以使用自研的主控。

数字人端程序与web端程序交互采用websocket通讯，数字人端作为通讯的服务端，web作为客户端。

中控程序与web不进行通讯，需要主控向web端的指令由数字人端进行转发。

**3.1.2 TTS （语音合成）**

语音合成由数字人端来完成。

由主控发送给数字人端程序文本语句，数字人端收到后获取回复文本信息，自行生成 TTS音频文件播放，并且需要告知web端，开始播放语音和播放完成状态信息。

不同厂商的sdk整合因开发语言而异，请开发者自行前往开放平台注册获取对应的sdk 和开发文档

**3.1.3 配置文件**

| 字段 | 作用 | 字段说明 |
| --- | --- | --- |
| voice\_name | 发音人 | 不同的发音人代表了不同的音色.  思琪siqi温柔女声 (默认)  思悦 siyue 温柔女声  艾雅 aiya 严历女声  艾夏 aixia 亲和女声  艾美 aimei 甜美女声  艾雨 aiyu 自然女声  艾悦 aiyue 温柔女声  艾婿 aijing 严历女声  小美 xiaomei 甜美女声 |
| speed | 语速（暂不支持配置） | 合成音频对应的语速，取值范围：[0,1]，数值越大语速越快。默认值：1 |
| volume | 音量 | 合成音频的音量，取值范围：[0,100]，数值越大音量越大。 默认值：100 |
| sample\_rate | 合成音频采样率(暂不支持配置) | 合成音频采样率，支持参数，16000，8000，默认为16000 |

默认配置为：

[TTS]

voice\_name=siqi

speed=1

volume=100

路径：

Project\Windows\AIhuman\Config\ TTSConfig.ini

**3.1.4 Socket配置文件**

| 字段 | 作用 | 字段说明 |
| --- | --- | --- |
| server\_ip | 数字人socket server ip | 数字人作为socket 服务，根据ip 和port ，用来接收信息,默认为127.0.0.1 |
| server\_port | 数字人socket server port | 默认为8084 |
| client\_ip | 数字人socket client ip | 数字人作为socket 客户端，根据ip 和port ，用来发送信息,默认为127.0.0.1 |
| client\_port | 数字人socket client port | 默认为8085 |

默认设置为：

[Socket]

server\_ip=127.0.0.1

server\_port=8084

client\_ip=127.0.0.1

client\_port=8085

路径：

Project\Windows\AIhuman\Config\Socket.ini

### 3.2操作说明

1.打开主控软件和数字人软件

2.编辑主控软件，发现相关信息

3.数字人收到信息然后进行解析，并转发到Web端

4.提取解析后的数据，对其进行TTS请求，并将状态同步给web端

5.数字人收到TTS流，进行播放

6.数字人收到动作信息，同步进行展示相应的动作

## 第四章 和数字人交互

### 4.1功能概述

此说明主要是主控与数字人端的交互说明。

数字人端与web端主要为数据传递，交互内容与主控和数字人端交互内容为主。

通信协议为udp+json的形式

### 4.2操作说明

4.2.1 发送内容通用形式

```
{
"category":(Num),
"data":{
(key1):(val1),
(key2):(val2),
(key3):(val3)
}
}
```

| 字段 | 值 | 说明 | 是否传递web |
| --- | --- | --- | --- |
| category | 0 | ASR语音识别消息 | 否 |
|  | 1 | NLP自然语言处理消息 | 是 |
|  | 3 | ACTION动作消息 | 否 |
|  | 4 | VIDEO视频消息 | 是 |
|  | 5 | 控制虚拟人物位置及大小消息 | 否 |
|  | 6 | 控制web端界面切换消息 | 否 |
|  | 7 | 数字人转发，不解析消息 | 是 |
| data | {…} | 不同类型消息包含数据不同 |  |

---

| 字段 | 值 | 值 | 说明 |
| --- | --- | --- | --- |
| answer |  | String | 语音播报tts文本（改字段需要数字人端解析获取用作tts合成） |
| text |  | String | 前端显示文本（web端获取做显示） |
| picture |  | String | 图片文件名，默认http路径 |
| mode |  | Num | 提示词模式，默认为模式1。目前支持两种模式。 |
| action |  | String | 动作名，对应数字人具有的动作名 |
| type |  | Num | 0： 空 1： 文本 2：图片/多图 3：视频 |

4.2.2 文字消息

```
{
"category":1,
"data":{
"action":"",
"answer":"好的，现在帮您办理。",
"ask":"银行卡",
"picture":"http://xx/xx/xx/card.jpg",
"type":2
}
}
```

4.2.3 图片消息

```
{
"category":1,
"data":{
"action":"",
"answer":"农业银行欢迎您",
"ask":"农业银行",
"picture":"http://xx/xx/xx/logo.png",
"text":"农业银行欢迎您",
"type":5
}
}
```

4.2.4 动作消息

```
{
"category":3,
"data":{
"action": "jugong"
}
}
```

动作集合：

| **动作名称** | **描述** |
| --- | --- |
| jugong | 数字人鞠躬 |
| baishou | 数字人摆手 |
| baiyoushou | 数字人摆右手 |
| baishuangshou | 数字人摆双手 |
| xiongqian | 数字人手放胸前 |

4.2.5 视频消息

```
{ 
    "category":4, 
    "data":{ 
        "video_state": 0, 
        "video_name":"http://video.chinanews.com/flv/2019/04/23/400/111773_web.mp4"
    }
}
```

4.2.6 控制虚拟人物位置及大小消息

```

"category":5, "data": { "position":
{
"x": 10,
"y": 30
},
{
"category":4,
"data":{
"video_state": 0,
"video_name":"http://xx/xx/000.mp4"
}
}
"rotation":
{
"x": 0.0, "y": 0.0,
"z": 0.0
},
"scale":
{
"x": 1.0, "y": 1.0,
"z": 1.0
}
}
}
```

| 字段 | 是否必需 | 说明 |
| --- | --- | --- |
| Position | NO | x: 控制数字人左右移动 y : 控制数字人上下移动 |
| rotation | NO | Float类型 数字人旋转角度 |
| scale | NO | Float类型 数字人缩放比例 |

4.2.7 富文本消息

```
{
    "category":1,
    "data":{
        "RichText":"<div id='se-knowledge'><p>这是标题<br><strong>这是图片<br></strong><img width='547' height='648' src='https://beebot-knowledgecloud-aliyun-public-cn-shanghai.oss-cn-shanghai.aliyuncs.com/kc/1207282/kc-media/kc-faq-oss/wrong1-1695609995718.png' slate-data-type='image'></p><link rel='stylesheet' href='https://g.alicdn.com/isipfe/docs/rich.css?'></div>",
        "type": 3
    }
}
```

4.3 图片示例

使用Socket
Tools工具和数字人交互
![](https://resource.eziot.com/group1/M00/01/29/CtwQEmZoZCyASaPGAADSBqEZam8261.png)

4.4 点击提示词

提示词：客户可以根据自己的需求，动态配置提示词以及答案

操作：

使用鼠标、或者手指，点击屏幕上的提示词 。 数字人会播报提示词对应的答案。

提示词如下图所示：

![](https://resource.eziot.com/group1/M00/01/29/CtwQE2ZoZESAd_P0AAEgLSQwwqA404.png)

说明：

提示词可以动态配置，根据用户的需求，进行自定义配置。

## 第五章 换肤系统

### 5.1 功能概述

用户根据自己需求，动态的更换背景

### 5.2 操作说明

配置路径：Project\Windows\AIhuman\backgroundImageI.png

要求：

1.  分辨率必须为1080\*1920

2.  格式后缀为jpg或者png

举例：以下为默认配置的背景图片

## 第六章 退出系统

### 6.1 功能概述

退出程序

### 6.2 操作说明

1.使用键盘Esc，即可退出数字人程序。

2.或者点击数字人右上角，会弹出弹框，点击Exit，即可退出数字人程序

如下图所示：

真机效果图如下所示：

人物效果图目前有两种，用户可以根据需求来选择其中一个。更多的人物效果，敬请期待

效果图可以参看产品概述里文档