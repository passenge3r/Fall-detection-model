# index.md

> 更新时间: 2026-06-17T17:43:46.000+08:00

> 文档ID: 4030 | 来源树: OPEN_API

---

## 铃声预览 （ClockPlay）

- 接口功能

   铃声预览 （ClockPlay）

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/AlarmClock/ClockPlay`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| body | Content-Type | string |  | Y |
| header | accessToken | string | 用户访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| body | volume | integer | 闹钟音量 | Y |
| body | musicId | integer | 闹钟音乐ID, range:[0,1,2,3,4,5,6,7,8,9,10]. 0-老式闹钟1-敲打声2-小河流水3-钢琴4-吉他5-清新6-进取7-鸟叫8-经典闹钟9-小星星10-无铃声（缓慢灯光） | Y |
| body | action | integer | 闹钟预览操作. 1=播放，0=暂停 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/AlarmClock/ClockPlay' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Content-Type": "value",
    "volume": 0,
    "musicId": 0,
    "action": 0
}'
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
  },
  "data": 1066639013
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| meta | object | 服务响应信息 |
| meta.code | integer | 服务响应状态码。参见响应码解释。 |
| meta.message | string | 服务响应状态描述 |
| meta.moreInfo | object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | string | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | string | 设备响应状态描述 |
| data | integer | 业务参数，详细说明见下表 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 20007 | 设备不在线 |  |