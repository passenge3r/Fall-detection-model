# API-存储与媒体处理-云录制-项目操作-单条查询ISAPI业务所指定的项目

> 更新时间: 2026-06-30T17:51:38.000+08:00

> 文档ID: 1368 | 来源树: 云存储

---

## 单条查询ISAPI业务所指定的项目

- 接口功能

   单条查询业务所指定的项目。

- 请求地址

`https://open.ys7.com/api/open/cloud/cloud/business`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | bizType | String | 业务类型：ISAPI | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/open/cloud/cloud/business?accessToken=at.xxxxx&bizType=ISAPI'
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
        "projectId": "222",
        "bizType": "ISAPI",
        "createTime": "2023-01-13T15:50:07",
        "updateTime": "2023-01-13T15:50:07"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 返回项目业务信息 |
| data.projectId | String | 项目ID |
| data.bizType | String | 业务类型 |
| data.createTime | String | 创建时间 |
| data.updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |