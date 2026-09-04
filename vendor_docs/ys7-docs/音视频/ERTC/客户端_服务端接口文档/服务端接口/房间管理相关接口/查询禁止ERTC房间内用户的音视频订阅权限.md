# 查询禁止ERTC房间内用户的音视频订阅权限

> 更新时间: 2026-06-23T16:53:56.000+08:00

> 文档ID: 3697 | 来源树: 音视频

---

## 查询禁止ERTC房间内用户的音视频订阅权限

- 接口功能

   功能描述：查询禁止ERTC房间内用户的音视频订阅权限  
是否支持托管：否  
是否支持子账号：否

- 请求地址

`https://open.ys7.com/api/service/rtc/conference/participant/subscription`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | appId | String | 应用ID | Y |
| body | roomId | String | 房间ID | Y |
| body | subscriber | String | 订阅人 | N |
| body | producer | String | 被订阅人 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/rtc/conference/participant/subscription' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'appId=' \
--data-urlencode 'roomId='
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "appId": "",
        "roomId": "",
        "subscribers": [],
        "producers": [],
        "audioStream": 0,
        "videoStream": 0,
        "screenStream": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| body | Object | 响应元信息 |
| meta | Object |  |
| code | String | 状态码 |
| message | String | 错误信息 |
| moreInfo | String | object |
| data | Object |  |
| appId | String | 应用ID |
| roomId | String | 会议ID |
| subscribers | Array | 订阅人ID列表 |
| producers | Array | 被订阅人ID列表 |
| audioStream | Int | 0: 未禁用；1：禁用 |
| videoStream | Int | 0: 未禁用；1：禁用 |
| screenStream | Int | 0: 未禁用；1：禁用 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 404 | 资源不存在 | 资源不存在 |
| 500 | 服务器异常 | 服务器异常 |
| 400 | 参数错误 | 参数错误 |