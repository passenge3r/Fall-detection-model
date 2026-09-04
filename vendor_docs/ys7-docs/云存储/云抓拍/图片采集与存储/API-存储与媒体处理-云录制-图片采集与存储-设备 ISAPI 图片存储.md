# API-存储与媒体处理-云录制-图片采集与存储-设备 ISAPI 图片存储

> 更新时间: 2026-06-30T17:52:34.000+08:00

> 文档ID: 1385 | 来源树: 云存储

---

## 设备ISAPI图片存储

- 接口功能

   给智能设备（主要为海康智能设备）下发ISAPI智能消息订阅，订阅后设备将主动上报智能消息。注意：调用该接口前，需要确保设备在线。

- 请求地址

`https://open.ys7.com/api/open/cloud/ISAPI/Event/notification/subscribeEvent`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | method | String | 下发ISAPI指令方法，POST/PUT，优先POST | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/ISAPI/Event/notification/subscribeEvent' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=G12262381' \
--data-urlencode 'method=POST'
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
| meta | Object | 返回状态码及信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |

**补充说明：调用成功/失败判断**

   1. 调用失败：当响应参数data里出现methodNotAllowed，则说明调用失败（如下图），需要在请求参数method字段更换参数。

![调用失败示例](https://resource.eziot.com/group2/M00/00/9A/CtwQF2RmAKSAO-5CAAHEzzjnugU535.png)

   2. 调用成功：当响应参数data里出现<statusString>OK，或者出现SubscribeEventResponse，则说明调用成功（如下图）。

![调用成功示例1](https://resource.eziot.com/group2/M00/00/9A/CtwQF2RmAUGAQjixAACo3A2KQhY269.png)

![调用成功示例2](https://resource.eziot.com/group2/M00/00/9A/CtwQFmRmAKeAHKYtAAMqohwT6iA651.png)