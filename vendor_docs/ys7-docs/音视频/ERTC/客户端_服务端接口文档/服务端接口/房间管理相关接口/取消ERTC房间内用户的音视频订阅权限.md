# 取消ERTC房间内用户的音视频订阅权限

> 更新时间: 2026-06-23T16:53:53.000+08:00

> 文档ID: 3696 | 来源树: 音视频

---

## 取消ERTC房间内用户的音视频订阅权限

- 接口功能

   功能描述：取消ERTC房间内用户的音视频订阅权限  
是否支持托管：否  
是否支持子账号：否

- 请求地址

`https://open.ys7.com/api/service/rtc/conference/participant/subscription/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | appId | String | 应用ID | Y |
| body | roomId | String | 会议房间ID | Y |
| body | subscribers | Array<String> | 订阅方 | Y |
| body | producers | Array<String> | 被订阅方 | Y |
| body | videoStream | Int | 0: 未禁用；1：禁用 | Y |
| body | audioStream | Int | 0: 未禁用；1：禁用 | Y |
| body | screenStream | Int | 0: 未禁用；1：禁用 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/rtc/conference/participant/subscription/update' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'appId=' \
--data-urlencode 'roomId=' \
--data-urlencode 'subscribers=' \
--data-urlencode 'producers=' \
--data-urlencode 'videoStream=' \
--data-urlencode 'audioStream=' \
--data-urlencode 'screenStream='
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应元信息 |
| code | String | 业务响应码 |
| message | String | 响应信息 |
| moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 404 | 资源不存在 | 资源不存在 |
| 500 | 服务器异常 | 服务器异常 |
| 400 | 参数错误 | 参数错误 |