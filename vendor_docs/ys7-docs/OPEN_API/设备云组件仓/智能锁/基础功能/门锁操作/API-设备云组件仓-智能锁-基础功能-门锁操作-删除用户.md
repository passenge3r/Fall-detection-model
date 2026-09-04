# API-设备云组件仓-智能锁-基础功能-门锁操作-删除用户

> 更新时间: 2026-07-09T13:45:11.000+08:00

> 文档ID: 770 | 来源树: OPEN_API

---

## 删除智能锁用户

- 接口功能

   删除智能锁用户

- 请求地址

`https://open.ys7.com/api/lapp/keylock/user/delete`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | lockUserIndex | String | 指纹锁用户ID | Y |
| Body | accessToken | String | 访问令牌 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/user/delete' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.0v38go2cdf814p7k3ne8xwvy2codwt1m-1ovws9vkav-18gf1pk-bnadjuikn' \
--data-urlencode 'deviceSerial=BG9859941' \
--data-urlencode 'lockUserIndex=2'
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
| msg | String | 返回内容 |
| code | String | 返回响应码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |