# API-云接入-设备能力-客流统计-获取客流统计开关状态

> 更新时间: 2026-07-09T13:39:37.000+08:00

> 文档ID: 688 | 来源树: OPEN_API

---

## 获取客流统计开关状态

- 接口功能

   该接口用于获取客流统计开关状态（接口需要设备支持客流统计功能） 子账户token请求所需最小权限："Permission":"Get" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/lapp/passengerflow/switch/status`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/passengerflow/switch/status' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx'
```

- 返回数据

```
{
    "data": {
        "deviceSerial": "427734888",
        "channelNo": 0,
        "enable": 0
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 业务数据 |
| deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 |
| channelNo | Int | 通道号 |
| enable | Int | 状态：0-关闭，1-开启 |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持客流统计功能 |