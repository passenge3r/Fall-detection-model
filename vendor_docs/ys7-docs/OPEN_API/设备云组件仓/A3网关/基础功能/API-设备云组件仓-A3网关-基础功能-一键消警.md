# API-设备云组件仓-A3网关-基础功能-一键消警

> 更新时间: 2026-07-06T17:45:35.000+08:00

> 文档ID: 875 | 来源树: OPEN_API

---

## 设备一键消警

- 接口功能

   该接口用于实现设备远程消除警报功能（需要设备支持远程一键消警功能）。子账户token请求所需最小权限：`无`。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/lapp/detector/cancelAlarm`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 网关设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/detector/cancelAlarm' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=465538888'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |

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
| 49999 | 数据异常 | 接口调用异常 |