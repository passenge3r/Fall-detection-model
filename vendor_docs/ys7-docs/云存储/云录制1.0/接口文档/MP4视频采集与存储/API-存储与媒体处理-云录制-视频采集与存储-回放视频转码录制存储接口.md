# API-存储与媒体处理-云录制-视频采集与存储-回放视频转码录制存储接口

> 更新时间: 2026-07-01T18:44:23.000+08:00

> 文档ID: 1381 | 来源树: 云存储

---

## 回放视频转码录制存储接口

- 接口功能

创建回放录制任务，从回放视频中取流进行转码录制，支持删除任务。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/rec/video/save`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 设备通道，默认1 | N |
| Body | projectId | String | 项目ID（即项目编号），项目的唯一标识，需输入已创建的项目ID | Y |
| Body | recType | String | 录像类型，local-本地录像，cloud-云存储，record-云录制2.0 | Y |
| Body | startTime | String | 录像开始时间，格式: yyyyMMddHHmmss | Y |
| Body | endTime | String | 录像结束时间，格式: yyyyMMddHHmmss | Y |
| Body | devProto | String | 若不传，则标识为萤石协议；若传gb28181，标识为国标设备；默认不传 | N |
| Body | validateCode | String | 录像解密密钥，若设备加密则必须填写，否则视频无法录制成功；若设备未加密，则该入参不要传 | N |
| Body | voiceSwitch | String | 录制视频声音开关，0.关 1.开 2.自动，默认2，如果音频不是AAC，则自动关闭视频声音 | N |
| Body | streamType | Int | 码流类型，云存储视频录制可以选择 1：高清（主码流）2：标清（子码流）；设备本地的回放视频只按主码流存储，无需选择 | N |
| Body | format | String | 视频封装类型，默认format=mp4，即以MP4格式进行录制；当format=ps时，会直接录制ps流 | N |
| Body | aiBox | String | 是否需要录制Ai框，0关 1开，默认关闭 | N |
| Body | sliceDuration | Int | 录像文件片段时长，单位分钟，范围：30分钟-210分钟，默认30分钟 | N |
| Body | recordSpeed | String | 默认不填此参数，可填参数为1/2/4。1：正常倍速；2：2倍速；4：4倍速；注意：4倍速会对录像进行抽帧，录像时长可能与预计时长不匹配，建议使用2倍速。云存储回放不支持倍速 | N |
| Body | filePrefix | String | 自定义前缀命名后可以对任务内的文件名称进行命名 | N |
| Body | spaceId | String | 当recType=record时必填，填写对应云录制2.0的空间ID | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/rec/video/save' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: BD3957004' \
--header 'localIndex: 1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'projectId=001' \
--data-urlencode 'recType=cloud' \
--data-urlencode 'startTime=20220324120000' \
--data-urlencode 'endTime=20220324130000'
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