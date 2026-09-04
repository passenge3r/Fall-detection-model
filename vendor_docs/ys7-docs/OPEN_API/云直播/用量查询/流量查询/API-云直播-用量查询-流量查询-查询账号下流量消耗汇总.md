# API-云直播-用量查询-流量查询-查询账号下流量消耗汇总

> API-云直播-用量查询-流量查询-查询账号下流量消耗汇总

> 更新时间: 2026-06-30T17:54:54.000+08:00

> 文档ID: 1424 | 来源树: OPEN_API

---

## 查询账号下流量消耗汇总

- 接口功能

   该接口用于查询账号下流量消耗汇总。子账户token无权限请求。

- 请求地址

`https://open.ys7.com/api/lapp/traffic/user/total`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/traffic/user/total' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功",
    "data": {
        "totalFlow": 16565165,
        "usedFlow": 14523,
        "averageConsume": 200
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| totalFlow | Long | 拥有的总流量，单位字节（企业版被赋予带宽能力，不计算该流量） |
| usedFlow | Long | 已使用的流量，单位字节 |
| averageConsume | Long | 日平均消耗，单位字节/天 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 10017 | appKey不存在 | 确认appKey是否正确 |
| 49999 | 数据异常 | 接口调用异常 |