# 创建直播流（RTMP接入推流）

> 更新时间: 2026-06-23T16:32:40.000+08:00

> 文档ID: 4433 | 来源树: OPEN_API

---

## 创建直播流（RTMP接入推流）

- 接口功能

   创建直播流，支持at token、托管，Real权限

- 请求地址

`https://open.ys7.com/api/service/media/streammanage/stream`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | string | 萤石开放平台用户的accessToken，支持at token、托管，Real权限 | Y |
| query | accessType | int | 接入类型：2-rtmp接入 （必传） | Y |
| query | startTime | string | 开始时间，accessType为1时生效，时间格式：yyyy-MM-dd HH:mm:ss，开始时间和结束时间跨度最多7天 | Y |
| query | endTime | string | 结束时间，accessType为1时生效，时间格式：yyyy-MM-dd HH:mm:ss，开始时间和结束时间跨度最多7天，结束时间不能小于等于当前时间 | Y |
| query | enableRecord | int | 是否录制：0-否（默认），1-是，accessType为2时生效 | N |
| query | recordSpaceId | string | 云存储空间Id,没传会使用默认空间(永久时效) | N |
| query | recordDuration | int | 周期录制时长，单位：秒。取值范围：15分钟~120分钟，不填则默认为 120 分钟。accessType为2时生效 | N |
| query | recordFormat | int | 录制格式：1-MP4（默认），2-M3U8 。accessType为2时生效 | N |
| query | delayTime | int | 断流拼接时长。 直播断流时长超过设定的拼接时长后，将会生成新文件，断流拼接时长支持 15~21600 秒。 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/media/streammanage/stream' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "data": {
        "streamId": "787305182210818048" //系统自动生成的32为字符串，直播流的唯一标识
    },
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
| data | object | data |
| -streamId | string | streamId |
| meta | object | meta |
| -code | int | code |
| -message | string | message |
| -moreInfo | object | moreInfo |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 10001 | 参数错误 | 参数错误 |
| 50000 | 服务异常 | 服务异常 |