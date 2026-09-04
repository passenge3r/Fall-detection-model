# 最佳实践：海康门禁/IPC设备：呼叫微信VOIP通话方案

> 最佳实践：海康门禁/IPC设备：呼叫微信VOIP通话方案

> 更新时间: 2026-05-25T16:36:25.000+08:00

> 文档ID: 4357 | 来源树: 音视频

---

# 最佳实践：海康门禁/IPC设备：呼叫微信VOIP通话方案

> 本文档主要阐述如何将普通IoT设备（比如门禁/IPC等，未集成ERTC SDK）与微信VOIP打通，实现微信接听IoT设备呼叫的方案

前言：本文内容仅针对未集成ERTC的设备，开发者可以通过：设备端无联系人快速判断。

若设备端已经集成ERTC SDK，拥有联系人时，可以参考文档：<https://open.ys7.com/help/4332>

## ⼀. 背景

随着萤石S10、RK3等视频通话摄像头发布，设备与手机端通信接听模式主要为“通话消息提醒”，接通流程不够便捷，难以做到一步接通，甚至导致错失部分呼叫。

萤石开放平台提供“设备端—客户端”的实时音视频（ERTC)通话能力。同时，为了实现用户在发起语音通话场景下更快捷地接听，萤石对接听方式进行了全面优化，通过与微信开放平台的云云对接，让所有萤石云上的设备拥有拨打微信电话的功能。

![](https://resource.eziot.com/group1/M00/01/8B/CtwQE2gCBb2AabPiAB3BVktrFj0041.gif)

弹窗接听

![](https://resource.eziot.com/group1/M00/01/8B/CtwQEmgCBfWAFKyXACYGsanb_8I112.gif)

锁屏接听

---

具体介绍文档可以参考：[萤石ERTC+VoIP发布，支持微信小程序弹窗接听智能设备呼叫](https://mp.weixin.qq.com/s/gQT29hn-e2YE3Bl4XcWuZQ)

## 二、让门禁等普通设备也能实现微信VOIP通话方案

微信接听能力提高了设备接听率，而这些产品能力，都集成了萤石实时音视频SDK，简称ERTC SDK 。

如果设备已经集成了ERTC SDK，则可以直接与云端进行呼叫与通话，详情可见：<https://open.ys7.com/help/4332>

那**设备如果没有集成ERTC能力，比如海康门禁、门锁、门铃，甚至普通IPC有呼叫按钮**，但是没有双向SDK，有没有办法实现微信呼叫？

答案是：有，萤石ERTC同样也可以再服务端进行转发，将普通的呼叫转成ERTC能力，再与微信端进行联通，实现普通设备呼叫微信VOIP的能力。

---

![](https://resource.eziot.com/group1/M00/01/8B/CtwQEmgAiG6ATk88AAO68s5eV_w013.png)

图 ERTC 通话能力概述

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2g0ciKABf60AALyPeCt0lc784.png)

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmg0cxiAF6HCAAKqFjcaveM832.png)

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2g0cxqAU1RWAAJveHNuOgw640.png)

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmg0ciSAIz3uAALjJyJUl1E936.png)

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2g0ciaAMg6NAAKcNcQSjTA033.png)

如图，普通门铃，由于设备只有单向预览能力，但是依然可以走到微信呼叫（可向小助手索要原始视频），并且实现微信接听功能。

## 三、接入流程说明

⼀次完整的呼叫流程包括如下⼏个步骤：

**①设备发起呼叫**

发起呼叫利⽤了设备与萤⽯云之间的⻓连接。萤⽯云会将呼叫消息回调给开发者服务。此⽅案适合所有上萤⽯云且具备⾳视频能⼒的设备。

比如：门铃等门禁类设备，发起呼叫的时候，会给开发者通知

**② 设备⼊会**

目前萤石云兼容了设备接入ERTC与未接入ERTC的设备入会的方案，对于门禁类设备，开发者只需服务调⽤萤⽯云端API，即可将呼叫⽅设备加⼊实时会话。

- 对于不具备ERTC能⼒的设备，如现有的⼤多数智能⻔禁设备，萤⽯云可以调⽤设备的预览/对讲能⼒，使设备加⼊会话房间。这类设备可以实现单向视频，双向⾳
  频的效果。

**③ 微信⼊会**

开发者只需在云端调⽤萤⽯云API，即可实现对微信⽤⼾的呼叫。

整体流程说明如下：

![](https://resource.eziot.com/group1/M00/01/8B/CtwQE2gAjXWAcRpwAAMwfNSvbBg922.png)

图示：即为开发者调用微信呼叫的整体流程示意图

## 四、开发者开发内容

### 1）开发者服务端要求

1.监听设备呼叫事件(web hook)

服务端监听来⾃萤⽯云的事件消息。

设备产⽣呼叫事件后，会将事件回调⾄开发者服务器。

具体可以参考消息推送服务的介绍：[文档概述 · 萤石开放平台API文档](https://test12open.ezv-test.com/help/558)

2.创建会话房间。

在萤⽯云，⼀次实时通话要从创建⼀次会话房间开始。开发者需要创建房间，并为加⼊房间的设备和APP客⼾端签发授权token。

参考：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/1998)

3.拉设备⼊会

将会话房间信息发送给设备，使设备进⼊房间。

参考：<https://open.ys7.com/help/4297>

4. 指定呼叫对象

开发者服务可以对呼叫事件做⼀些过滤操作和云端逻辑。⽐如：

- 联系人能力，包括呼叫方称谓等：备注：由于当前开放平台联系人的功能是需要设备绑定联系人的，因此普通门禁设备呼叫无法使用联系人功能，需要开发者自行开发联系人功能。
- 动态指定某个呼叫对象、
- 同时呼叫多个呼叫对象（微信不支持同时呼叫多个微信账号）
- 呼叫排队
- 决定呼叫微信或者呼叫APP

5.呼叫微信

如果呼叫微信，则把开发者在微信注册的app\_id,要呼叫微信⽤⼾的open\_id发送⾄萤⽯云。由萤⽯云代理完成对微信⽤⼾的呼叫和通话。

文档：<https://open.ys7.com/help/4298>

### 2）开发者：微信呼叫要求

如需实现设备对⼩程序的呼叫，⼩程序需要做如下⼯作，如图所示：

![](https://resource.eziot.com/group1/M00/01/8B/CtwQEmgAjXeAcmCYAAEip9OO09E652.png)

开发者操作步骤说明：

1. 注册微信⼩程序开发者⾝份，并开通硬件设备能⼒，参考：<https://developers.weixin.qq.com/miniprogram/dev/framework/device/device-message.html>
2. 在微信开放平台认证设备，参考：<https://developers.weixin.qq.com/miniprogram/dev/framework/device/device-register.html>
3. 实现⽤⼾授权设备
   设备如果要向⽤⼾发起通话，需要⽤⼾在⼿机微信端先对设备进⾏授权。
   参考：<https://developers.weixin.qq.com/miniprogram/dev/framework/device/voip/auth.html>
4. 实现设备与微信之间的通话，需要⼩程序后台实现呼叫，媒体转发等逻辑。