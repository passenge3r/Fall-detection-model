# ERTC最佳实践：IOT设备与微信VOIP通话方案

> ERTC最佳实践：IOT设备与微信VOIP通话方案

> 更新时间: 2026-05-25T16:36:25.000+08:00

> 文档ID: 4301 | 来源树: 音视频

---

# IOT设备与微信VOIP通话方案介绍

> 本文档主要阐述如何将IoT设备与微信VOIP打通，实现微信接听IoT设备呼叫的方案及微信呼叫IOT设备的方案

# ⼀. 背景

随着萤石S10、RK3等视频通话摄像头发布，设备与手机端通信接听模式主要为“通话消息提醒”，接通流程不够便捷，难以做到一步接通，甚至导致错失部分呼叫。

萤石开放平台提供“设备端—客户端”的实时音视频（ERTC)通话能力。同时，为了实现用户在发起语音通话场景下更快捷地接听，萤石对接听方式进行了全面优化，通过与微信开放平台的云云对接，让所有萤石云上的设备拥有拨打微信电话的功能。

![](https://resource.eziot.com/group1/M00/01/8B/CtwQE2gCBb2AabPiAB3BVktrFj0041.gif)

弹窗接听

![](https://resource.eziot.com/group1/M00/01/8B/CtwQEmgCBfWAFKyXACYGsanb_8I112.gif)

锁屏接听

---

具体介绍文档可以参考：[萤石ERTC+VoIP发布，支持微信小程序弹窗接听智能设备呼叫](https://mp.weixin.qq.com/s/gQT29hn-e2YE3Bl4XcWuZQ)

而这些产品能力，都应用到了萤石实时音视频产品，简称ERTC。

本文档主要介绍如何将门禁、门铃、门锁、通话摄像头等设备接入微信VOIP的产品开发：

其中，与APP端的呼叫接听可以参考文档：<https://open.ys7.com/help/4332>

# 二、接入流程说明

⼀次完整的呼叫流程包括如下⼏个步骤：

**①设备/小程序发起呼叫**

**② 设备⼊会**

**③ 微信⼊会**

开发者只需在云端调⽤萤⽯云API，即可实现对微信⽤⼾的呼叫。

# 三、整体流程说明如下：

## **接入准备（默认已完成[前置条件准备](https://open.ys7.com/help/4918)）**

1. 开通设备开放平台视频通话能力（备注：由于设备通道跟联系人是绑定的，而设备默认走萤石云app的联系人因此视频呼叫不会到开放平台，要让设备视频走到开放平台，开发者请**必须**按程序调用这个接口，否则视频会无法发起。） [点击查看](https://open.ys7.com/help/4893)
2. 开通消息推送服务 [点击查看](https://open.ys7.com/help/566)，并订阅ertc相关消息类型 [点击查看](https://open.ys7.com/help/4913)
3. 开发者配置微信公众平台小程序回调地址 [微信公众平台](https://mp.weixin.qq.com)
4. 创建联系人，依赖appId， [点击查看](https://open.ys7.com/help/4335)
5. 设备关联联系人，依赖步骤3完成联系人创建后与设备进行关联 [点击查看](https://open.ys7.com/help/4338)
6. 开发者需维护设备联系人和微信用户小程序openId的唯一关联，实现一对一呼叫。 [微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/wx.login.html) | [微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html)

> 具备ERTC能力的设备端呼叫开发者客户端，（开发者客户端与服务端之间的连接需要开发者自行通过手机厂商推送/极光推送等三方厂商服务完成），其中webhook消息内会带上房间信息，开发者客户端需要使用对应客户端 SDK加入webhook消息中的房间。

## **用例：设备呼叫小程序客户端**

1. 开发者先注册小程序

- 注册微信⼩程序开发者⾝份，并开通硬件设备能⼒，参考：[小程序设备消息 | 微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/framework/device/device-message.html)
- 在微信开放平台认证设备，参考：[设备认证 | 微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/framework/device/device-register.html)

2. 开发者授权设备

实现⽤⼾授权设备 设备如果要向⽤⼾发起通话，需要⽤⼾在⼿机微信端先对设备进⾏授权。 参考：[用户授权设备 | 微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/framework/device/voip/auth.html)

3. 用户操作设备上添加的联系人（依赖接入准备里的第3条添加设备联系人）发起呼叫
4. 开发者监听webhook消息[点击查看](https://open.ys7.com/help/4913) ，获取到appId和房间号信息，通过开放平台接口获取到加入房间所需要的[通话Token](https://open.ys7.com/help/1872)（原：资源token） ，在设备端调用对应sdk方法加入房间，进行通话
5. 设备挂断/取消呼叫等操作，开发者都会收到对应的webhook消息，进行后续处理
6. 当设备呼叫微信联系人时，开放平台先把对应微信的消息通知（通过webhook）给开发者，开发者先调微信开放平台的呼叫接口，微信开放平台会分配相关房间给到开发者。

①开发者将该房间信息回调给萤石开放平台，通知开放平台邀请设备加入房间

该步骤，要通知开放平台加入微信房间，参考文档：[微信voip操作](https://open.ys7.com/help/4298)

②开发者同时将微信接听/拒绝的状态同步给开放平台，开放平台完成呼叫状态同步

③接听后，如果客户挂断电话，同样也要同步相关状态给萤石开放平台，完成挂断同步

## **用例：微信小程序呼叫设备**

1. 开发者配置微信公众平台小程序回调地址
2. 开发者授权设备

实现⽤⼾授权设备 用户如果要向设备发起通话，需要⽤⼾在⼿机微信端先对设备进⾏授权。 参考：[用户授权设备 | 微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/framework/device/voip/auth.html)

3. 用户操作小程序上的授权设备列表，发起呼叫。参考：[呼叫设备 | 微信开放文档](https://developers.weixin.qq.com/miniprogram/dev/framework/device/voip-plugin/api/callDevice.html)

①开发者通过开放平台接口获取到加入房间所需要的[通话Token](https://open.ys7.com/help/1872)（原：资源token）。

②开发者在微信回调中调用萤石开放平台呼叫接口。

4. 开发者监听webhook消息[点击查看](https://open.ys7.com/help/4913) 。

①设备接听/拒接/挂断等操作，开发者都会收到对应的webhook消息，通知开放平台加入/拒绝/退出微信房间。参考文档：[微信voip操作](https://open.ys7.com/help/4298)。

5. 通话中，如果小程序挂断电话，也要同步相关状态给萤石开放平台，完成挂断同步。
6. 小程序取消呼叫时，也要调用开放平台取消呼叫接口。

## **更多：其他开放接口**

联系人相关管理接口：

| 接口名称 | 接口地址 |
| --- | --- |
| 开通视频通话能力 | 前往查看：[点击查看](/help/4893) |
| 添加设备联系人 | 前往查看：[点击查看](/help/4335) |
| 查询联系人列表 | 前往查看：[点击查看](/help/4336) |
| 删除联系人 | 前往查看：[点击查看](/help/4337) |
| 设备关联联系人 | 前往查看：[点击查看](/help/4338) |
| 查询设备关联联系人列表 | 前往查看：[点击查看](/help/4339) |
| 删除设备联系人 | 前往查看：[点击查看](/help/4340) |