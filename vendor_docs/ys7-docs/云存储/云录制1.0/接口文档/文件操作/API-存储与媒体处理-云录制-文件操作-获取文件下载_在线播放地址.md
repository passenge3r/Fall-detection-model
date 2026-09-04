# API-存储与媒体处理-云录制-文件操作-获取文件下载/在线播放地址

> 更新时间: 2026-06-30T17:52:09.000+08:00

> 文档ID: 1377 | 来源树: 云存储

---

## 获取文件下载/在线播放地址

- 接口功能

   获取文件下载/在线播放地址。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/file/official/download`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户令牌 | Y |
| Query | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Query | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Query | contentType | String | 文件在线播放参数，填写对应的文件格式后可以在线播放文件，可填写的参数有：video/flv,image/png,video/mp4,image/jpg,image/jpeg，一般云录制视频文件为MP4格式，图片文件为jpeg格式 | N |
| Query | expireSeconds | Long | 过期时间，单位秒，默认7200，【60-604800】 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/file/official/download?fileId=7b09224c0223494d91bbd04def495966&projectId=001&contentType=video/mp4&expireSeconds=7200' \
--header 'accessToken: at.xxxxx'
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
        "expire": 1673610578230,
        "urls": [
            "http://openrecord.ys7.com/VIDEO_PREVIEW_FILES/xxxx/001/BD3957004-1/xxxx.mp4?Expires=xxxx&OSSAccessKeyId=xxxxx&Signature=xxxxx&response-content-type=video%2Fmp4"
        ]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 文件下载信息 |
| data.expire | Long | 下载地址过期时间 |
| data.urls | Array | 文件下载/在线播放地址列表 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |