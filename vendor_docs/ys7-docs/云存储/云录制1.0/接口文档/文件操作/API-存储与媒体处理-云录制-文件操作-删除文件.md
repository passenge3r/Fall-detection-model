# API-存储与媒体处理-云录制-文件操作-删除文件

> 更新时间: 2026-06-30T17:52:16.000+08:00

> 文档ID: 1378 | 来源树: 云存储

---

## 删除文件

- 接口功能

   删除文件。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Query | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/open/cloud/v1/file?accessToken=at.xxxxx&fileId=7d2d79ba6f8e499dbcaa13b6b4a00154&projectId=001'
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
| meta.code | Int | 返回码 |
| meta.message | String | 返回信息 |
| meta.moreInfo | Object | 其他信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |