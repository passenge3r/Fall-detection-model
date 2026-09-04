# ERTC-voip相关-将设备踢出房间

> 更新时间: 2026-06-17T18:20:22.000+08:00

> 文档ID: 4300 | 来源树: 音视频

---

## ERTC-voip相关-将设备踢出房间

- 接口功能

   将设备踢出会议，是否支持托管：否，是否支持子账号：否

- 请求地址

`https://open.ys7.com/api/v3/rtc/device/kickout`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | appId | String | RTC应用Id | Y |
| body | strRoomId | String | 房间号 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | channelNo | String | 通道号 | Y |
| body | resourceToken | String | 资源token生成资源时，userId格式必须为："设备序列号\_通道号" | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/rtc/device/kickout' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'appId=' \
--data-urlencode 'strRoomId=' \
--data-urlencode 'deviceSerial=' \
--data-urlencode 'channelNo=' \
--data-urlencode 'resourceToken='
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": {}
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta |
| -code | Int | code |
| -message | String | message |
| -moreInfo | Object | moreInfo |
| data | Object | data |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 400 | 参数错误 |  |
| 412 | 前置条件不满足 |  |
| 50000 | 服务异常 |  |
| 403 | 用户无权限操作 |  |