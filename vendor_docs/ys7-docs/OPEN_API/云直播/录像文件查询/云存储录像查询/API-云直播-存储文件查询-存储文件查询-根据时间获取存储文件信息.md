# API-云直播-存储文件查询-存储文件查询-根据时间获取存储文件信息

> API-云直播-存储文件查询-存储文件查询-根据时间获取存储文件信息

> 更新时间: 2026-06-30T17:54:42.000+08:00

> 文档ID: 1422 | 来源树: OPEN_API

---

## 根据时间获取存储文件信息

- 接口功能

   该接口用于根据时间获取存储文件信息。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/video/by/time`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 访问令牌 | Y |
| body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 通道号，非必选，默认为1 | N |
| body | startTime | Long | 起始时间，时间格式为：1378345128000。非必选，默认为当天0点 | N |
| body | endTime | Long | 结束时间，时间格式为：1378345128000。非必选，默认为当前时间 | N |
| body | recType | Int | 回放源，0-系统自动选择，1-云存储，2-本地录像。非必选，默认为0 | N |
| body | version | String | 返回分页结构，recType=1时，传2.0会返回分页结构；recType=2时，传2.0且pageSize不为空的情况才会返回分页结构 | N |
| body | pageSize | Int | recType为1或2时，可指定返回的文件数量，云存储类型分页大小范围:1-1000，本地录像类型分页大小范围:1-500 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/video/by/time' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734203' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'startTime=1378345128000' \
--data-urlencode 'endTime=1378345128000' \
--data-urlencode 'recType=0'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功",
    "data": [
        {
            "recType": 0,
            "startTime": 1378345128000,
            "endTime": 1378345128000,
            "deviceSerial": "409864662",
            "cameraNo": "1",
            "localType": "ALLEVENT",
            "channelType": "D",
            "id": 20432171600,
            "fileId": "20432171600",
            "ownerId": "chenyong",
            "fileType": 1,
            "fileName": "",
            "cloudType": 1,
            "fileIndex": "5d5b6d94-13e8-440b-a25b-00eda521c35f",
            "fileSize": 4011828,
            "locked": 0,
            "createTime": "2016-08-22 13:59:13",
            "crypt": 22,
            "keyChecksum": "",
            "videoLong": 150000,
            "coverPic": "https://218.244.139.5:0/api/cloud?method=download&fid=xxxxx&session=xxxxx",
            "downloadPath": "218.244.139.5:0",
            "type": 1
        },
        {
            "recType": 0,
            "startTime": 1378345128000,
            "endTime": 1378345128000,
            "deviceSerial": "409864662",
            "cameraNo": "1",
            "localType": "ALLEVENT",
            "channelType": "D",
            "id": 20432171600,
            "fileId": "20432171600",
            "ownerId": "chenyong",
            "fileType": 1,
            "fileName": "",
            "cloudType": 1,
            "fileIndex": "5d5b6d94-13e8-440b-a25b-00eda521c35f",
            "fileSize": 4011828,
            "locked": 0,
            "createTime": "2016-08-22 13:59:13",
            "crypt": 22,
            "keyChecksum": "",
            "videoLong": 150000,
            "coverPic": "https://218.244.139.5:0/api/cloud?method=download&fid=xxxxx&session=xxxxx",
            "downloadPath": "218.244.139.5:0",
            "type": 1
        }
    ]
}
```

