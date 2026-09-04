# API-设备云组件仓-智能锁-基础功能-图像补光-设置日夜切换

> 更新时间: 2026-07-06T17:44:08.000+08:00

> 文档ID: 839 | 来源树: OPEN_API

---

## 设置日夜切换

- 接口功能

   该接口用于设置日夜切换。本文档仅适用于设备型号 CS-DL30-V100、CS-Y3000F-V100，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/ImageSupplement/DayNightGate`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | brightnessThrelD | Integer | 亮度门限，取值范围[0,100] | Y |
| Body | NightModeCtrl.nightModeCtrlMode | String | 日夜切换模式，取值范围[manual,time,auto]：manual-手动切换，time-分时切换，auto-自动切换 | N |
| Body | NightModeCtrl.ManualMode.manualModeVal | String | 手动切换方式，取值范围[day,night]：day-白天，night-晚上 | N |
| Body | NightModeCtrl.TimeMode.SwitchList | Array | 时间计划列表，取值范围[0,16] | N |
| Body | NightModeCtrl.TimeMode.SwitchList[].startTime | String | 开始时间 | Y |
| Body | NightModeCtrl.TimeMode.SwitchList[].endTime | String | 结束时间 | Y |
| Body | NightModeCtrl.AutoMode.autoSwtichThresholdVal | Integer | 切换阈值，取值范围[0,100] | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/ImageSupplement/DayNightGate' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "NightModeCtrl": {
        "nightModeCtrlMode": "manual",
        "ManualMode": {
            "manualModeVal": "day"
        },
        "TimeMode": {
            "SwitchList": [[{"startTime": "", "endTime": ""}]]
        },
        "AutoMode": {
            "autoSwtichThresholdVal": 0
        }
    },
    "brightnessThrelD": 0
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
| 200 | 成功 | 请求成功 |