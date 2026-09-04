# API-设备云组件仓-智能锁-基础功能-门锁操作-远程开锁功能开关设置

> 更新时间: 2026-07-09T13:44:52.000+08:00

> 文档ID: 759 | 来源树: OPEN_API

---

## 远程开锁功能开关设置

- 接口功能

   远程开锁功能开关设置。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/remote/config`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | enable | String | 功能开关：0-关，1-开 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/remote/config' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'enable=xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 响应提示信息 |
| code | String | 响应code |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |