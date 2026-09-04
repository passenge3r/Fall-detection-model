# API-云接入-设备能力-客流统计-查询设备某一天的统计客流数据

> 用于查询设备某一天的客流统计数据

> 更新时间: 2026-07-09T13:39:40.000+08:00

> 文档ID: 690 | 来源树: OPEN_API

---

- 接口功能

该接口用于查询设备某一天的客流统计数据（接口需要设备支持客流统计能力集 `support_flow_statistics`）注意：当天的数据会在第二天凌晨2点左右更新，获取前一天的数据只能在第二天的2点之后才能获取到。子账户token请求所需最小权限："Permission":"Get" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/passengerflow/daily`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的 access\_token | Y |
| Body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 通道号 | Y |
| Body | date | Long | 时间戳日期，精确至毫秒，默认为今天，date 参数只能是 0 时 0 分 0 秒（如 1561046400000 可以，1561050000000 不行） | N |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/passengerflow/daily' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.9mqitppidgce4y8n54ranvyqc9fjtsrl' \
--data-urlencode 'deviceSerial=596510666' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'date=1561046400000'
```

- 返回数据

```
{
  "data": {
    "inFlow": 1000,
    "outFlow": 1000
  },
  "code": "200",
  "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| inFlow | Int | 进店流量 |
| outFlow | Int | 出店流量 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken 异常或过期 | 重新获取 accessToken |
| 10005 | appKey 异常 | appKey 被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial 不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持客流统计功能 |