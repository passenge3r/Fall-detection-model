# API-存储与媒体处理-云录制-图片二次处理-图片加水印接口-ISAPI 图片加水印接口

> 更新时间: 2026-06-30T17:53:55.000+08:00

> 文档ID: 1394 | 来源树: 云存储

---

## ISAPI图片加水印接口

- 接口功能

   指定项目id和文件id对应的ISAPI图片加水印接口，可生成一次性水印图片或者生成持久化存储的水印图片，可自主选择是否要存储，不覆盖原图。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file/download/watermark`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | bizType | String | 业务类型，下载ISAPI文件时必填isapi | Y |
| Body | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Body | saveOrNot | String | 是否存储：save=存储，会返回新文件的fileId；not=不存储 | Y |
| Body | text | String | 水印文本，最大21个汉字或者64个字符 | Y |
| Body | transparency | Int | 水印透明度[0,100]，默认值：100，表示透明度100%（不透明） | N |
| Body | site | String | nw：左上、north：中上、ne：右上、west：左中、center：中部、east：右中、sw：左下、south：中下、se：右下，默认值:se | N |
| Body | color | String | RGB颜色值，例如：000000表示黑色，FFFFFF表示白色，默认值：000000（黑色） | N |
| Body | size | Int | 指定水印文字的大小，如果水印文字过大，只会展示一部分，请合理设置水印大小，范围(0,1000]，默认值：40，单位：px | N |
| Body | rotate | Int | 指定文字顺时针旋转角度[0,360]，默认值：0，表示不旋转 | N |
| Body | fill | Int | 指定是否将文字水印铺满原图，1:铺满，0:不铺满，默认值:0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/file/download/watermark' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'bizType=isapi' \
--data-urlencode 'projectId=001' \
--data-urlencode 'fileId=K19978742-1' \
--data-urlencode 'saveOrNot=save' \
--data-urlencode 'text=水印测试' \
--data-urlencode 'site=se' \
--data-urlencode 'color=000000'
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
| operationUrls | Array | 水印图片下载URL列表 |
| newFileId | String | 存储文件的ID |
| expire | Long | 过期时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 入参错误 | 检查资源是否存在或入参 |
| 500 | 操作失败 | 请检查传递参数进行重试，如还是服务错误请联系客服 |