# API-存储与媒体处理-云存储-获取设备云存储信息

> API-存储与媒体处理-云存储-获取设备云存储信息

> 更新时间: 2026-06-30T17:54:40.000+08:00

> 文档ID: 1409 | 来源树: 云存储

---

## 获取设备云存储信息

- 接口功能

   该接口用于查询设备云存储相关信息（该接口不支持NVR）。子账户token请求所需最小权限：Permission:Get Resource:Cam:序列号:通道号。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/device/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 开通云存储用户的设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | phone | String | 开通云存储用户的手机号，非必选参数 | N |
| body | channelNo | Int | 非必选参数，不为空表示查询指定通道云存储信息，为空表示查询设备本身云存储信息，默认是1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/device/info' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510666' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'phone=18888888888'
```

- 返回数据

```
{
    "data": {
        "userName": "ezviz",
        "deviceSerial": "596510666",
        "channelNo": 1,
        "totalDays": 7,
        "status": 1,
        "validDays": 280,
        "startTime": 1470370451000,
        "expireTime": 1603107852000,
        "serviceDetail": {
            "userName": "ezviz",
            "deviceSerial": "596510666",
            "channelNo": 1,
            "totalDays": 30,
            "startTime": 1539949152000,
            "expireTime": 1603107852000,
            "status": 0
        }
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| userName | String | 云存储服务所属用户的用户名 |
| deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 |
| channelNo | Int | 通道号 |
| totalDays | Int | 云存储服务录像覆盖周期 |
| status | Int | 云存储状态，-2:设备不支持，-1:未开通云存储，0:未激活，1:激活，2:过期 |
| validDays | Int | 可用天数 |
| startTime | Long | 云存储服务开始时间，精确到秒 |
| expireTime | Long | 云存储服务结束时间，精确到秒 |
| serviceDetail | Object | 不同类型云存储服务信息，只有当设备存在两种类型云存储服务才会有此对象 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | phone对应用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 未知错误 | 设备返回其他错误码或操作异常 |