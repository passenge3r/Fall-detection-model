# API-存储与媒体处理-云录制-视频采集与存储-即时视频转码录制存储接口

> 更新时间: 2026-06-30T17:52:25.000+08:00

> 文档ID: 1382 | 来源树: 云存储

---

## 即时视频转码录制存储接口

- 接口功能

   立即开始进行视频录制。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/instant/record/save`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 设备通道号，默认1 | N |
| Body | projectId | String | 项目id | Y |
| Body | recordSeconds | Int | 录制时长，单位秒，默认86400秒（24小时） | N |
| Body | validateCode | String | 录像解密密钥，若设备加密则必须填写，否则视频无法录制成功 | N |
| Body | sliceDuration | Int | 录像文件片段时长，单位分钟，范围：30分钟-210分钟，默认30分钟 | N |
| Body | retryNum | Int | 任务重试次数，支持设置0-5次，默认不重试，不能超过5次 | N |
| Body | streamType | Int | 码流类型，1-高清，2-标清，默认1 | N |
| Body | voiceSwitch | Int | 录制视频声音开关，0.关 1.开 2.自动，默认2 | N |
| Body | devProto | String | 设备协议：gb28181(国标)，不传默认为萤石协议 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/instant/record/save' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: BD3957004' \
--header 'localIndex: 1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'projectId=001' \
--data-urlencode 'recordSeconds=86400' \
--data-urlencode 'sliceDuration=30' \
--data-urlencode 'streamType=1' \
--data-urlencode 'voiceSwitch=1'
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