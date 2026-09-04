# API-设备云组件-宠物喂食器-喂食相关-下一餐喂食信息-查询下一餐信息

> 更新时间: 2026-06-30T11:49:09.000+08:00

> 文档ID: 1567 | 来源树: OPEN_API

---

## 查询下一餐信息

- 接口功能

   属于自定义领域（global），查询下一餐信息。喂食计划中，下一次出粮的时间。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NextMealInfo`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NextMealInfo' \
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
        "FeedTime": "18:23",
        "week": 5,
        "FeedSize": 6,
        "Enable": true,
        "Sequence": 1
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
| data.FeedTime | String | 喂食时间，动作执行时间，例如10:48，长度范围[1,5] |
| data.week | Int | 星期，星期几，取值范围[1,7] |
| data.FeedSize | Int | 喂食量，份额，一份份额约8-10g，取值范围[0,20] |
| data.Enable | Boolean | 有效，true-有效，false-无效 |
| data.Sequence | Int | 序号，取值范围[0,7] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |