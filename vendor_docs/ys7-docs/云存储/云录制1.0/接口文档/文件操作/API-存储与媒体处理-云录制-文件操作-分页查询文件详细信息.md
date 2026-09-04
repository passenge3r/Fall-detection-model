# API-存储与媒体处理-云录制-文件操作-分页查询文件详细信息

> 更新时间: 2026-06-30T17:51:57.000+08:00

> 文档ID: 1374 | 来源树: 云存储

---

## 分页查询文件详细信息

- 接口功能

   分页查询文件详细信息。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/files`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Query | startTime | String | 查询起始时间，若不传时间则默认当天，格式: yyyyMMddHHmmss | N |
| Query | endTime | String | 查询结束时间，若不传时间则默认当天，格式: yyyyMMddHHmmss，结束时间与开始时间不允许跨天，查询时间以文件创建时间为准，目前不支持排序 | N |
| Query | pageNumber | Int | 分页页码，以0开始，默认0 | N |
| Query | pageSize | Int | 分页大小，取值范围[1,20]，默认10 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/open/cloud/v1/files?accessToken=at.xxxxx&projectId=001&startTime=20221216143333&endTime=20221216211011&pageNumber=0&pageSize=2'
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
            "projectId": "111",
            "fileId": "774a4e0f4e9c42ecacc38b7bf1383b0a",
            "fileType": 0,
            "status": 0,
            "fileCount": 1,
            "fileSize": 278221,
            "duration": 0,
            "errorCode": "0",
            "expireTime": "2023-01-15T14:33:33",
            "storageType": 1,
            "lastTransferTime": null,
            "unfreezeTime": null,
            "createTime": "2022-12-16T14:33:33",
            "updateTime": "2022-12-16T14:33:33",
            "taskId": "df0a6843052e4b5fa8b7895dbba8fa8d",
            "downloadUrls": null,
            "replayRecord": false
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Array | 文件详细信息列表 |
| data[].projectId | String | 项目ID |
| data[].fileId | String | 文件ID |
| data[].fileType | Int | 文件类型 0-图片 1-视频 |
| data[].status | Int | 文件状态 0-正常 1-上传中 2-上传失败 3-已过期 4-已删除 |
| data[].fileCount | Int | 实际文件个数，视频文件过大时可能拆分成多个小文件 |
| data[].fileSize | Int | 文件整体大小，单位：字节 |
| data[].duration | Int | 视频文件时长，单位：秒 |
| data[].errorCode | String | 错误码 |
| data[].expireTime | String | 到期时间 |
| data[].storageType | Int | 项目存储类型 1-标准存储 2-存档存储 |
| data[].lastTransferTime | String | 文件存储类型最后一次转换时间 |
| data[].unfreezeTime | String | 文件解冻有效期 |
| data[].createTime | String | 创建时间 |
| data[].updateTime | String | 操作时间 |
| data[].taskId | String | 任务编号 |
| data[].downloadUrls | Array | 下载地址 |
| data[].replayRecord | Boolean | 文件是否为回放录制产生的文件，false-否，true-是 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 429 | 请求过于频繁 | 降低请求频率后重试 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |