# API-设备云组件-安全帽-配置设备定位参数

> API-设备云组件-安全帽-配置设备定位参数

> 更新时间: 2026-05-25T16:38:50.000+08:00

> 文档ID: 1482 | 来源树: OPEN_API

---

## 配置设备定位参数

接口分类：ISAPI能力

- URL

https://open.ys7.com/api/hikvision/ISAPI/Mobile/location

- 接口描述

获取设备定位参数。其中，针对安全帽相机（DS-MCH208），获取定位模式（关/开-GPS/开-北斗/开-GPS+北斗）、定位信息上传周期（1s-24小时）、卫星校时（开/关）

- method

PUT

- Request Header 请求头

| 参数名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| EZO-AccessToken | String | 授权过程获取的access\_token | Y |
| EZO-DeviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| EZO-Date | String | 当前时间，示例：2017-12-01 10:00:00 | N |
| Content-Type | String I | SAPI 请求Body的内容类型，例如：application/xml ,如果信令为json格式,请填入application/json | N |

- Response Body请求参数（XML）

```
1.	<?xml version="1.0" encoding="UTF-8"?>
2.	<MobileLocation xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
3.	  <!--req, object, 定位配置能力, attr:version{opt, string, 域名空间}-->
4.	<!—当adjustTimeEnabled值为true时，其余两个值必须设置-->
5.	  <locateMode>OFF</locateMode><!--req, enum, 定位模式, subType:string, [GPS#GPS定位,BDS#北斗定位,mix#混合定位]-->
6.	  <adjustTimeEnabled>true</adjustTimeEnabled><!--opt, bool, 卫星校时-->
7.	  <locationInfoUploadInterval>15</locationInfoUploadInterval><!--opt, int, 定位信息上传周期, range:[1,59], desc:最小为1s，最大为59s，默认为10s-->
8.	</MobileLocation>
```

- Response Body输出参数（XML）

```
1.	<?xml version="1.0" encoding="UTF-8"?>
2.	<ResponseStatus xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
3.	  <!--ro, req, object, 响应消息, attr:version{ro, req, string, 版本}-->
4.	  <requestURL>
5.	    <!--ro, req, string, 请求的URL-->null
6.	  </requestURL>
7.	  <statusCode>
8.	    <!--ro, req, enum, 状态码, subType:int, [0#OK,1#OK,2#Device Busy,3#Device Error,4#Invalid Operation,5#Invalid XML Format,6#Invalid XML Content,7#Reboot Required]-->0
9.	  </statusCode>
10.	  <statusString>
11.	    <!--ro, req, enum, 状态信息, subType:string, [OK#成功,Device Busy#设备忙,Device Error#设备异常,Invalid Operation#无效的操作,Invalid XML Format#无效的XML格式,Invalid XML Content#无效的XML内容,Reboot#设备重启]-->OK
12.	  </statusString>
13.	  <subStatusCode>
14.	    <!--ro, req, string, 详细错误码英文描述, desc:详细错误码的英文描述-->OK
15.	  </subStatusCode>
16.	</ResponseStatus>
```

- response body输出参数通用错误代码

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