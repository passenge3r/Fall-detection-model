# API-存储与媒体处理-云录制-文件操作-单条查询文件详细信息

> 更新时间: 2026-06-30T17:52:01.000+08:00

> 文档ID: 1375 | 来源树: 云存储

---

## 单条查询文件详细信息

- 接口功能

   开发者查询单条文件详细信息。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Query | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/open/cloud/v1/file?accessToken=at.xxxxx&fileId=7d2d79ba6f8e499dbcaa13b6b4a00154&projectId=001'
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
        "projectId": "111",
        "fileId": "7d2d79ba6f8e499dbcaa13b6b4a00154",
        "fileType": 1,
        "status": 0,
        "fileCount": 1,
        "fileSize": 4972498,
        "duration": 60,
        "errorCode": "0",
        "expireTime": "2023-01-15T14:46:32",
        "storageType": 1,
        "lastTransferTime": null,
        "unfreezeTime": null,
        "createTime": "2022-12-16T14:46:32",
        "updateTime": "2022-12-16T14:46:32",
        "taskId": "976ce4504e4541dd9fdd6d2cc69f63cf",
        "downloadUrls": null,
        "replayRecord": false
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 文件详细信息 |
| data.projectId | String | 项目ID |
| data.fileId | String | 文件ID |
| data.fileType | Int | 文件类型 0-图片 1-视频 |
| data.status | Int | 文件状态 0-正常 1-上传中 2-上传失败 3-已过期 4-已删除 |
| data.fileCount | Int | 实际文件个数，视频文件过大时可能拆分成多个小文件 |
| data.fileSize | Int | 文件整体大小，单位：字节 |
| data.duration | Int | 视频文件时长，单位：秒 |
| data.errorCode | String | 错误码 |
| data.expireTime | String | 到期时间 |
| data.storageType | Int | 项目存储类型 1-标准存储 2-存档存储 |
| data.lastTransferTime | String | 文件存储类型最后一次转换时间 |
| data.unfreezeTime | String | 文件解冻有效期 |
| data.createTime | String | 创建时间 |
| data.updateTime | String | 操作时间 |
| data.taskId | String | 任务编号 |
| data.downloadUrls | Array | 下载地址 |
| data.replayRecord | Boolean | 文件是否为回放录制产生的文件，false-否，true-是 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |