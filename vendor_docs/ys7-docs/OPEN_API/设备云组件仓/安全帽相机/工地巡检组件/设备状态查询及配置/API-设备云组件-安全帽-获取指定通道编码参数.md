# API-设备云组件-安全帽-获取指定通道编码参数

> API-设备云组件-安全帽-获取指定通道编码参数

> 更新时间: 2026-05-25T16:38:51.000+08:00

> 文档ID: 1487 | 来源树: OPEN_API

---

## 获取指定通道编码参数

接口分类：ISAPI能力

- URL

https://open.ys7.com/api/hikvision/ISAPI/Streaming/channels/

范例：https://open.ys7.com/api/hikvision/ISAPI/Streaming/channels/101（用于设置设备1通道主码流）

- 接口描述

获取指定通道编码参数。其中，针对安全帽相机（DS-MCH208），仅支持获取设备视频的视频编码类型、分辨率宽与高、视频码率类型、定码率、视频帧率。并且该设备仅包含主码流。

- method

GET

- header 请求头

| 参数名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| EZO-AccessToken | String | 授权过程获取的access\_token | Y |
| EZO-DeviceSeria | l String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| EZO-Date | String | 当前时间，示例：2017-12-01 10:00:00 | N |
| Content-Type | String | ISAPI 请求Body的内容类型，例如：application/xml ,如果信令为json格式,请填入application/json | N |

- URI参数定义

| 参数名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| trackStreamID | string | 定义为：channel\*100+streamType（1-mianstream，2-substream依次类推）；例如101表示通道1的主码流，302表示通道3的子码流能力集 | Y |

- Response Body输出参数（XML）

```
1.	<?xml version="1.0" encoding="UTF-8"?>
2.	<StreamingChannel xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
3.	  <!--ro, req, object, 编码参数, attr:version{opt, string, 协议版本}-->
4.	  <id>
5.	    <!--ro, req, string, 通道ID-->test
6.	  </id>
7.	  <Video>
8.	    <!--ro, opt, object, 视频配置-->
9.	    <videoCodecType>
10.	      <!--ro, req, enum, 视频编码类型, subType:string, [UNKNOWN#UNKNOWN,MPEG4#MPEG4,MJPEG#MJPEG,3GP#3GP,H.264#H.264,HK.264#HK.264,MPNG#MPNG,SVAC#SVAC,H.265#H.265,H.264BP#H.264BP,H.264HP#H.264HP,H.264SVC#H.264SVC,MPEG2#MPEG2]-->H.264
11.	    </videoCodecType>
12.	    <videoResolutionWidth>
13.	      <!--ro, req, int, 分辨率宽-->1
14.	    </videoResolutionWidth>
15.	    <videoResolutionHeight>
16.	      <!--ro, req, int, 分辨率高-->1
17.	    </videoResolutionHeight>
18.	    <videoQualityControlType>
19.	      <!--ro, opt, enum, 视频码率类型, subType:string, [CBR#定码率,VBR#变码率]-->CBR
20.	    </videoQualityControlType>
21.	    <constantBitRate>
22.	      <!--ro, opt, int, 定码率-->1
23.	    </constantBitRate>
24.	    <maxFrameRate>
25.	      <!--ro, req, int, 视频帧率, desc:帧率x100，如22帧下发2200,1/4帧下发25-->1
26.	    </maxFrameRate>
27.	  </Video>
28.	</StreamingChannel>
```

- Response Body输出参数通用错误代码

| 状态码 | 状态描述 | 子状态码 | 错误码 | 中文描述 |
| --- | --- | --- | --- | --- |
| 1 | OK | ok | 0x1 | 成功 |
| 2 | Device Busy | noMemory | 0x20000001 | 设备内存不足 |
| 2 | Device Busy | deviceBusy | 0x20000004 | 设备忙或设备无响应 |
| 4 | Invalid Operation | notSupport | 0x40000001 | 设备不支持 |
| 4 | Invalid Operation | lowPrivilege | 0x40000002 | 没有足够的权限进行此操作 |
| 4 | Invalid Operation | methodNotAllowed | 0x40000004 | HTTP方法不允许 |
| 4 | Invalid Operation | notActivated | 0x40000007 | 设备未激活 |
| 5 | Invalid Format | badXmlFormat | 0x50000001 | XML格式错误 |
| 5 | Invalid Format | badJsonFormat | 0x50000002 | JSON格式错误 |
| 5 | Invalid Format | badURLFormat | 0x50000003 | URL格式错误 |
| 6 | Invalid Content | badParameters | 0x60000001 | 参数错误 |
| 6 | Invalid Content | MessageParametersLack | 0x60000019 | 报文参数缺少 |
| 7 | Reboot Required | Reboot Required | 0x70000001 | 操作生效前需要重启 |

- Response Heade输出参数（xml）

| Header参数名 | 类型 | 描述 |
| --- | --- | --- |
| EZO-Code | String | 返回码Y |
| EZO-Message | String | 返回信息Y |

- Response Heade通用错误代码

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