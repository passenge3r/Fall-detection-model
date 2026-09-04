# 根据任务ID查询文件列表

> 根据任务id查询文件列表

> 更新时间: 2026-06-01T17:13:12.000+08:00

> 文档ID: 1373 | 来源树: 云存储

---

## 根据任务ID查询文件列表

- 接口功能

   根据任务id查询文件列表。

- 请求地址

`https://open.ys7.com/api/v3/open/cloud/task/files`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| query | accessToken | String | 萤石开放API访问令牌 | Y |
| query | taskId | String | 任务ID | Y |
| query | pageNumber | Int | 分页页码，以0开始，默认为0 | Y |
| query | pageSize | Int | 分页大小，从1开始，不能大于50 | Y |
| query | sortField | String | 排序字段，默认为createTime，表示创建时间 | N |
| query | sortRule | String | 排序规则，asc：升序，desc：降序 | N |
| query | hasUrl | Boolean | 是否需要下载链接，true：需要，false：不需要，默认false。若文件移动至归档存储且未解冻，下载链接为空 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/open/cloud/task/files?accessToken=at.xxx&taskId=d0015b1769e845b0a478e9ec3fc3555c&pageNumber=0&pageSize=2&sortField=createTime&sortRule=asc&hasUrl=true'
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
            "fileId": "7b09224c0223494d91bbd04def495966",
            "fileType": 1,
            "status": 0,
            "fileCount": 1,
            "fileSize": 4337348,
            "duration": 60,
            "errorCode": "0",
            "expireTime": "2023-02-03T16:42:57",
            "storageType": 1,
            "lastTransferTime": null,
            "unfreezeTime": null,
            "createTime": "2023-01-04T16:42:57",
            "updateTime": "2023-01-04T16:42:57",
            "taskId": "d0015b1769e845b0a478e9ec3fc3555c",
            "downloadUrls": [
                "http://open-mediarecoder.oss-cn-hangzhou.aliyuncs.com/..."
            ],
            "replayRecord": false,
            "resultSpaceId": 270326,
            "outputType": 4
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应元信息 |
| data | Array | 文件列表 |
| data[].projectId | String | 文件所属项目ID |
| data[].fileId | String | 文件ID |
| data[].fileType | Int | 文件类型：0-.jpg，1-.mp4 |
| data[].status | Int | 文件状态：0-正常，1-正在上传，2-上传失败，3-已过期，4-已删除 |
| data[].fileCount | Int | 文件实际个数，视频文件可能过大被拆分成多个小文件 |
| data[].fileSize | Long | 文件大小，单位：字节 |
| data[].duration | Int | 转码时长，单位：秒 |
| data[].errorCode | String | 文件上传错误码 |
| data[].expireTime | String | 文件过期时间 |
| data[].storageType | Int | 项目存储类型：1-标准存储，2-存档存储 |
| data[].lastTransferTime | String | 文件存储类型最后一次转换时间 |
| data[].unfreezeTime | String | 文件解冻有效期 |
| data[].createTime | String | 文件记录创建时间 |
| data[].taskId | String | 任务编号 |
| data[].downloadUrls | Array | 下载地址列表 |
| data[].replayRecord | Boolean | 文件是否为回放录制产生的文件，false-否，true-是 |
| data[].timePoint | String | 抽帧文件产生对应的时间点，仅针对抽帧任务生效，格式为yyyy-MM-dd'T'HH:mm:ss |
| data[].resultSpaceId | Long | 统一存储空间id |
| data[].outputType | Int | 输出文件类型：1-云录制1.0，4-存储空间id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |