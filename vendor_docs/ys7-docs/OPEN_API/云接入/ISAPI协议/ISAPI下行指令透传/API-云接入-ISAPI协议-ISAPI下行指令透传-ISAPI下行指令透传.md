# API-云接入-ISAPI协议-ISAPI下行指令透传-ISAPI下行指令透传

> API-云接入-ISAPI协议-ISAPI下行指令透传-ISAPI下行指令透传

> 更新时间: 2026-05-25T16:38:17.000+08:00

> 文档ID: 694 | 来源树: OPEN_API

---

# ISAPI下行指令透传

本节包含isapi下行透传接口,该接口主要是用于透传控制海康品牌设备,如下为isapi协议的一个抽象示例.

## 端 / 平台 ->设备

- 接口功能：

  该接口用于从端或平台下发送ISAPI协议请求到设备,该接口支持json和XML形式的信令透传
- 请求地址

  `https://open.ys7.com/api/hikvision/{isapi协议上的 请求路径}`
- 请求方式

  根据协议选择,例如GET、PUT、POST
- 请求参数

`Resquest Header 部分`

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| EZO-AccessToken | String | 授权过程获取的access\_token | Y |
| EZO-DeviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| EZO-Date | String | 当前时间，示例：2017-12-01 10:00:00 | Y |
| Content-Type | String | ISAPI 请求Body的内容类型，例如：application/xml ,如果信令为json格式,请填入application/json | Y |

`Resquest Body 部分,示例如下:`

XML:

```
<?xml version="1.0" encoding="UTF-8"?>
<NTPServer version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>1</id>
    <addressingFormatType>ipaddress</addressingFormatType>
    <ipAddress>10.10.10.10</ipAddress>
    <portNo>123</portNo>
    <synchronizeInterval>1</synchronizeInterval>
</NTPServer>
```

JSON:

```
{
  "Zone":{
    "id":1,
    "zoneName":"test",
    "zoneType":"Instant",
    "delayTime":1,
    "stayAwayEnabled":true,
    "chimeEnabled":true,
    "silentEnabled":true,
    "timeOut":true,
    "detectorSeqCfg":"mod",
    "detectorSeq":"123456789"
  }
}
```

- HTTP请求报文

```
PUT /api/hikvision/ISAPI/System/time/ntpServers/1 HTTP/1.1
Host: open.ys7.com
EZO-AccessToken: at.2eafygyuabvmptnbak3ctbiq03eotm8x-6pkihc3byk-1w21rv5-dhjflmofu
EZO-DeviceSerial: 519928976
EZO-Date: 2017-12-01 10:00:00
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<NTPServer version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>1</id>
    <addressingFormatType>ipaddress</addressingFormatType>
    <ipAddress>10.10.10.10</ipAddress>
    <portNo>123</portNo>
    <synchronizeInterval>1</synchronizeInterval>
</NTPServer>
```

- 返回数据

`Response Header部分`

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| EZO-Code | String | 返回码 | Y |
| EZO-Message | String | 返回信息 | Y |

`Response Body部分,示例如下:`

XML:

```
  <?xml version="1.0" encoding="UTF-8"?>
  <NTPServer version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
      <id>1</id>
      <addressingFormatType>ipaddress</addressingFormatType>
      <ipAddress>10.10.10.10</ipAddress>
      <portNo>123</portNo>
      <synchronizeInterval>1</synchronizeInterval>
  </NTPServer>
```

JSON:

```
{
    "Zone": {
        "id": 1,
        "zoneName": "test",
        "zoneType": "Instant",
        "delayTime": 1,
        "stayAwayEnabled": true,
        "chimeEnabled": true,
        "silentEnabled": true,
        "timeOut": true,
        "detectorSeqCfg": "mod",
        "detectorSeq": "123456789"
    }
}
```

- 返回码

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