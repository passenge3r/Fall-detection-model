# API-设备云组件仓-智能锁-基础功能-门锁操作-添加临时密码

> 更新时间: 2026-07-09T13:45:06.000+08:00

> 文档ID: 767 | 来源树: OPEN_API

---

## 添加临时密码

- 接口功能

   添加临时密码

- 请求地址

`https://open.ys7.com/api/lapp/keylock/temporary/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | lockUserName | String | 用户名 | N |
| Body | beginTime | String | 开始时间（秒级时间戳），时间格式为1457420564，精确到秒 | N |
| Body | endTime | String | 结束时间（秒级时间戳），时间格式为1457420564，精确到秒 | N |
| Body | limitTime | String | 限制次数，-1不限制 | N |
| Body | deviceSerial | String | 设备序列号 | N |
| Body | accessToken | String | 访问令牌 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/temporary/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.0v38go2cdf814p7k3ne8xwvy2codwt1m-1ovws9vkav-18gf1pk-bnadjuikn' \
--data-urlencode 'deviceSerial=BG9859941' \
--data-urlencode 'lockUserName=123' \
--data-urlencode 'beginTime=1766651674' \
--data-urlencode 'endTime=1766655274' \
--data-urlencode 'limitTime=-1'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": {
        "index": "1",
        "pwd": "54020324"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 返回内容 |
| code | String | 返回响应码 |
| data | Object | 业务数据 |
| index | String | 临时密码编号 |
| pwd | String | 临时密码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |