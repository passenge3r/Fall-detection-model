# API-云接入-通用设备管理-设备确权-在线确权

> 更新时间: 2026-07-09T18:39:17.000+08:00

> 文档ID: 666 | 来源树: OPEN_API

---

## 在线确权

- 接口功能

   该接口用于在线确权。

- 请求地址

`https://open.ys7.com/api/userdevice/v3/devices/permission`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的access\_token | Y |
| Query | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/userdevice/v3/devices/permission?accessToken=xxxxx&deviceSerial=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "status": 1
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回元信息 |
| code | Int | 返回码 |
| message | String | 返回消息 |
| moreInfo | Object | 更多信息 |
| status | Int | 确权状态标识 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 确权成功 | 请求成功 |
| 401 | Unauthorized |  |
| 403 | Forbidden |  |
| 404 | Not Found |  |
| 504 | 网络异常 |  |
| 2009 | 超时 |  |
| 2021 | 确权失败 |  |
| 70000 | 确权失败 |  |