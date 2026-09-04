# API-云接入-设备能力-客流统计-查询设备某一天每小时的客流数据

> 更新时间: 2026-07-09T13:39:45.000+08:00

> 文档ID: 691 | 来源树: OPEN_API

---

## 查询设备某一天每小时的客流数据

- 接口功能

   该接口用于查询设备某一天每小时的客流统计数据（接口需要设备支持客流统计功能） 子账户token请求所需最小权限："Permission":"Get" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/passengerflow/hourly`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 通道号 | Y |
| Body | date | Long | 时间戳日期，精确至毫秒，默认为今天 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/passengerflow/hourly' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'date=146744312353'
```

- 返回数据

```
{
    "data": [
        {
            "hourIndex": 0,
            "inFlow": 23,
            "outFlow": 32
        },
        {
            "hourIndex": 1,
            "inFlow": 12,
            "outFlow": 41
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Array<object> | 业务数据 |
| hourIndex | Int | 小时索引 |
| inFlow | Int | 进店流量 |
| outFlow | Int | 出店流量 |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持客流统计功能 |