# API-存储与媒体处理-云录制-视频采集与存储-加密录像日历查询

> 更新时间: 2026-06-25T14:29:29.000+08:00

> 文档ID: 2042 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-加密录像日历查询

- 接口功能

   加密录像日历查询。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/exist/month`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 通道号 | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | spaceId | String | 空间id,不填默认查询主空间下录像日历 | Y |
| query | month | String | 查询的月份，时间格式为：yyyyMM | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/exist/month?month=202510&spaceId=44028' \
--header 'deviceSerial: 553055114' \
--header 'accessToken: at.xxxxx' \
--header 'localIndex: 1'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        "2023-11-27",
        "2023-11-29",
        "2023-11-30"
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回信息 |
| -code | Int | 错误码 |
| -message | String | 错误信息 |
| data | Array<String> | 返回数据，存在录像的日期列表 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |