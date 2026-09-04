# API-设备云组件-安全帽-配置设备工作状态上报参数

> API-设备云组件-安全帽-配置设备工作状态上报参数

> 更新时间: 2026-05-25T16:38:51.000+08:00

> 文档ID: 1486 | 来源树: OPEN_API

---

## 配置设备工作状态上报参数

接口分类：ISAPI能力

- URL

https://open.ys7.com/api/hikvision/ISAPI/System/localButtonPermission?format=json

- 接口描述

配置设备工作状态上报参数。其中，针对安全帽相机（DS-MCH208），仅支持定时上报。

- method

PUT

- header 请求头

| 参数名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| EZO-AccessToken | String | 授权过程获取的access\_token | Y |
| EZO-DeviceSeria | l String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| EZO-Date | String | 当前时间，示例：2017-12-01 10:00:00 | N |
| Content-Type | String | ISAPI 请求Body的内容类型，例如：application/xml ,如果信令为json格式,请填入application/json | N |

- Request Body请求参数（json）

```
1.	{
2.	 "Timing": { 
3.	 /*opt, object, 定时上报参数, desc:statusUploadMode==timing时必填*/
4.	  "interval":  300 
5.	  /*opt, int, 上报间隔（秒）, range:[0,600], unit:秒, desc:设备间隔多久上报一次状态信息*/
6.	 }
7.	}
```

- Response Body输出参数（json）

```
1.	{
2.	 "statusCode":  1, 
3.	 /*ro, opt, int, 状态码, desc:无法用1表示时（1表示成功且无特殊状态）必须返回*/
4.	 "statusString":  "ok", 
5.	 /*ro, opt, string, 状态描述, range:[1,64], desc:无法用ok表示时（ok表示成功且无特殊状态）必须返回*/
6.	 "subStatusCode":  "ok", 
7.	 /*ro, opt, string, 子状态码, range:[1,64], desc:无法用ok表示（ok表示成功且无特殊状态）必须返回*/
8.	 "errorCode":  1, 
9.	 /*ro, opt, int, 错误码, desc:当statusCode不为1时，与subStatusCode对应*/
10.	 "errorMsg":  "ok" 
11.	 /*ro, opt, string, 错误信息, desc:当statusCode不为1时，必须返回,解释信息在协议约束中，允许设备在后续的版本迭代中，进行优化丰富提升（不限制死）*/
12.	}
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