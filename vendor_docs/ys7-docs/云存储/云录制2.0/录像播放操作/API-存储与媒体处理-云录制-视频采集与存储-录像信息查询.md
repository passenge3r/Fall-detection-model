# API-存储与媒体处理-云录制-视频采集与存储-录像信息查询

> 更新时间: 2026-06-25T14:29:57.000+08:00

> 文档ID: 2043 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-录像信息查询

- 接口功能

   录像信息查询。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/info/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | localIndex | String | 通道号 | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| query | startTime | String | 开始时间，时间格式为：yyyy-MM-dd HH:mm:ss | Y |
| query | endTime | String | 结束时间，时间格式为：yyyy-MM-dd HH:mm:ss，不允许跨天 | Y |
| query | spaceId | Long | 空间ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/info/list?startTime=2025-09-02%2021%3A46%3A05&endTime=2025-09-02%2022%3A46%3A05&spaceId=44028' \
--header 'accessToken: at.xxxxx' \
--header 'localIndex: 1' \
--header 'deviceSerial: 553055114'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "id": 339,
            "fileId": "20240124115700-C11633138-1-26-0285",
            "spaceId": 38,
            "deviceSerial": "C11633138",
            "channelNo": "1",
            "ownerId": "openteam",
            "fileType": 1,
            "cloudType": 51,
            "fileIndex": "20240124115700-C11633138-1-26-0285",
            "startTime": "20240124115700",
            "stopTime": "20240124115801",
            "fileSize": 1213224,
            "locked": 0,
            "createTime": "20240124120550",
            "crypt": 0,
            "keyChecksum": "",
            "videoLong": 61000,
            "coverPic": "https://recordstreamertxsh.ys7.com:8091/api/cloud/record?method=download&fid=20240124115700-C11633138-1-26-0285&fileType=1&deviceSerialNo=C11633138&cn=1&startTime=1706068624000&endTime=1706068681000&storageVersion=2&ticket=xxxxx&bizCode=CLOUD_RECORD",
            "downloadPath": "recordstreamertxsh.ys7.com:32721",
            "type": 1,
            "videoType": 1,
            "totalDays": 3650,
            "sliceLength": 10,
            "expireTime": "20340121130550",
            "istorageVersion": 2
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回信息 |
| -code | Int | 错误码 |
| -message | String | 错误信息 |
| data | Object | 返回数据 |
| -fileInfos | Array<Object> | 录像信息列表 |
| --startTime | String | 文件开始时间 |
| --endTime | String | 文件结束时间 |
| --deviceSerial | String | 设备序列号 |
| --channelNo | String | 设备通道号 |
| --fileId | String | 文件ID |
| --ownerId | String | 文件所有者ID |
| --cloudType | Int | 云存储类型：存储位置修改，当前未开放，0-未知 |
| --fileIndex | String | 文件索引 |
| --fileSize | Long | 文件大小 |
| --downloadPath | String | 下载路径，录像片段播放时使用，无法直接访问 |
| --type | Int | 云存储来源 |
| --iStorageVersion | Int | 1 单文件存储模式；2 连续存储模式；3 待定 |
| --spaceId | Long | 空间ID |
| --coverPic | String | 封面图，客户端打开封面图需要自行拼接&x=400和&decodekey=xxx |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |