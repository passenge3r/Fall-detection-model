# API-存储与媒体处理-云录制-视频采集与存储-预约视频转码录制存储接口

> 更新时间: 2026-06-30T17:52:32.000+08:00

> 文档ID: 1383 | 来源树: 云存储

---

## 预约视频转码录制存储接口

- 接口功能

   从实时视频中取流进行转码录制。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/preview/save`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | channelNo | Int | 通道号 | Y |
| Body | deviceSerial | String | 设备序列号，由于转码限制，仅支持AAC音频编码的设备有声录制 | Y |
| Body | startTime | String | 录像开始时间，格式: yyyyMMddHHmmss，开始时间需在未来10分钟后 | Y |
| Body | endTime | String | 录像结束时间，格式: yyyyMMddHHmmss，结束时间和开始时间之差需在24小时之内 | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Body | validateCode | String | 录像解密密钥，若设备加密则必须填写，否则视频无法录制成功 | N |
| Body | voiceSwitch | String | 录制视频声音开关，0.关 1.开 2.自动，默认2，如果音频不是AAC，则自动关闭视频声音 | N |
| Body | devProto | String | 若不传，则标识为萤石协议；若传gb28181，标识为国标设备；默认不传 | N |
| Body | streamType | String | 码流类型，可以选择 1：高清（主码流）2：标清（子码流） | N |
| Body | aiBox | String | 是否需要录制Ai框，0关 1开，默认关闭 | N |
| Body | sliceDuration | Int | 录像文件片段时长，单位分钟，范围：30分钟-210分钟，默认30分钟 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/preview/save' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'deviceSerial=F03175298' \
--data-urlencode 'startTime=20220324120000' \
--data-urlencode 'endTime=20220324130000' \
--data-urlencode 'projectId=001'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "taskId": "eba536dd28274723ac6870f16576a037"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 返回任务信息 |
| data.taskId | String | 任务ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |