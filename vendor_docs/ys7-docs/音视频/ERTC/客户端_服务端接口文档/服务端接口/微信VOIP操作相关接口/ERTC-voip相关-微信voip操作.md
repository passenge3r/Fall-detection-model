# ERTC-voip相关-微信voip操作

> 更新时间: 2026-06-17T18:20:16.000+08:00

> 文档ID: 4298 | 来源树: 音视频

---

## ERTC-voip相关-微信voip操作

- 接口功能

   微信小程序开始通话或取消通话，是否支持托管，是否支持子账号：否

- 请求地址

`https://open.ys7.com/api/service/rtc/voip/trigger`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | requestId | String | 取消通话时必填，需填开始通话时接口返回的requestId | Y |
| body | cmdType | Int | 0 开始通话 1 取消通话（默认为0）2拒接通话 | N |
| body | wxAppId | String | 微信应用Id | Y |
| body | wxRoomId | String | 微信房间号 | Y |
| body | openId | String | 微信openId | Y |
| body | sessionKey | String | 微信SessionKey | Y |
| body | serverToken | String | 微信token | Y |
| body | resourceToken | String | 资源token，包含房间信息，appId等信息，生成资源token时customId必须为openId | Y |
| body | appId | String | ERTC 应用Id | Y |
| body | strRoomId | String | ERTC 房间号 | Y |
| body | wechatVideoStatus | Int | 0:不发送，不接收、1:不发送，接收、2:发送，不接收、3:发送，接收，目前只支持1和3。1是微信上有画面，设备没画面；3是设备和微信都有画面 | Y |
| body | encodeType | String | 目前仅支持h264和h265 | Y |
| body | wechatVideoPlayRotationDegree | Int | 建议填写0，默认0，标准的旋转的角度只有四挡：0、90、180和270 | N |
| body | encodeVideoFixedLength | Int | 目前支持640和320，默认640 | N |
| body | encodeVideoRotation | Int | 收到的流的方向，默认-1,1: 0度流，需要配合小程序端的0度流参数，两者一致后才能收到0度流;其它：旋转流，默认也是旋转流 | N |
| body | encodeVideoRatio | Int | 收到的流的比例，默认-1；75: 宽/高\*100=75, 例如240x320；133: 宽/高\*100=133, 例如320x240；50: 宽/高\*100=50, 例如160x320；200: 宽/高\*100=200, 例如320x160 | N |
| body | account | String | 设备联系人account | Y |
| body | deviceId | String | 设备序列号（cmdType=2时必填） | N |
| body | modelId | String | 设备modelId（cmdType=2时必填） | N |
| body | payload | String | 小程序呼叫payload（cmdType=2时必填） | N |
| body | hangupReason | String | 拒接类型 9 繁忙 10 响铃超时 11 拒接（cmdType=2时必填） | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/rtc/voip/trigger' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'requestId=' \
--data-urlencode 'cmdType=' \
--data-urlencode 'wxAppId=' \
--data-urlencode 'wxRoomId=' \
--data-urlencode 'openId=' \
--data-urlencode 'sessionKey=' \
--data-urlencode 'serverToken=' \
--data-urlencode 'resourceToken=' \
--data-urlencode 'appId=' \
--data-urlencode 'strRoomId=' \
--data-urlencode 'wechatVideoStatus=' \
--data-urlencode 'encodeType=' \
--data-urlencode 'account='
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": {}
    },
    "data": {
        "requestId": "fe08a03789134c5eaad643a0c6baa589"
    }
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
| -requestId | String | requestId |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 500 | 服务器异常 |  |
| 400 | 参数错误 |  |
| 412 | 前置条件不满足 |  |