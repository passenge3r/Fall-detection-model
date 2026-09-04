# API-存储与媒体处理-云存储-同一个账号下设备间云存储转移

> API-存储与媒体处理-云存储-同一个账号下设备间云存储转移

> 更新时间: 2026-06-30T17:54:37.000+08:00

> 文档ID: 1407 | 来源树: 云存储

---

## 同一个账号下设备间云存储转移

- 接口功能

   该接口用于云存储在同一个账号下两个设备之间转移。

   注1：云存储转移针对设备下所有云存储，无法进行单个云存储服务的转移。云存储转出条件：设备中存在可用的云存储，且云存储没有在使用（即 1:设备存在云存储 2:云存储停用或设备不在线）；云存储转入条件：设备在线，且没有可用的云存储（即设备云存储全部过期，或未使用过云存储）。注2：设备云存储转移后默认为停用状态，但是状态显示可能不正确，建议用户启用停用一次。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/trans`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | fromDeviceSerial | String | 云存储转出设备的设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | fromChannelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |
| body | toDeviceSerial | String | 云存储转入设备的设备序列号 | Y |
| body | toChannelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |
| body | requestId | String | 请求ID，建议UUID，注:相同的请求ID会被认为是同一个请求 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/trans' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'fromDeviceSerial=LL0000001' \
--data-urlencode 'fromChannelNo=1' \
--data-urlencode 'toDeviceSerial=686220334' \
--data-urlencode 'toChannelNo=1' \
--data-urlencode 'requestId=123465'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 10013 | 非开发者账户无权限调用 |  |
| 10054 | 云存储操作异常 |  |
| 10056 | 设备不支持云存储服务转出 | 当前设备无云存储服务 或 当前设备在线且云存储服务为启用状态 |
| 10057 | 设备不支持云存储服务转入 | 云存储转入设备不在线 或 转入设备中存在可用的云存储 |
| 10058 | 两台设备间云存储不支持转移 |  |
| 10059 | requestId已存在 |  |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 |  |
| 20007 | 设备不在线 |  |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |