# AI台球自动剪辑最佳实践.md

> 更新时间: 2026-05-25T16:37:49.000+08:00

> 文档ID: 3821 | 来源树: AI

---

# AI台球自动剪辑最佳实践

> 文档说明：目前开放平台已经提供了视频录制、视频点播、视频剪辑、AI台球算法等能力，开发者如何快速接入并输出自己的AI台球精彩剪辑可以参考此文档进行接入。

# 1. 越来越火热的无人台球需求

![](https://resource.eziot.com/group1/M00/01/53/CtwQEmcXPgqALsWuAAceMexVYjU237.png)

一个小房间，3-4张小球桌，一堆人围在一起打球，但是前台却没有服务人员，人员扫码自助完成一整套的台球娱乐活动，这就是这些年越来越火热的无人自助台球。

随着无人台球的火热，老板不在台球厅，又希望能给打球的爱好者提供更好的服务，还希望他们能自发帮助宣传，AI台球精彩视频就能帮助开发者实现这一套逻辑。

①给用户提供打球过程视频，用户打完球就能收到一段打球过程，在线就能看。

![](https://resource.eziot.com/group1/M00/01/53/CtwQE2cXPg2ADfkKAAGsvp96liw683.png)

②用户可以自行剪辑5秒-10分钟片段，然后下载到手机

③分享视频到开发者自己平台，或者分享朋友圈带上台球厅定位

![](https://resource.eziot.com/group1/M00/01/53/CtwQEmcXPg-ATCB7AAjUInA1UiQ711.png)

![](https://resource.eziot.com/group1/M00/01/53/CtwQE2cXPhKAAO25AALL4pmUulQ617.png)

分享视频，带上定位，宣传台球门店。

那么随着技术的不断迭代，试想一下，如果用户打完球几分钟后，就能自动给他一段他打球的精彩瞬间，是不是更酷呢？

# 2、开放平台AI剪辑整体说明

随着自助台球的越来越火热，萤石开放平台凭借物联网+算法的能力，为更多的台球开发者提供更多的服务能力。

![](https://resource.eziot.com/group1/M00/01/53/CtwQEmcXPhSAMJxzAAJJ6e2qCj4989.png)

台球用户手动剪辑的接口，用户可以参考之前的视频剪辑文档，而本文重点讲解如何通过AI算法，自动给用户提供精彩视频。

文档主要介绍以下几块内容：

| 功能 | 功能描述 |
| --- | --- |
| 算法能力 | 介绍当前萤石已有的算法能力 |
| 摄像头要求 | AI算法对台球桌的摆放、视角的大小都有一定的要求，再调用算法之前，建议开发者在工程上进行整理 |
| 智能生成 | 算法+视频剪辑接口结合才能输出完整的精彩视频 |

# 产品介绍

萤石开放平台云录制+云点播+算法

云录制是基于海康威视/萤石等物联网IPC设备的云端视频录制，在调用算法之前，要求视频必须在云端保存。云录制的调用方法可以参考：[云录制视频](https://open.ys7.com/help/1975)

云点播：视频剪辑+视频智能生产，并提供云端视频播放分发

算法：萤石开放平台基于萤石蓝海大模型，为各类开发者，各类场景提供各种富有生命力的算法。

# 接入说明

## 0、前提条件

①请在萤石开放平台注册开发者账号。如您已有开发者帐号，可以跳过这一步。

②在消息推送控制台开通消息推送服务 消息推送服务开通操作手册，并联系客服，后台开通AI算法分析结果消息类型：ys.open.ai.resultData，算法分析结果是通过云信令消息异步推送的。

③开通AI算法服务reasoning，如未开通可联系客服支持。

④联系客服手动开通该接口调用权限。提供如下信息：

- 设备序列号
- 开发者账号

## 1、台球桌摆放

由于台球桌的角度、摄像头的角度等，都会影响算法的稳定性与效果，建议按如下文档进行台球桌的摆放

[文档：台球桌摄像头架设安装说明](https://open.ys7.com/help/3739)

备注：如果不按稳当说明的摆放，则可能会影响最终算法效果，可能会漏算或者错算

## 2、台球算法说明

### ①台球桌颜色

目前台球桌桌布只支持绿色、灰色

![](https://resource.eziot.com/group1/M00/01/53/CtwQE2cXPhiAR1QvAAFPExKXqAw816.png)

绿色桌面

![](https://resource.eziot.com/group1/M00/01/53/CtwQEmcXPhqASkr2AAKcHMPmUBc724.png)

目前随着接入者的增多，开发者可以提供更多的球桌颜色给到我们进行训练，可以联系客服

### ②目前只支持国标台球

目前只支持中式台球，也就是俗称的8球制台球，斯诺克、9球等规则都有一定的出入，无法做到很好的兼容，如果是其他球类，则只能提供进球识别等基础算法，其他黑八进袋、白球进袋等可能会造成误判。

## 4、台球精彩瞬间AI识别试用

功能列表

| 功能 | 能力 | 是否具备 |
| --- | --- | --- |
|  | 识别开局 | 是 |
|  | 识别开球进球 | 是 |
|  | 识别无关时刻 | 是 |
| 基本功能 | 识别击球 | 是 |
|  | 识别击球结果 | 是 |
|  | 对局结束 | 是 |
|  | 支持多种颜色球桌(灰色、绿色) | 是 |
|  | 支持多角度球桌摆放(横、竖) | 是 |
| 进阶能力 | 进球片段提取合成Vlog | 是 |

### **1）第一步：视频录制**

通过萤石云存储，或云录制，可以将设备上的打球过程存到云端。

第一步：视频录制得到得任务ID进行文件查询，参考接口：<https://open.ys7.com/help/1373>

备注：目前只支持云录制mp4录制的1.0版本，暂不支持加密录制。后续开放中，预计12月上线，敬请期待、

视频录制得到得任务ID进行文件查询，参考接口：<https://open.ys7.com/help/1373>

调用示例：

```
curl -X GET \
 'https://open.ys7.com/api/v3/open/cloud/task/d0015b1769e845b0a478e9ec3fc3555c?accessToken=at.cz52cslwb2dpac9s8d2wmmri72d1lix6-5c09lw8s6k-1kzsoyd-zhwd78nlb' \
 -H 'Postman-Token: 452b5ba3-0a9e-4a68-85a9-3186d06ec41d' \
 -H 'cache-control: no-cache'
```

输出结果：

```
{
 "meta": {
 "code": 200,
 "message": "操作成功",
 "moreInfo": null
 },
 "data": {
 "total": 1,
 "pageNumber": 0,
 "filesInfo": [
 {
 "projectId": "tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "fileType": 1,
 "status": 0,
 "fileCount": 1,
 "fileSize": 155208213,
 "duration": 660,
 "errorCode": "0",
 "expireTime": "2024-10-05T15:32:44",
 "storageType": 1,
 "lastTransferTime": null,
 "unfreezeTime": null,
 "createTime": "2024-09-05T15:32:44",
 "updateTime": "2024-09-05T15:32:44",
 "expectStartTime": "2024-09-05T14:51:00",
 "taskId": "7483e046975c4a69aae492c8ad69da82",
 "downloadUrls": ["http://xxx.xxx.xxxx/xxx.MP4"],
 "replayRecord": true
 }
 ],
 "pageSize": 10
 }
} }
}
```

### **2）调用AI分析接口，获取分析结果（云信令消息）**

AI剪辑说明：
普通功能接口参考：<https://open.ys7.com/help/3733>

通过传入视频url地址，AI算法自动分析后将结果（时间起止点）通过云信令返回给三方平台。

![](https://resource.eziot.com/group1/M00/01/4B/CtwQE2b4zFuAGWs-AADefhm20O0514.png)

### **3）调取视频剪辑接口，合成视频**

①视频剪辑接口地址：<https://open.ys7.com/help/2863>

②通过传入步骤2返回的多个时间戳起止点，将视频进行裁剪，添加转场效果，并合成，最终返回剪辑任务ID

备注：如果要制作一段精彩的视频，可以通过上传片头片尾、背景音乐、转场视频等进行合成

③上传片头片尾、背景音乐、转场视频等![](https://resource.eziot.com/group1/M00/01/53/CtwQE2cXPiCAMEMQAAWH9bUEhj8319.png)
点击控制台-云点播，点击上传音视频

④添加转场动效

转场效果：参考：</help/3737>

![](https://resource.eziot.com/group1/M00/01/53/CtwQEmcXPiOAebM3AEbIHDo4FwI850.png)

⑤视频剪辑文件查询：<https://open.ys7.com/help/3717>

通过传入剪辑任务ID，返回剪辑视频URL。

【begin\_time，end\_time】

调用示例：

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/video/convert' 
--header 'accessToken: {{accessToken}}' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'Content-Type: application/json' \
--data-raw '{
 "timeLine": [
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 },
 {
 // 使用对焦切换转场
 "type": "Transition",
 "subType": "directional"
 }
 ],
 "in": 0,// 算法分析出来的begin_time/1000
 "out": 2// 算法分析出来的end_time/1000
 },
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 },
 {
 // 使用对焦切换转场
 "type": "Transition",
 "subType": "directional"
 }
 ],
 "in": 8,// 算法分析出来的begin_time/1000
 "out": 10// 算法分析出来的end_time/1000
 },
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 }
 ],
 "in": 15,// 算法分析出来的begin_time/1000
 "out": 17// 算法分析出来的end_time/1000
 }
 ],
 // 背景音乐，需要在云点播中进行上传
 "audioTimeLines": [
 {
 "type": 3,
 "fileId": "l17q8HCC"
 }
 ],
 "fileName": "合成视频1"
}'

---响应

{
 "meta": {
 "code": 200,
 "message": "操作成功",
 "moreInfo": null
 },
 "data": {
 "taskId":"12314214"//剪辑任务id
 }
}
```

### **4）在线点播**

### 开发者可以根据返回的视频URL进行在线点播操作，包括获取在线播放地址、二次操作，还可以进行下载到本地等操作。