# API-设备云组件仓-T2C智能门窗传感器-基础功能-声音设置-播放指定声音

> 更新时间: 2026-07-06T13:40:21.000+08:00

> 文档ID: 950 | 来源树: OPEN_API

---

## 播放指定声音

- 接口功能

   该接口用于播放指定声音。本文档仅适用于设备型号 CS-T2C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/SoundSetting/PlaySpecificSound`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | volume | Integer | 音量，取值范围[0,100] | Y |
| Body | playSoundType | String | 声音类型，取值范围[alarm,call]：alarm-告警音，call-呼叫音 | N |
| Body | index | Integer | 声音索引，取值范围[0,65535] | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/SoundSetting/PlaySpecificSound' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "volume": 0,
    "playSoundType": "alarm",
    "index": 0
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
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Null | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |