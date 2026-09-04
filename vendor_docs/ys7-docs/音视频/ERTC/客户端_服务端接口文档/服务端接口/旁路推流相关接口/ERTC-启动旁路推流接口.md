# ERTC-启动旁路推流接口

> 更新时间: 2026-06-24T16:01:23.000+08:00

> 文档ID: 2110 | 来源树: 音视频

---

## ERTC-启动旁路推流接口

- 接口功能

   功能描述：开发者用户启动直播。

   是否支持托管：否

   是否支持子帐号：否

- 请求地址

`https://open.ys7.com/api/service/rtc/live/start`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | appId | String | 应用ID | Y |
| body | livePushUrl | String | 直播推流地址 | Y |
| body | roomId | String | 会议房间ID | Y |
| body | liveConfig | String | 直播画面配置，json格式的字符串 | Y |
| body | watermarkConfig | String | 文字水印标签配置，json格式的字符串 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/rtc/live/start' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'appId=xxxxx' \
--data-urlencode 'livePushUrl=xxxxx' \
--data-urlencode 'roomId=xxxxx' \
--data-urlencode 'liveConfig=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 0,
        "message": "string"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 请求处理结果 |
| -code | Int | 状态码 |
| -message | String | 成功/错误信息 |
| data | Object | 返回数据 |
| -requestId | String | 作为该直播的ID，后续修改或停止直播时，需要传入 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码:200 |
| 10002 | accessToken过期或异常 | HTTP状态码:401 |
| 404 | 资源不存在 | HTTP状态码:404 |
| 500 | 服务器异常 | HTTP状态码:500 |
| 400 | 参数错误 | HTTP状态码:400 |
| 429 | 请求过于频繁 | HTTP状态码:429 |
| 40002 | 操作缓存异常,请稍后重试 | HTTP状态码:503 |