# API-存储与媒体处理-云录制-图片二次处理-图片聚合视频

> API-存储与媒体处理-云录制-图片二次处理-图片聚合视频

> 更新时间: 2026-06-30T17:54:17.000+08:00

> 文档ID: 1397 | 来源树: 云存储

---

## 图片聚合视频

- 接口功能

   该接口用于新建图片聚合任务，将来源图片聚合生成视频。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/concentrate`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 用户访问凭证 | Y |
| body | files | Array | 来源图片信息，元素格式为 projectId&fileId，目前仅支持1000张图片；宽高必须为整数，以第一张图片为准，所有图片分辨率比例需要相同；不支持归档图片；不支持非图片；不支持超过2MB的图片；不支持png图片；否则即使下发成功，也无法生成成功；文件超过50张接口为投递模式，不返回文件合法性异常，请用户自行保证文件合法性 | Y |
| body | fps | Int | 帧率，范围 1-25 | Y |
| body | bitRate | Int | 码率，范围 30-500w | Y |
| body | projectId | String | 项目id | Y |
| body | fileId | String | 目标文件id | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/concentrate' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'files=default&ae89cc544c7d20b,default&0f10fd4b28ad339' \
--data-urlencode 'fps=1' \
--data-urlencode 'bitRate=100' \
--data-urlencode 'projectId=default' \
--data-urlencode 'fileId=123' \
--data-urlencode 'accessToken=at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| meta.code | Integer | 返回状态码，200表示成功 |
| meta.message | String | 返回状态描述 |
| data | Object | 响应内容 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |