# API-云通话-云广播-设备语音管理-获取设备语音列表接口

> 更新时间: 2026-07-01T18:23:30.000+08:00

> 文档ID: 1259 | 来源树: OPEN_API

---

## 获取设备语音列表接口

- 接口功能

   获取指定设备的语音列表，GET参数放在请求链接里。

- 请求地址

`https://open.ys7.com/api/route/voice/v3/devices/voices`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 访问令牌 | Y |
| Query | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/route/voice/v3/devices/voices?accessToken=at.xxxxx&deviceSerial=G12262381'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "voiceInfos": [
        {
            "voiceId": 1,
            "voiceName": "测试语音",
            "voiceUrl": "http://custom-voice-reminder-hn.oss-cn-shenzhen.aliyuncs.com/voice/e8e131c4e4684f4f8460f4676b5b777d.aac?Expires=1584433153&OSSAccessKeyId=xxxxx&Signature=xxxxx",
            "status": 1,
            "time": 1584375603
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| meta.code | Int | 操作码，200表示操作成功 |
| meta.message | String | 提示信息 |
| meta.moreInfo | Object | 详细信息 |
| voiceInfos | Array | 设备语音文件信息列表 |
| voiceInfos[].voiceId | Int | 语音文件id |
| voiceInfos[].voiceName | String | 语音名称 |
| voiceInfos[].voiceUrl | String | 语音文件url |
| voiceInfos[].status | Int | 平台和设备语音同步状态，0:同步完成，1:正在同步，2:同步失败 |
| voiceInfos[].time | Int | 语音创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |