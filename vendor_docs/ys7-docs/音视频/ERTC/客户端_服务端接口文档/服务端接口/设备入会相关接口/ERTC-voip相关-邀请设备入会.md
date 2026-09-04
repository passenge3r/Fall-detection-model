# ERTC-voip相关-邀请设备入会

> 更新时间: 2026-06-23T16:32:18.000+08:00

> 文档ID: 4297 | 来源树: 音视频

---

## ERTC-voip相关-邀请设备入会

- 接口功能

   邀请设备入会，是否支持托管：否，是否支持子账号：否

- 请求地址

`https://open.ys7.com/api/v3/rtc/device/join`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | appId | String | ERTC 应用Id | Y |
| body | strRoomId | String | 房间号 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | channelNo | String | 设备通道号 | Y |
| body | resourceToken | String | 资源token生成资源token时，userId格式必须为："设备序列号\_通道号" | Y |
| body | mode | Int | 1-双向音视频模式（默认），2-对讲模式，默认为1 | N |
| body | streamType | Int | 1-主码流，2-子码流。默认为1 | N |
| body | maxActiveSeconds | Int | 单位(秒)：超过此时间或触发SDGW其它主动退出策略时，设备自动退出房间，不传或-1表示不设置 | N |
| body | devVerifyCode | String | 视频加密密码(加密设备需要传递，否则可能黑屏) | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/rtc/device/join' \
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
| 500 | 服务器异常 |  |
| 400 | 参数错误 |  |
| 412 | 前置条件不满足 |  |
| 50000 | 服务异常 |  |
| 403 | 用户无权限操作 |  |