# API-设备云组件仓-智能锁-基础功能-门锁操作-查询终端授权情况

> 更新时间: 2026-07-09T13:45:03.000+08:00

> 文档ID: 765 | 来源树: OPEN_API

---

## 查询终端授权情况

- 接口功能

   本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁。其余型号不保证可用。 注：如下接口调用，需要联系萤石配置白名单，否则接口可能调用报错

- 请求地址

`https://open.ys7.com/api/lapp/keylock/remote/authStatus`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 用户访问令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Query | endpointId | String | 开门终端 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/keylock/remote/authStatus' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=xxxxx' \
--data-urlencode 'deviceSerial=xxxxx'
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
| msg | String | 返回消息 |
| code | String | 返回码 |
| data | Object | 业务数据 |
| status | Int | 授权状态,1:授权中 0:未处于授权中的状态 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |