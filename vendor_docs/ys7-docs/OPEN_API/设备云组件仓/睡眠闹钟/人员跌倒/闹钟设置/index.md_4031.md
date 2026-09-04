# index.md

> 更新时间: 2026-06-17T17:43:54.000+08:00

> 文档ID: 4031 | 来源树: OPEN_API

---

## 闹钟修改 （ClockModify）

- 接口功能

   闹钟修改 （ClockModify）

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/AlarmClock/ClockModify`

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
| body | data | array | 闹钟设置, range:[0,] | Y |
| body | ClockMode | array | 重复形式, range:[0,] | Y |
| body | ClockStatus | boolean | 闹钟开关 | Y |
| body | UpdateTime | number | 更新时间 | Y |
| body | ClockVolume | integer | 闹钟音量 | Y |
| body | RepeatType | integer | ClockModify, range:[0,1]. 0-仅一次1-重复，具体见ClockMode | Y |
| body | ClockMusic | integer | 闹钟音乐, range:[0,1,2,3,4,5,6,7,8,9,10]. 0-老式闹钟1-敲打声2-小河流水3-钢琴4-吉他5-清新6-进取7-鸟叫8-经典闹钟9-小星星10-无铃声（缓慢灯光） | Y |
| body | ClockTime | string | 闹钟时间, range:[1,] | Y |
| body | ClockName | string | 闹钟名称, range:[1,] | Y |
| body | LastTime | integer | 响铃时长, range:[0,1,2]. 0-1分钟1-5分钟2-10分钟 | Y |
| body | ClockID | integer | 闹钟ID | Y |
| body | ModifyMode | integer | 修改类型, range:[0,1,2]. 0-删除1-增加2-修改 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/AlarmClock/ClockModify' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Content-Type": "value",
    "data": [],
    "ClockMode": [],
    "ClockStatus": true,
    "UpdateTime": "value",
    "ClockVolume": 0,
    "RepeatType": 0,
    "ClockMusic": 0,
    "ClockTime": "value",
    "ClockName": "value",
    "LastTime": 0,
    "ClockID": 0,
    "ModifyMode": 0
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
  "data": null
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
| data | -- | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 20007 | 设备不在线 |  |