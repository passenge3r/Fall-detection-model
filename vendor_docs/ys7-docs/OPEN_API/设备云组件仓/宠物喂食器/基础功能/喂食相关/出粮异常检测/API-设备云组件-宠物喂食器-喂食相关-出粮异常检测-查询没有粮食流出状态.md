# API-设备云组件-宠物喂食器-喂食相关-出粮异常检测-查询没有粮食流出状态

> 更新时间: 2026-06-30T11:52:39.000+08:00

> 文档ID: 1577 | 来源树: OPEN_API

---

## 查询没有粮食流出状态

- 接口功能

   属于自定义领域（global），查询没有粮食流出状态。展示上一次出粮时，设备是否真正出粮的状态。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NoFoodOutStatus`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NoFoodOutStatus' \
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
    "data": false
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
| data | Boolean | 没有粮食流出状态，true-没有粮食流出（状态异常），false-有粮食流出（状态正常） |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |