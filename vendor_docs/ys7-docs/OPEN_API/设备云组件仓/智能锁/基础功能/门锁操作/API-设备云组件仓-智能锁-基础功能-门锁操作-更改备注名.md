# API-设备云组件仓-智能锁-基础功能-门锁操作-更改备注名

> 更新时间: 2026-07-09T13:43:56.000+08:00

> 文档ID: 753 | 来源树: OPEN_API

---

## 更改备注名

- 接口功能

   更改备注名

- 请求地址

`https://open.ys7.com/api/lapp/keylock/user/modify/remark`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | lockUserIndex | String | 门锁用户id | Y |
| Body | remarkName | String | 备注名 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/user/modify/remark' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'lockUserIndex=2' \
--data-urlencode 'remarkName=name'
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