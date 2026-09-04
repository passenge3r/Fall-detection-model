# API-云直播-用量查询-流量查询-查询账户下流量消耗详情

> API-云直播-用量查询-流量查询-查询账户下流量消耗详情

> 更新时间: 2026-06-30T17:54:56.000+08:00

> 文档ID: 1425 | 来源树: OPEN_API

---

## 查询账户下流量消耗详情

- 接口功能

   该接口用于查询账户下流量消耗详情，默认只能查询前一天以前的数据，最多只能查询7天的流量数据。子账户token无权限请求。

- 请求地址

`https://open.ys7.com/api/lapp/traffic/user/detail`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | startTime | Long | 开始时间，时间格式为1457420564508，精确到毫秒，默认为当前日期往前推算1周。最多只能查询当前日期往前1周内的数据 | N |
| body | endTime | Long | 结束时间，时间格式为1457420564508，精确到毫秒，默认为当前日期往前推算1天。只能查询1天前的数据 | N |
| body | pageStart | Int | 分页起始页，从0开始，默认为0 | N |
| body | pageSize | Int | 分页大小，默认为10，最大为50 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/traffic/user/detail' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'startTime=1495209600000' \
--data-urlencode 'endTime=1494604800000' \
--data-urlencode 'pageStart=0' \
--data-urlencode 'pageSize=2'
```

- 返回数据

```
{
    "data": [
        {
            "flowDate": 1495209600000,
            "deviceCount": 1,
            "channelCount": 1,
            "hlsFlow": 11566,
            "appFlow": 5566,
            "rtmpFlow": 2234,
            "flowCount": 19366
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Array | 返回数据列表 |
| flowDate | Long | 日期，格式：long型时间戳 |
| deviceCount | Int | 当日消耗流量设备数 |
| channelCount | Int | 当日消耗流量通道数 |
| hlsFlow | Long | 轻应用HLS地址预览消耗，单位字节 |
| appFlow | Long | APP应用预览消耗，单位字节 |
| rtmpFlow | Long | 轻应用RTMP地址预览消耗，单位字节 |
| flowCount | Long | 流量消耗汇总，单位字节 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 10017 | appKey不存在 | 确认appKey是否正确 |
| 49999 | 数据异常 | 接口调用异常 |