# API-存储与媒体处理-云录制-项目操作-更新项目下载流量限制

> 更新时间: 2026-06-30T17:51:43.000+08:00

> 文档ID: 1369 | 来源树: 云存储

---

## 更新项目下载流量限制接口

- 接口功能

   更新项目下载流量限制接口。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/project/limit/{projectId}`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Path | projectId | String | 项目ID，项目的唯一标识，限制字母数字和下划线，长度在32位以内 | Y |
| Query | accessToken | String | 用户令牌 | Y |
| Query | flowLimit | Long | 项目下载流量限制，单位：字节，-1代表不限制 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/open/cloud/v1/project/limit/111?accessToken=at.xxxxx&flowLimit=2024'
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