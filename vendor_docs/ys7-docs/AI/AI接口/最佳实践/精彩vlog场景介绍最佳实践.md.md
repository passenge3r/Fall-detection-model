# 精彩vlog场景介绍最佳实践.md

> 精彩vlog场景介绍最佳实践.md

> 更新时间: 2026-06-01T15:12:52.000+08:00

> 文档ID: 3949 | 来源树: AI

---

# 精彩瞬间vlog方案介绍

> 游客在体验各类景区或其他场景之后，期望能有个精彩的Vlog游玩短视频。萤石提供软硬一体的解决方案给开发者，开发者可基于萤石提供的全套产品，快速集成并进行流量变现。

# 1、越来越火热的文旅vlog

随着抖音、微信视频号、小红书等自媒体的发展带动，短视频已成为人们获取信息、种草的重要方式。据《CSM2020-2021 短视频价值分析报告》显示2021年用户已突破10.2亿，市场价值超1000亿。

## 短视频+旅游，实现数字文旅场景创新

![](https://resource.eziot.com/group2/M00/01/05/CtwQFmhMDYmAEUo2ABdKw7yUVNY530.png)

## 当前景区短视频痛点

针对以上难点，萤石推出了萤石精彩瞬间vlog方案

# 2、萤石精彩瞬间vlog方案

## 让每位游客成为景区的代言人

通过智能高清摄像机捕捉游客精彩时刻，串联多景点游玩视频，合成游记vlog。

本文主要是说明：**开发者快速集成API**，帮助开发者快速搭建精彩瞬间vlog小程序及相关后台的说明。

![](https://resource.eziot.com/group1/M00/01/8E/CtwQE2hMGpaAIl6CAAMjmIfW0Jk445.png)

如果您不是开发者，而是景区客户，需要搭建一整套小程序，请联系小助手，我们会提供萤石生态合作伙伴给你提供方案支持。包括小程序开发、管理后台开发、支付、空境视频拍摄等，详询：[精彩视频vlog萤石生态方案介绍](https://resource.eziot.com/group1/M00/00/F3/CtwQE2VtTSuAN0y0AAAmQb_3exk350.png)

## 适用场景

![](https://resource.eziot.com/group2/M00/01/04/CtwQF2hMDZCAPKocACcaodCINY4866.png)

目前主要是针对以上场景提供精彩瞬间vlog的能力：

- 景区：漂流、自然景区等景点，如玉龙雪山、孔庙等合作客户案例
- 室内游玩：比如攀岩、室内游玩等
- 党建：入党仪式宣言等，适合党建
- 展厅：例如海康展厅，提供每个客户的参展vlog，帮助企业宣传

## 交互流程介绍

![](https://resource.eziot.com/group2/M00/01/05/CtwQFmhMDZKARc46AC_TWnBEvj0064.png)

开发者/景区需要针对精彩视频提供者6个内容的产品，主要包括：

### ①设置打卡点

![](https://resource.eziot.com/group2/M00/01/04/CtwQF2hMDZSAPn-nACNSD6iCzio169.png)

综合考虑视频生成、下载及分享传播的因素，建议标准配置4-7个点位的智能人脸摄像头，通过引导物料、导览标识吸引游客前往指定打卡地。

### ②让游客对着镜头互动拍摄

游客对着摄像头进行自由动作，比如挥挥手、比个V之类的

![](https://resource.eziot.com/group1/M00/01/8E/CtwQEmhMEguAXWfRAATuGHmKn9I184.png)

### ③让游客扫描二维码进入应用

有几种模式：可以第一个地点后就直接生成视频，也可以经过多个点后，再合成一个整体的视频给到游客。

### ④精彩vlog合成

![](https://resource.eziot.com/group2/M00/01/05/CtwQFmhMDY6ASMe6ABfAtaIckJY763.png)

一般来说，通过萤石云视频vlog相关模板设置，可以将片头、空镜头等，将一大段的视频合成一个视频。

然后就可以开放这个视频给游客进行下载了。

### 合成的视频可以参考萤石的Demo视频：

vlog参考视频1：[精彩视频vlog萤石版Demo1.mp4](https://izhstatic.ys7.com/vasp-openweb/1749809967853_12-12%E6%99%AF%E5%8C%BAvlog%E8%90%A4%E7%9F%B3%E7%89%88demo.mp4)

vlog参考视频2：[精彩视频vlog萤石Demo2.mp4](https://izhstatic.ys7.com/vasp-openweb/1749809996810_3%E6%9C%8826%E6%97%A5.mp4)

### ⑤分享下载

引导游客进行三方平台分享下载。

# 3、开发对接

## 0.前提

### 1）摄像机购买

目前推荐海康文体卫精彩视频专属摄像机，由于涉及不同场景，比如室内室外、长距离/短距离、快速/慢速、4G/WiFi等等条件，建议直接海康销售，根据景区场景选择对应的摄像机。

比如：

如果景区是漂流场景，则需要防水、需要5-20米距离，需要快速抓拍，但是人脸同时抓拍的人脸数只需要50个以下，因此可以推荐类似于这种摄像机：

DS-2CD7U447MWD-XZ/JM(1050/4)(B)

原因：

①设备支持人脸抓拍模式：支持对运动人脸抓拍和属性分析，支持快速抓拍和优选抓拍两种模式，支持抓拍图片去重功能

②最高分辨率可达400万像素，并在此分辨率下可输出30fps实时图像，图像更流畅，支持透雾、电子防抖，支持宽动态120 dB

③适合5-20米距离的人脸抓拍

因此，景区或者开发者选择摄像机时，可以跟海康销售提前沟通，确定自己的场景，然后选择合适的设备，如果不知道自己需求，也可以咨询萤石小助手获取推荐设备。

### 2）将设备连入萤石开放平台

注册萤石云开放平台，链接:https://open.ys7.com/cn/s/index,获取AK、SK等关键接口对接配置信息

### 3）开通消息通知等服务

**开通通知服务：** 由于视频剪辑等服务处理，需要用到消息通知等服务，建议开通服务：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/5127)

**创建云录制项目：** 进入萤石云开放平台-云存储产品-云录制产品，创建项目，并为项目设置ISAPI项目(只能设置一个ISAPI项目)

## 1.对接：给设备开通云存储

**为什么要开通萤石云存储服务？**

根据萤石之前最佳实践，一般游客扫描人脸照片后，需要在30秒内获取剪辑好的视频，因此建议提前将每天的景区视频保存到云端，如果开发者不在意这个30秒时间，则也可以视频保存在本地，不上传云端。

**怎么开通**

一般海康设备都是不具备萤石云存储能力的，一般有两种方法：

### ①海康设备定制连续云存储

备注：由于一般景区视频需要裁剪前后时间，建议设备定制连续云存储。

定制流程，建议咨询海康销售。定制后，通过地址：[余额开通云存储](https://open.ys7.com/help/1400) 开通设备云存储

### ②通过NVR设备直接使用云录制2.0进行录制

云录制的使用说明详见：

暂不支持云录制2.0，需要联系产品定制

## 2.景区人脸对接流程说明

![](https://resource.eziot.com/group1/M00/01/8E/CtwQEmhMD2qAERPuAAGZe_giaW8948.png)

## 3.人脸对接：项目相关流程

### 3. 1景区vlog项目创建

> 该接口用于创建项目，每个项目的人脸库是隔离的，不同景区之间的人脸库不会互通

参考文档：

<https://open.ys7.com/help/3976>

### 3.2 给设备开通配置景区vlog人脸检索权限

> 该接口用于设备上报后的人脸消息进入项目里

[查看文档](https://open.ys7.com/help/4067)

说明：

①一些景区当天来当天就走的，建议人脸的周期为1天，如果遇到邮轮等情况需要人脸保持7天以上的可以设置多天。

②人脸入库当前最多支持5万/项目，若要超过请联系小助手扩容，会产生额外成本及检索速度

### 3.3 创建人脸数据库

> 该接口用于设备人脸图片上报后，将人脸进行人脸识别，提取人脸特征值，放入对应项目的人脸特征库

[查看文档](https://open.ys7.com/help/4320)

### 3.4 人脸检索

> 当用户上传图片后，该接口会将人脸进行识别，并与指定的人脸库里的人脸进行比对，最后将视频片段时间给到开发者

---

- 接口URL

https://open.ys7.com/api/service/open/scenic/spot/vlog/video/retrieval

**请求**

- Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |

**body**

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| faceImageUrl | string | Y | 人脸图的url地址 |  |
| spaceId | string | Y | 存储空间隔离id,云录制1.0使用项目id,云录制2.0使用spaceId |  |
| projectId | string | Y | 项目id，长度0-31 |  |
| timeInterval | string | N | 录制视频时，人脸抓拍告警时间点前后的的时间间隔，单位：秒 |  |

**请求示例**

```
curl --location 'https://open.ys7.com/api/service/open/scenic/spot/vlog/video/retrieval' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'accessToken: at.1ne41gy9d1w6m37xcp0it14z6hdiv9h' \
--data-urlencode 'spaceId=testboyan' \
--data-urlencode 'projectId=projectId_SPH1' \
--data-urlencode 'faceImageUrl=https://open.ys7.com/api/lapp/mq/downloadurl?appKey=b9a3ad6e8026410095d825&fileKey=ISAPI_FILES/FF4130602_1_3033/20241211203016404-FF4130602-2$encrypt=2,2024-12-11T20:35:10,9571ec1d' \
--data-urlencode 'timeInterval=8'
```

- 响应

**返回数据**

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| data | object | data |  |
| -taskId | string | taskId |  |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |

**返回示例**

```
{
    "data": {
        "taskId":"222222222"
    },
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

**错误码**

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 500 | 500 | 服务器异常 |  |
| 400 | 400 | 参数错误 |  |

### 3.5 景区vlog查询任务结果（GET）

> 景区vlog查询任务结果

---

- 接口URL

https://open.ys7.com/api/service/open/scenic/spot/vlog/task/files

- 请求

**Header**

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |

- query

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| taskId | string | Y | 任务id | 上一个接口返回的任务id |

**请求示例**

```
curl --location 'https://open.ys7.com/api/service/open/scenic/spot/vlog/task/files?taskId=675bf3b4398e184c4c7' \
--header 'accessToken: at.1ne41gy9d1w6m37xcp0it14z6hdiv9hv-54xtkhnvno'
```

- 响应

**返回数据**

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |
| data | object | data |  |
| -taskId | string | taskId | 任务id |
| -projectId | string | projectId | 项目id |
| -videoDataList | array<object> | videoDataList |  |
| --spaceId | string | spaceId | 存储空间隔离id,云录制1.0使用项目id,云录制2.0使用spaceId |
| --deviceSerial | string | deviceSerial | 录像所属的设备序列号 |
| --localIndex | string | localIndex | 录像所属的设备通道 |
| --fileId | string | fileId | 文件id |
| --downloadUrls | array<string> | downloadUrls | 下载地址 |
| --alarmTime | string | alarmTime | 人脸抓拍告警时间 |

**返回示例**

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "taskId": "675bf3b4398e184c4c734b51",
        "projectId": "projectId_SPH1",
        "videoDataList": [
            {
                "spaceId": "testboyan",
                "fileId": "15c4d5d874ed4acc8a2229f806a114af",
                "deviceSerial": "FQ8436675",
                "localIndex": "1",
                "downloadUrls": [
                    "http://av-talk-test.oss-cn-hangzhou.aliyuncs.com/REC_FILES/9f74b527ce5b4b9b86f324bb6dafd9fb/testboyan/FF41306"
                ],
                "alarmTime": "2024-12-16 15:32:55"
            },
            {
                "spaceId": "testboyan",
                "fileId": "81e6a6bf9b6848cab70beaf9c5c528d3",
                "deviceSerial": "FQ8426675",
                "localIndex": "1",
                "downloadUrls": [
                    "http://av-talk-test.oss-cn-hangzhou.aliyuncs.com/REC_FILES/9f74b527ce5b4b9b86f324bb6dafd9fb/testboyan/FF413060"
                ],
                "alarmTime": "2024-12-16 17:32:55"
            }
        ]
    }
}
```

**错误码**

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 500 | 500 | 服务器异常 |  |
| 400 | 400 | 参数错误 | &nbs |

### 3.6 视频片段剪辑

获取3.5的视频时间跟片段后，通过视频剪辑接口，进行视频剪辑：

①视频剪辑接口地址：<https://open.ys7.com/help/2863>

②通过传入3.5返回的多个时间戳起止点，将视频进行裁剪，添加转场效果，并合成，最终返回剪辑任务ID

备注：如果要制作一段精彩的视频，可以通过上传片头片尾、背景音乐、转场视频等进行合成

③上传片头片尾、背景音乐、转场视频等

④添加转场动效

转场效果：参考：<https://open.ys7.com/help/3737>

⑤视频剪辑文件查询：<https://open.ys7.com/help/3717>

通过传入剪辑任务ID，返回剪辑视频URL。

### 3.7 下载视频

开发者可以根据返回的视频URL进行在线点播操作，包括获取在线播放地址、二次操作，还可以进行下载到本地等操作。[参考文档](https://open.ys7.com/help/4145)

### 3.8 人脸分数

人脸抓拍照片分数定义：设备在抓拍的时候，会根据游客的角度、照片清晰度，给照片打一个分数，0-100分之间。

鉴于抓拍人脸清晰度不一导致识别不准确等问题，现在默认景区人脸图片分值为70分。也就是在人脸入库时，会自动舍弃70分以下的照片。

如果开发者觉得视频太短，则可以降低分值，但是当前未开放接口，请联系小助手调整分值。

### 3.9 视频剪辑片段

当前会根据人脸的图片OSD时间，给出人脸前后5秒，但是部分场景5秒可能不够，开发者可以自定义前后时间值。

![](https://resource.eziot.com/group1/M00/01/8E/CtwQE2hMEEGAQK1gAADwuCwpeU0748.png)![](https://resource.eziot.com/group2/M00/01/04/CtwQF2hMDYuAPvn6AAJ-7N4W9Jc250.png)