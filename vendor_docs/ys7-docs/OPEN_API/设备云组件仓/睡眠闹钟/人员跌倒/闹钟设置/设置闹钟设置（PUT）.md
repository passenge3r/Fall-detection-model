# 设置闹钟设置（PUT）

> 更新时间: 2026-06-22T10:28:23.000+08:00

> 文档ID: 4026 | 来源树: OPEN_API

---

## 设置闹钟设置

- 接口功能

    设置闹钟设置

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/AlarmClock/ClockSetting`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Array | 闹钟设置 范围：[0,] | Y |
| body | r | Int | RepeatType 0-仅一次 1-重复，具体见ClockMode  范围：[0,1] | N |
| body | s | Boolean | ClockStatus | N |
| body | t | String | ClockTime 范围：[1,] | N |
| body | v | Int | ClockVolume | N |
| body | lt | Int | LastTime 0-1分钟 1-5分钟 2-10分钟  范围：[0,1,2] | N |
| body | mus | Int | ClockMusic 0-老式闹钟 1-敲打声 2-小河流水 3-钢琴 4-吉他 5-清新 6-进取 7-鸟叫 8-经典闹钟 9-小星星 10-无铃声（缓慢灯光）  范围：[0,1,2,3,4,5,6,7,8,9,10] | N |
| body | id | Int | ClockID | N |
| body | n | String | ClockName 范围：[1,] | N |
| body | ut | Number | UpdateTime | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/AlarmClock/ClockSetting' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '[\n\t[\n\t\t{\n\t\t\t"r":412822283,\n\t\t\t"s":true,\n\t\t\t"t":"",\n\t\t\t"v":1169825258,\n\t\t\t"lt":1406336776,\n\t\t\t"mus":1493216266,\n\t\t\t"id":2139839645,\n\t\t\t"n":"",\n\t\t\t"ut":6.39128732E8\n\t\t}\n\t]\n]'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "成功",
    "moreInfo": {
      "deviceMeta": {
        "code": "0x00000000",
        "errorMsg": "Succeeded."
      }
    }
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |