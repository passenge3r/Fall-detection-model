# API-存储与媒体处理-云录制-项目操作-更新项目

> 更新时间: 2026-06-30T17:51:15.000+08:00

> 文档ID: 1365 | 来源树: 云存储

---

## 更新项目

- 接口功能

   更新项目存储信息。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/project/{projectId}`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Path | projectId | String | 项目ID，项目的唯一标识，限制字母数字和下划线，长度在32位以内 | Y |
| Query | accessToken | String | 用户令牌 | Y |
| Query | projectName | String | 项目名称 | Y |
| Query | expireDays | Int | 项目文件过期天数，0表示不过期；标准存储不输入默认30天，归档存储不输入默认60天，范围：0~36500天 | N |
| Query | storageType | Int | 项目存储类型，默认标准存储。1-标准存储，2-存档存储 | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/open/cloud/v1/project/111?accessToken=at.xxxxx&projectName=bao&expireDays=45&storageType=1'
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