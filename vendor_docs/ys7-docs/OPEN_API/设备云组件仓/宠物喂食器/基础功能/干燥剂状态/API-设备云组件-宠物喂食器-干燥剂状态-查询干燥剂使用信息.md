# API-设备云组件-宠物喂食器-干燥剂状态-查询干燥剂使用信息

> 更新时间: 2026-06-30T11:53:18.000+08:00

> 文档ID: 1586 | 来源树: OPEN_API

---

## 查询干燥剂使用信息

- 接口功能

   属于自定义领域（global），查询干燥剂使用信息。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/Desiccant`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/Desiccant' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "StartDate": "2022-12-01",
        "RemainingDays": 25
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数 |
| data.StartDate | String | 开始日期，开始使用的时间，例如2022-12-01，长度范围[1,12] |
| data.RemainingDays | Int | 剩余天数，剩余可使用天数，取值范围[0,30] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |