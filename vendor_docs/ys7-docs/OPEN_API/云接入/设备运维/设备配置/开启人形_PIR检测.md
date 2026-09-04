# 开启人形/PIR检测

> 更新时间: 2026-06-30T12:11:07.000+08:00

> 文档ID: 1724 | 来源树: OPEN_API

---

## 开启人形/PIR检测

- 接口功能

   开启人形/PIR检测

- 请求地址

`https://open.ys7.com/api/v3/device/alarm/detect/switch/set`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| body | type | String | AI人形检测-1，PIR检测-5 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/alarm/detect/switch/set' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: K69690868' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'type=1'
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
| code | String | 业务码 |
| msg | String | 描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |