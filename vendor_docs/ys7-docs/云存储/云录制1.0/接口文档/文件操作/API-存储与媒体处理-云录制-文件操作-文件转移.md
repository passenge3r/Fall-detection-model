# API-存储与媒体处理-云录制-文件操作-文件转移

> 更新时间: 2026-06-30T17:52:18.000+08:00

> 文档ID: 1379 | 来源树: 云存储

---

## 文件转移

- 接口功能

   文件转移接口，将文件转移到其他项目空间。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/file`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Body | fileId | String | 文件ID，项目下文件的唯一标识，需输入已录制的文件ID | Y |
| Body | newProjectId | String | 要转移到的新项目ID | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/file' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'projectId=001' \
--data-urlencode 'fileId=wodewenjian' \
--data-urlencode 'newProjectId=002'
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

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |