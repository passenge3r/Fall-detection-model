# API-设备云组件-宠物喂食器-喂食相关-下一餐喂食信息-查询取消下一餐

> 更新时间: 2026-06-30T11:49:12.000+08:00

> 文档ID: 1568 | 来源树: OPEN_API

---

## 查询取消下一餐

- 接口功能

   属于自定义领域（global），查询取消下一餐。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/CancelNextMeal`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/CancelNextMeal' \
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
    "data": true
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
| data | Boolean | 取消下一餐，下次喂食计划是否会进行发放。false-确定取消，下一餐的喂食计划将被取消；true-确定不取消，下一餐的喂食计划将正常进行 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |