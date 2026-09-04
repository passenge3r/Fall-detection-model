# API-存储与媒体处理-云录制-视频采集与存储-查询加密录制项目信息

> 更新时间: 2026-06-25T14:29:11.000+08:00

> 文档ID: 2039 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-查询加密录制项目信息

- 接口功能

   查询加密录制项目信息。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/space`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | spaceId | String | 录像空间id | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/space?spaceId=44028' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": ""
    },
    "data": {
        "spaceId": 3,
        "totalSize": 0,
        "totalTimePlan": 0,
        "totalEventPlan": 0,
        "spaceName": "dsfasdfasd",
        "storageType": 1,
        "expireDays": 0,
        "primarySpace": false
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 错误信息 |
| -code | Int | 错误码 |
| -message | String | 错误信息 |
| -moreInfo | String | 更多信息 |
| data | Object | 数据 |
| -spaceId | Int | 录像空间ID |
| -totalSize | Int | 空间总大小 |
| -totalTimePlan | Int | 时间计划数量 |
| -totalEventPlan | Int | 时间计划数量 |
| -spaceName | String | 空间名称 |
| -storageType | Int | 存储类型 1: 标准存储 |
| -expireDays | Int | 生命周期 0为永久 |
| -primarySpace | Boolean | 是否为主空间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 资源不存在 |
| 500 | 服务器异常 | 服务器内部异常 |
| 400 | 参数错误 | 请求参数错误 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |