# ISAPI接入指南

> ISAPI接入指南

> 更新时间: 2026-05-25T16:38:17.000+08:00

> 文档ID: 1885 | 来源树: OPEN_API

---

## 1. 海康ISAPI协议是什么？

### 1.1 海康ISAPI

海康ISAPI是海康的一套HTTP通信协议，自2013年创建以来，内容已扩展至智能设备管理、车辆识别、停车场管理、人脸智能、门禁权限管理、录播管控等，这些功能配合海康提供的智能硬件设备（例如AI智能前后端产品、通用前后端产品、门禁产品、交通产品、对讲产品、报警产品、热成像产品等多种网络硬件设备），被广泛应用于交通、消防、安检、教育、建筑等多种行业。

### 1.2 萤石透传ISAPI协议

萤石可以在公网环境下透传海康ISAPI协议，实现远程的海康品牌设备控制与管理。使接入萤石云的海康设备可以轻松使用ISAPI协议管控设备。（海康提供的ISAPI协议本身仅只适用于“硬件与客户端处于同一个局域网或专网下有固定IP地址”或“硬件或硬件所接的路由器有固定公网IP地址或域名”的网络环境）

### 1.3 为什么要用ISAPI文档？

在业务方案的完善中，往往会用到很多带有丰富功能的海康硬件设备，例如工地场景-执法记录仪远程巡检、停车计费场景-停车砖应用、智慧社区建设-门禁管理……这些带有丰富功能的设备能够帮助业务方案在行业中打造更多的优势与方案竞争力，因此，在开发者中颇受欢迎。

那么如何更好的使用海康设备呢？如何快速集成这些功能呢？使用ISAPI文档即可快速实现！

### 1.4 产品优势

- 申请便捷：通过海康开放平台可在线快速签约，申请协议不再困难。
- 使用便捷：直接透传ISAPI协议，可快速实现对海康设备的高级功能使用
- 功能全面：自2013年创建以来，ISAPI总计已经有11000多个接口，内容包括设备管理、车辆识别、停车场管理、人脸智能、门禁权限管理审讯管控、录播管控等功能，满足各行业客户对于设备的管控需求。

## 2. 如何看懂海康ISAPI协议文档？

### 2.1 申请协议

