# API-设备云组件-宠物喂食器-夜间模式设置-查询夜间模式

> 更新时间: 2026-06-30T11:53:14.000+08:00

> 文档ID: 1584 | 来源树: OPEN_API

---

## 查询夜间模式

- 接口功能

   属于自定义领域（global），查询夜间模式。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NightMode`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/NightMode' \
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
        "Switch": false,
        "StartTimeInt": 0,
        "EndTimeInt": -3600
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
| data.Switch | Boolean | 开关，是否开启夜间模式，true-开启，false-关闭 |
| data.StartTimeInt | Int | 开始时间戳，夜间模式的开始时间，时间戳形式，仅读取时、分部分，例如39240为18:54 |
| data.EndTimeInt | Int | 结束时间戳，夜间模式结束时间，时间戳形式，仅读取时、分部分，结束时间早于开始时间则为下一天时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |