# API-存储与媒体处理-云录制-视频采集与存储-终止一次性录制计划

> 更新时间: 2026-06-25T14:30:53.000+08:00

> 文档ID: 2046 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-终止一次性录制计划

- 接口功能

   终止一次性录制计划。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/stop`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | oneOffPlanId | Long | 一次性计划ID | Y |
| body | onlyStopPreview | Boolean | 是否仅停止预览，默认false | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/stop' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'oneOffPlanId=589880' \
--data-urlencode 'onlyStopPreview=true'
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
| meta | Object | 返回体 |
| -code | Int | 返回码 |
| -message | String | 返回信息 |
| -moreInfo | String | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 资源不存在 |
| 500 | 服务器异常 | 服务器内部异常 |
| 400 | 参数错误 | 请求参数错误 |
| 412 | 前置条件不满足 | 前置条件不满足 |