通过海康开放平台可直接在线申请ISAPI文档：
![](http://resource.eziot.com/group2/M00/00/BA/CtwQFmU4yYKAXEb8AABkZ_h7TtA755.png)

- 申请入口：<https://open.hikvision.com/agreement?type=100>
- 申请指南：<https://open.hikvision.com/agreement/guide>
- 申请要求：公司信息支持企业E签宝在线签约
  ![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U4ykOARWZvAAE_ES954iQ180.png)

## 2.2 阅读协议文档

根据设备型号或项目申请到的ISAPI文档往往动辄500页以上，那作为我们萤石和海康的合作伙伴，想要快速集成设备的功能，应该如何去看这份文档呢？

下面，我们以门禁设备-明眸为例，带大家一起来看懂ISAPI文档！

### 1. 获得文档

在线上完成签署，我们获得到的就是对应的完整ISAPI文档，加压后我们可以看到《ISAPI开发指南》、《错误码》、《日志类型》、《字典信息》这样四分文档。

其中，我们在开发过程中核心需要了解的就是《ISAPI开发指南》、《错误码》两份。

![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U4ywuASKCoAACaaOFX6nY862.png)

![](http://resource.eziot.com/group2/M00/00/BA/CtwQFmU4zAOAdnxbAABQGIkhgBI448.png)

### 2. 看懂《ISAPI开发指南》

下面，让我们一起来话3分钟时间了解最为重要的《ISAPI开发指南》

整份文档可以分为前提概述、功能实现方式介绍、接口文档三个部分。

| 部分 | 包含内容 |
| --- | --- |
| 前提概述 | 包含概览、应用场景、所属网络模型中的层级、ISAPI框架介绍。 |
| 功能实现方式介绍 | 包含所有功能的实现方式介绍，其中包含每个功能实现步骤中分别调用了哪些ISAPI接口的描述。 |
| 接口文档 | 对应“功能接口”，里面是这个设备支持的ISAPI下行接口的介绍。 |

![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U4zYyANeJpAAC8O61EXLM465.png)
![](http://resource.eziot.com/group2/M00/00/BA/CtwQFmU4zZ2AM4ZyAADJ7ml-Ogk945.png)

- 功能实现方式介绍：

如果我们当前要使用门禁设备实现“人员管理”功能，我们在《功能实现方式介绍》模块中找到对应（或者类似）的功能模块介绍

![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U4zeKAeuItAANfgdsaBnw227.png)

看文档我们可以获知，这部分的内容里面包含查询、设置、新增、修改、删除几个功能点。接下去我们可以根据需求，选择其中对应的功能，按照其中给的逻辑进行实现：

![](http://resource.eziot.com/group2/M00/00/BA/CtwQFmU4zhaAH3w6AAFe_XNATu8386.png)

- 接口文档：

我们可以看到实现人员新增中共涉及到两个接口（见上图）。接下去我们在《接口文档》中搜索对应接口，可以看到接口的具体描述。
![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U4zwSAJL3jAAK-4fj-244344.png)
将接口结合《3.1 调用协议接口（端/平台->设备，ISAPI下行透传）》中的萤石透传方式调用接口即可。（《ISAPI开发指南》文档中展示业务相关的数据、参数描述；《调用协议接口（端/平台->设备，ISAPI下行透传）》中仅展示透传方案以及透传所需相关参数）

### 3. 看懂《错误码》

此份在文档中包含该设备在使用过程中所有可能产生的报错码及其报错原因。（针对输出参数Response Body部分）

## 3. 如何使用海康ISAPI协议进行开发？

### 3.1 调用协议接口（端/平台->设备，ISAPI下行透传）

#### \* 端 / 平台 ->设备

- **URL**

https://open.ys7.com/api/hikvision/{isapi协议上的 请求路径}

- **接口描述**

该接口用于从端或平台下发送ISAPI协议请求到设备,该接口支持json和XML形式的信令透传

- **接口分类**

根据协议选择,例如GET、PUT、POST

- **请求参数Resquest Header 部分**

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| EZO-AccessToken | String | 授权过程获取的access\_token | Y |
| EZO-DeviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| EZO-Date | String | 当前时间，示例：2017-12-01 10:00:00 | Y |
| Content-Type | String | ISAPI 请求Body的内容类型，例如：application/xml ,如果信令为json格式,请填入application/json | Y |

- **请求参数Resquest Body 部分**

如果为XML，示例如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<NTPServer version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
   <id>1</id>
   <addressingFormatType>ipaddress</addressingFormatType>
</NTPServer>
```

如果为JSON，示例如下：

```
{
   "Zone":{
   "id":1,
   "zoneName":"test",
    "zoneType":"Instant"
   }
}
```

- **输出参数Response Body部分**

如果为XML，示例如下：

```
<?xml version="1.0" encoding="UTF-8"?>  
<storageExtension xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">  
<!--ro, opt, object, 获取存储策略配置, attr:version{req, string, 协议版本}-->  
<LoopEnable>  
<!--ro, opt, bool, 是否启用硬盘循环覆盖-->true  
</LoopEnable>  
</storageExtension>
```

如果为JSON，示例如下：

```
{
   "Zone": {
   "id": 1,
   "zoneName": "test",
   "zoneType": "Instant"
    }
}
```

输出参数Response Body部分通用错误码：

详见获取到的ISAPI文件包中，错误码.xlsx文件。

- **输出参数Response Header部分（xml）**

| Header参数名 | 类型 | 描述 |
| --- | --- | --- |
| EZO-Code | String | 返回码 |
| EZO-Message | String | 返回信息 |

输出参数Response Header部分通用错误码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | success | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20002 | Device not exists | 设备不存在 |
| 20006 | Net error | 网络异常 |
| 20007 | Device off line | 设备不在线 |
| 20008 | Device response timeout | 设备响应超时 |
| 20018 | The user doesn't own the device | 该用户不拥有该设备 |

接口调用示例：

获取设备状态【GET】

```
curl --location --request GET 'https://open.ys7.com/api/hikvision/ISAPI/System/status' \
--header 'EZO-AccessToken: {{at}}' \
--header 'EZO-DeviceSerial: G75147751' \
--data-raw ''
```

配置指定通道编码参数【PUT】

```
curl --location --request PUT 'https://open.ys7.com/api/hikvision/ISAPI/Streaming/channels/101' \
--header 'EZO-AccessToken: {{at}}' \
--header 'EZO-DeviceSerial: J72665109' \
--header 'Content-Type: application/xml' \
--data-raw '<?xml version="1.0" encoding="UTF-8"?><StreamingChannel xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
<id>1</id>
<Video>
<videoCodecType>H.264</videoCodecType>
<videoResolutionWidth>1920</videoResolutionWidth>
<videoResolutionHeight>1080</videoResolutionHeight>
</Video>
</StreamingChannel>
'
```

### 3.2 接收ISAPI消息（设备->端/平台，ISAPI上行消息）

#### 1. 开通消息推送服务，并开通ISAPI消息类型的接收。

- 进入控制台—产品中心—消息推送—点击立即开通
  ![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U477WAEzazAAKq4xMEupY496.png)
- 填写消息推送配置信息：

（1）消息类型：目前平台支持6种消息类型上报，其中，需要选择开通ISAPI上行消息。

（2）Webhook回调地址：自定义回调地址，必需提供https url作为webhook地址；

（3）失败重试最大次数：消息推送失败后，重复推送的次数

![](http://resource.eziot.com/group2/M00/00/BB/CtwQFmU478mASFerAAL11xnZjmY240.png)

#### 2. 配置消息图片/视频存储空间。

- 开通云录制功能

（1）开通地址：https://open.ys7.com/console/preCloudRecord.html
![](http://resource.eziot.com/group2/M00/00/BB/CtwQFmU48KqAGnO0AAF3WIIue34920.png)

- 创建isapi图片存储

（1）创建存储项目文件夹：开通服务后，点击项目管理，点击右上角创建新的项目
![](http://resource.eziot.com/group2/M00/00/BB/CtwQFmU48VeAdriGAAD8B-KyHnA920.png)

（2）填写新建项目信息

![](http://resource.eziot.com/group2/M00/00/BA/CtwQF2U48YuAILuGAABF-DsQ0JQ418.png)

- 创建isapi存储项目

选择「设为isapi项目」，后续账号下设备产生的isapi告警图片会自动转存至此项目文件夹。
![](http://resource.eziot.com/group2/M00/00/BB/CtwQFmU48buAWIJKAAD9ouwDl2g097.png)

#### 3. 调用接口获取图片

- **URL**

https://open.ys7.com/api/lapp/mq/downloadurl

- **接口描述**

该接口用于下载ISAPI图片

- **接口分类**

GET

- **请求参数Resquest Header 部分**

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| Content-Type | String | application/x-www-form-urlencoded | Y |

- **请求参数Resquest Params 部分**

| Head | Head | Head | Head |
| --- | --- | --- | --- |
| appKey | String | 开发者appkey | Y |
| fileKey | String | ISAPI上行报文中的picUrl字段 | Y |

- **接口调用示例：**

```
curl --location --request GET 'https://open.ys7.com/api/lapp/mq/downloadurl?appKey=1f6f231875144exxxxd08aaaffce7e4&fileKey=ISAPI_FILES/F998xx556_1/2021061021xxx4298-F99xx9556-1-10000$encrypt=2,2021-06-10T21:10:40,a75a0221147xxx464e9dce2028'
```

## 4. 问题咨询

可以联系萤石设备接入小助手：

![](http://resource.eziot.com/group1/M00/00/E8/CtwQE2U7cbGAfZi6AAE_ES954iQ580.png)