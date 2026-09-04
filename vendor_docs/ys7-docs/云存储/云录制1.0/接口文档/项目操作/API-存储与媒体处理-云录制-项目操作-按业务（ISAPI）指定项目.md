# API-存储与媒体处理-云录制-项目操作-按业务（ISAPI）指定项目

> 更新时间: 2026-06-30T17:51:33.000+08:00

> 文档ID: 1367 | 来源树: 云存储

---

## 按业务（ISAPI）指定项目

- 接口功能

   按业务（ISAPI）指定项目。

- 请求地址

`https://open.ys7.com/api/open/cloud/cloud/business`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 用户令牌 | Y |
| Body | bizType | String | 业务类型：ISAPI | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/cloud/business' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'bizType=ISAPI' \
--data-urlencode 'projectId=222'
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