# API-存储与媒体处理-云录制-视频采集与存储-删除一次性录制计划

> 更新时间: 2026-06-25T14:31:10.000+08:00

> 文档ID: 2049 | 来源树: 云存储

---

## 删除一次性录制计划

- 接口功能

   删除一次性录制计划。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | oneOffPlanId | Long | 单次计划ID | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'oneOffPlanId=5904'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回体 |
| meta.code | Int | 返回码 |
| meta.message | String | 返回信息 |
| meta.moreInfo | String | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码：200 |
| 500 | 服务器异常 | HTTP状态码：500 |
| 400 | 参数错误 | HTTP状态码：400 |
| 412 | 前置条件不满足 | HTTP状态码：412 |
| 406 | 平台不支持的操作 | HTTP状态码：406 |