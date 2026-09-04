# API-设备云组件仓-T3C智能按钮-基础功能-声音设置-设置告警声音使能开关

> 更新时间: 2026-07-06T13:41:01.000+08:00

> 文档ID: 967 | 来源树: OPEN_API

---

## 设置告警声音使能开关

- 接口功能

   该接口用于设置告警声音使能开关。本文档仅适用于设备型号 CS-T3C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/SoundSetting/AlarmSoundEnabled`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | voiceIndex | Integer | 自定义语音的索引 | N |
| Body | enabled | Boolean | 声音开关 | Y |
| Body | soundType | Integer | 声音类型，取值范围[0,1,2,3]：0-短叫，1-长叫，2-静音，3-自定义语音 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/SoundSetting/AlarmSoundEnabled' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "voiceIndex": 986514344,
    "enabled": true,
    "soundType": 108951160
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