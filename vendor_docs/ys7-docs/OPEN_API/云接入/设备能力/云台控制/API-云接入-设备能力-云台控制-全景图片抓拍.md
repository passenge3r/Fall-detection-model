# API-云接入-设备能力-云台控制-全景图片抓拍

> 更新时间: 2026-07-09T13:34:13.000+08:00

> 文档ID: 685 | 来源树: OPEN_API

---

## 全景图片抓拍

- 接口功能

   全景图片抓拍。设备能力集：support\_location\_capture。注：因图片存放在云录制空间，所以需要事先开通云录制，否则会失败。 子账户token请求所需最小权限："Permission":"Ptz" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/pic/panoramic/compose`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 资源号 | Y |
| Body | projectId | String | 项目ID | Y |
| Body | validateCode | String | 加密密钥，输入设备加密密钥 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/pic/panoramic/compose' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'localIndex: 1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'projectId=xxxxx' \
--data-urlencode 'validateCode=xxxxx'
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
        "taskId": "4d9d0a832dcf4d3882894c7b08031012"
    }
}
```

   注：抓图结果通过 ys.open.cloud 消息返回（详见下方"抓图返回消息体"）。也可以通过云录制接口[根据任务ID查询文件列表](https://open.ys7.com/help/1378)查询。

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 返回码 |
| message | String | 返回信息 |
| moreInfo | String | 附加信息 |
| data | Object | 业务数据 |
| taskId | String | 任务id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |
| 400 | 参数不正确 |  |
| 404 | 资源不存在 |  |
| 500 | 服务异常 |  |

- 抓图返回消息体（消息类型：ys.open.cloud）

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| header | Object | 设备信息 |
| userId | String | 用户id |
| deviceId | String | 设备id |
| channelNo | Int | 通道id |
| type | String | ys.open.cloud |
| messageTime | Long | 消息时间 |
| body | Object | 消息体 |
| userId | String | 用户id |
| deviceSerial | String | 设备序列号 |
| channelNo | String | 设备通道 |
| projectId | String | 项目id |
| fileId | String | 全景图片id |
| taskId | String | 任务id |
| errorCode | String | 错误码：COLLECT\_FAIL("40001","device capture fail")；PROJECT\_NOT\_EXIST("40002","project not exist")；FILE\_STORAGE\_TYPE\_ERROR("40003","file not allow archive")；SERVER\_ERROR("40005","internal error")；UPLOAD\_URL\_FAIL("40006","get upload fail")；TASK\_EXPIRE("40007","task expire")；PANORAMIC\_CAPTURE\_STORAGE\_ERROR("40008","panoramic storageId error") |
| errorMsg | String | 错误信息 |
| downloadUrl | String | 下载链接（2小时有效） |
| activeTime | Long | 有效时间 |
| messageType | String | panoramic\_capture |