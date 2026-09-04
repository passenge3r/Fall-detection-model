# API-智能门铃-基础功能-休眠状态-低功耗设备休眠状态设置

>  

> 更新时间: 2026-06-30T10:58:43.000+08:00

> 文档ID: 1529 | 来源树: OPEN_API

---

## 低功耗设备休眠状态设置

- 接口功能

   低功耗设备休眠状态设置。本文档仅适用于设备型号 CS-CP3，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/open/device/metadata/wakeup`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/open/device/metadata/wakeup' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G12345678'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 返回码 |
| meta.message | String | 返回消息 |
| meta.moreInfo | Object | 更多信息 |
| data | Object | 返回数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20007 | 设备不在线 | http状态码412 |
| 20018 | 该用户不拥有该设备 | http状态码403 |