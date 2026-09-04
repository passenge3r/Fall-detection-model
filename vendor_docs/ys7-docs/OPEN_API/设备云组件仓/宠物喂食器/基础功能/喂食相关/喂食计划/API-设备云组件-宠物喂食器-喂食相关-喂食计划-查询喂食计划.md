# API-设备云组件-宠物喂食器-喂食相关-喂食计划-查询喂食计划

> 更新时间: 2026-06-30T11:49:07.000+08:00

> 文档ID: 1565 | 来源树: OPEN_API

---

## 查询喂食计划

- 接口功能

   属于自定义领域（global），查询喂食计划。用于定时喂食，可设置循环计划也可设置单次计划，与手机闹钟功能相似。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/MealPlan`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/global/MealPlan' \
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
    "data": [
        "17f10480000global_ManualFeed_1",
        "11f18230000global_ManualFeed_6"
    ]
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
| data | Array | 喂食计划，取值范围[0,8]。格式说明：例如17f10480000global\_ManualFeed\_1。1.第一位字符(enable)：表示该条计划是否使能，0为禁用，计划为关闭状态；1为使能，计划为开启状态。2.第二至三位字符(weekdays)：表示周重复计划(二进制转化为十六进制数据)，按照每一位来代表日期，若全为0则代表单次模式只生效一次，否则为循环模式(第8位保留)，判断相应位是否置1，置1表示当天生效，例如1F->0x1F->01111111一周7天重复，0x12->00010010表示星期二和星期五执行。3.第四至七位字符(startTime)：表示动作执行时间，例如1200表示12:00时刻。4.第八至十一字符(sustain)：0000瞬时执行。5.第十二位字符起：表示执行动作，组装按固定格式global\_ManualFeed\_喂食份额，限制1-20(一份份额约等8-10g)。 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |