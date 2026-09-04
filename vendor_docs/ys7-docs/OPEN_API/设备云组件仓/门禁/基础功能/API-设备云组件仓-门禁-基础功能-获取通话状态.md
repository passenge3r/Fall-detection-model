# API-设备云组件仓-门禁-基础功能-获取通话状态

> 更新时间: 2026-07-06T13:48:07.000+08:00

> 文档ID: 1126 | 来源树: OPEN_API

---

## 获取通话状态

- 接口功能

   获取通话状态，支持子账号的 Get 权限。本文档仅适用于设备型号 DS-K1T 系列的人脸门禁，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/acs/videoIntercom/callStatus`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/x-www-form-urlencoded | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| body | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/acs/videoIntercom/callStatus' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial='
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": {
        "CallStatus": {
            "status": "idle"
        }
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Object | 业务数据 |
| data.CallStatus | Object | 状态 |
| data.CallStatus.status | String | 状态，idle#空闲，ring#响铃，onCall#通话中 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |