# 云点播-媒资管理-迁移视频文件（POST）

>  

> 更新时间: 2026-06-11T14:50:18.000+08:00

> 文档ID: 4954 | 来源树: 云存储

---

## 云点播-媒资管理-迁移视频文件

- 接口功能

   迁移视频文件到目标空间，支持保留或删除原文件

- 请求地址

`https://open.ys7.com/api/service/open/vod/file/transfer`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | newSpaceId | String | 目标空间ID | Y |
| body | fileNodeId | String | 文件节点ID | Y |
| body | fileName | String | 文件名称 | N |
| body | whetherRemainOrigin | Boolean | 是否保留原文件，true保留，false不保留 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/open/vod/file/transfer' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'newSpaceId=space_xxxxx' \
--data-urlencode 'fileNodeId=node_xxxxx' \
--data-urlencode 'fileName=video_001.mp4' \
--data-urlencode 'whetherRemainOrigin=true'
```

- 返回数据

```
{
    "data": {
        "fileNodeId": "node_xxxxx"
    },
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta.code | Int | 业务码，200表示成功 |
| meta.message | String | 响应信息 |
| meta.moreInfo | Object | 更多信息 |
| data.fileNodeId | String | 新文件节点ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请检查资源是否存在 |
| 500 | 服务器异常 | 服务器内部错误 |
| 400 | 参数错误 | 请检查请求参数格式 |