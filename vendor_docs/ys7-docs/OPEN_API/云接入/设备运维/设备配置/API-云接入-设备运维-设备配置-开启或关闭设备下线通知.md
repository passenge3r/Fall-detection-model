# API-云接入-设备运维-设备配置-开启或关闭设备下线通知

> 更新时间: 2026-07-09T13:40:24.000+08:00

> 文档ID: 719 | 来源树: OPEN_API

---

## 开启或关闭设备下线通知

- 接口功能

   开启或关闭设备下线通知

- 请求地址

`https://open.ys7.com/api/lapp/device/notify/switch`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 访问令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | enable | String | 状态：0-关闭，1-开启 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/notify/switch' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'enable=0'
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
| 10001 | 无效参数 |  |