- 返回数据（分页结构返回）

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": {
        "files": [
            {
                "recType": 2,
                "startTime": 1691627391000,
                "endTime": 1691627443000,
                "deviceSerial": "G12262381",
                "channelNo": 1,
                "localType": "ALARM",
                "channelType": "D",
                "id": null,
                "fileId": null,
                "ownerId": null,
                "fileType": 0,
                "fileName": null,
                "cloudType": 0,
                "fileIndex": null,
                "fileSize": 0,
                "locked": 0,
                "createTime": 0,
                "crypt": 0,
                "keyChecksum": null,
                "videoLong": 0,
                "coverPic": null,
                "downloadPath": null,
                "type": 1,
                "iStorageVersion": null,
                "videoType": null
            },
            {
                "recType": 2,
                "startTime": 1691627491000,
                "endTime": 1691627537000,
                "deviceSerial": "G12262381",
                "channelNo": 1,
                "localType": "ALARM",
                "channelType": "D",
                "id": null,
                "fileId": null,
                "ownerId": null,
                "fileType": 0,
                "fileName": null,
                "cloudType": 0,
                "fileIndex": null,
                "fileSize": 0,
                "locked": 0,
                "createTime": 0,
                "crypt": 0,
                "keyChecksum": null,
                "videoLong": 0,
                "coverPic": null,
                "downloadPath": null,
                "type": 1,
                "iStorageVersion": null,
                "videoType": null
            },
            {
                "recType": 2,
                "startTime": 1691627537000,
                "endTime": 1691627586000,
                "deviceSerial": "G12262381",
                "channelNo": 1,
                "localType": "ALARM",
                "channelType": "D",
                "id": null,
                "fileId": null,
                "ownerId": null,
                "fileType": 0,
                "fileName": null,
                "cloudType": 0,
                "fileIndex": null,
                "fileSize": 0,
                "locked": 0,
                "createTime": 0,
                "crypt": 0,
                "keyChecksum": null,
                "videoLong": 0,
                "coverPic": null,
                "downloadPath": null,
                "type": 1,
                "iStorageVersion": null,
                "videoType": null
            }
        ],
        "isAll": false,
        "nextFileTime": 1691627586000
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| recType | Int | 回放源，0-系统自动选择，1-云存储，2-本地录像 |
| startTime | Long | 文件开始时间 |
| endTime | Long | 文件结束时间 |
| deviceSerial | String | 设备序列号 |
| channelNo | Int | 设备通道号 |
| localType | String | 文件类型 0:ALARM 1:TIMING 2:IO |
| channelType | String | 该字段已废弃 |
| id | Long | 云存储信息主键ID（以下信息只有云存储有返回，本地存储返回为null或0） |
| fileId | String | 文件ID |
| ownerId | String | 文件所属用户ID |
| fileType | Int | 文件类型 0:目录 1:视频文件 2:图片文件 3:音频文件 |
| fileName | String | 文件名称 |
| cloudType | Int | 该字段已废弃 |
| fileIndex | String | 文件在云存储上的唯一索引 |
| fileSize | Long | 文件大小，单位B |
| locked | Int | 是否被锁定。1-锁定；0-未锁定 |
| createTime | Long | 创建时间 |
| crypt | Int | 是否加密 0-不加密 1-加密 |
| keyChecksum | String | 验证码MD5值 |
| videoLong | Long | 录像长度 |
| coverPic | String | 封面图片地址 |
| downloadPath | String | 该字段会出现在云存储录像查询中，不可用于下载录像（如需保存录像，可以使用UIkit或SDK中的录制功能） |
| type | Int | 该字段已废弃 |
| isAll | Boolean | 分页结构返回字段，是否已返回全部数据 |
| nextFileTime | Long | 分页结构返回字段，下一个文件的时间，可当参数传入startTime，继续查询剩余的文件。isAll为true时，该值为0，说明已返回全部数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 |  |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 |  |
| 10011 | 未开通萤石服务 | 设备对应用户未注册至应用下 |
| 10013 | 非开发者账号无权限调用 |  |
| 10030 | appkey和appsecret不匹配 |  |
| 20002 | 设备不存在 | 设备序列号输入有误或者设备未被添加或者通道异常 |
| 20014 | deviceSerial不合法 |  |
| 20032 | 该用户下通道不存在 |  |
| 60024 | 取消订阅操作失败 |  |
| 49999 | 操作异常 |  |