# API-存储与媒体处理-云录制-图片二次处理-图片缩略图

> 更新时间: 2026-06-30T17:53:57.000+08:00

> 文档ID: 1395 | 来源树: 云存储

---

## 图片缩略图接口

- 接口功能

   指定项目id和文件id对应的图片生成缩略图接口，可生成一次性缩略图或者生成持久化存储的缩略图。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file/operation/resize`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Body | newFileId | String | 新文件ID有值，会存储生成的缩略图，不覆盖原图；没有值，只会生成一次性的图片url | N |
| Body | newProjectId | String | 新项目ID，如果要存储新的文件，必填，否则不填 | N |
| Body | resizeType | String | 缩放的方式：ratio:等比缩放–关联size；measure:指定尺寸-关联high和width | Y |
| Body | high | Int | 指定缩放的高度（不填默认150） | N |
| Body | width | Int | 指定缩放的宽度（不填默认150） | N |
| Body | size | Int | 缩放比例，默认缩小50%，参数范围[1,100]，1代表等比例缩小到原图的1%，100代表缩小到原图的100% | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/file/operation/resize' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'projectId=001' \
--data-urlencode 'fileId=K19978742-1' \
--data-urlencode 'resizeType=ratio' \
--data-urlencode 'size=50'
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
| data | Object | 响应内容 |
| urls | Array | 原图文件下载URL列表 |
| operationUrls | Array | 缩略图下载URL列表 |
| newFileId | String | 存储文件的ID |
| expire | Long | 过期时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |