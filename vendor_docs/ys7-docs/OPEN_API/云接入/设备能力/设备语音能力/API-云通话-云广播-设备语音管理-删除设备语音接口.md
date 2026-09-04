# API-云通话-云广播-设备语音管理-删除设备语音接口

> 更新时间: 2026-07-01T18:25:31.000+08:00

> 文档ID: 1281 | 来源树: OPEN_API

---

## 删除设备语音接口

- 接口功能

   删除设备上的语音文件，DELETE参数放在请求链接里。

- 请求地址

`https://open.ys7.com/api/route/voice/v3/devices/voices`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 访问令牌 | Y |
| Query | deviceSerial | String | 设备序列号 | Y |
| Query | voiceId | Int | 设备语音唯一id | Y |
| Query | voiceName | String | 设备语音名称 | Y |
| Query | voiceUrl | String | 语音文件url | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/route/voice/v3/devices/voices?accessToken=at.xxxxx&deviceSerial=G12262381&voiceId=1&voiceName=test&voiceUrl=http://xxx.xxx.com/xxx.mp3'
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