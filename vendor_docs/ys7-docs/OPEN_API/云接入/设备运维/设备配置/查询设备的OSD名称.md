# 查询设备的OSD名称

> 更新时间: 2026-06-30T12:11:01.000+08:00

> 文档ID: 1721 | 来源树: OPEN_API

---

## 查询设备的OSD名称

- 接口功能

   查询设备OSD名称

- 请求地址

`https://open.ys7.com/api/v3/device/osd`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/osd?deviceSerial=C57256745' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": {
        "osd": "1234"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 业务码 |
| msg | String | 描述 |
| data | Object | 返回数据 |
| data.osd | String | 设备OSD名称 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |