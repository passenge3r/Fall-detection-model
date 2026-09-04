# API-云通话-云广播-告警提示音设置-设备告警提示音设置接口

> 更新时间: 2026-07-01T18:25:18.000+08:00

> 文档ID: 1277 | 来源树: OPEN_API

---

## 设备告警提示音设置接口

- 接口功能

   设备告警提示音设置接口，PUT参数放在请求链接里。

- 请求地址

`https://open.ys7.com/api/route/alarm/v3/devices/{deviceSerial}/alarm/sound`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 访问令牌 | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Query | voiceId | Int | 设备语音唯一id，soundType=3时有效 | N |
| Query | enable | Int | 0-关闭，1-开启 | Y |
| Query | soundType | Int | 0-短叫，1-长叫，2-静音，3-自定义语音 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/route/alarm/v3/devices/{deviceSerial}/alarm/sound?accessToken=at.xxxxx&voiceId=1&enable=1&soundType=0'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| meta.code | Int | 操作码，200表示操作成功 |
| meta.message | String | 提示信息 |
| meta.moreInfo | Object | 详细信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 111001 | 语音文件格式错误 |  |
| 111002 | 语音文件时长不合法 |  |
| 111003 | 语音文件上传失败 |  |
| 111004 | 语音文件转换失败 |  |
| 111005 | 语音文件时长获取 |  |
| 111006 | 语音文件列表获取失败 |  |
| 111007 | 下发的语音文件URL不存在 |  |
| 111008 | 参数错误，语音文件不能为空 |  |
| 111009 | 参数错误，语音文件URL不能为空 |  |
| 111010 | 参数错误，设备序列号不能为空 |  |
| 111011 | 参数错误，通道号不能为空 |  |

   其它错误码见[错误码](https://open.ys7.com/help/78)。