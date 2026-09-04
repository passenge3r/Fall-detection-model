# API-存储与媒体处理-云录制-图片二次处理-ISAPI图片缩略图接口

> API-存储与媒体处理-云录制-图片二次处理-ISAPI图片缩略图接口

> 更新时间: 2026-06-30T17:54:08.000+08:00

> 文档ID: 1396 | 来源树: 云存储

---

## ISAPI图片缩略图接口

- 接口功能

   该接口用于指定项目id和文件id对应的图片生成缩略图，可生成一次性缩略图或者生成持久化存储的缩略图。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file/download/resize`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | bizType | String | 业务类型，下载ISAPI文件时必填 isapi | Y |
| body | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| body | saveOrNot | String | 是否存储：save=存储,会返回新文件的fileId，not=不存储 | Y |
| body | resizeType | String | 缩放的方式：ratio:等比缩放-关联size，measure:指定尺寸-关联high和width | Y |
| body | high | Integer | 指定缩放的高度(不填默认150) | N |
| body | width | Integer | 指定缩放的宽度(不填默认150) | N |
| body | size | Integer | 缩放比例,默认缩50%，参数范围[1,100]，1代表等比例缩小到原图的1%，100代表缩小到原图的100% | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/file/download/resize' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'size=' \
--data-urlencode 'high=' \
--data-urlencode 'width=' \
--data-urlencode 'resizeType=' \
--data-urlencode 'projectId=' \
--data-urlencode 'fileId=' \
--data-urlencode 'saveOrNot=' \
--data-urlencode 'bizType=isapi'
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
        "urls": ["http://xxxx.xxx.com/org.jpg"],
        "operationUrls": ["http://xxxx.xxx.com/ops.jpg"],
        "expire": 1598266535250,
        "newFileId": "xxxxx"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| meta.code | Integer | 返回状态码，200表示成功 |
| meta.message | String | 返回状态描述 |
| data | Object | 响应内容 |
| urls | Array | 原图文件下载URL列表 |
| operationUrls | Array | 水印图片下载URL列表 |
| newFileId | String | 存储文件的ID |
| expire | Long | 过期时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |