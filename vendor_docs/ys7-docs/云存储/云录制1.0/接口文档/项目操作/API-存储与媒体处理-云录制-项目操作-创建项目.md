# API-存储与媒体处理-云录制-项目操作-创建项目

> 更新时间: 2026-07-01T18:45:20.000+08:00

> 文档ID: 1362 | 来源树: 云存储

---

## 创建项目

- 接口功能

   开发者创建项目。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/project/{projectId}`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Path | projectId | String | 项目ID，项目的唯一标识，限制字母数字和下划线，长度在32位以内 | Y |
| Body | accessToken | String | 用户令牌 | Y |
| Body | projectName | String | 项目名称，项目名称需要开发者在控制台自行创建，对应控制台的项目名称字段 | Y |
| Body | expireDays | Int | 项目文件过期天数，0表示不过期；标准存储不输入默认30天，归档存储不输入默认60天，范围：0~36500天 | N |
| Body | storageType | Int | 项目存储类型，默认标准存储。1-标准存储，2-存档存储 | N |
| Body | flowLimit | Long | 项目下载流量限制，单位：字节 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/cloud/v1/project/333' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'projectName=bao3' \
--data-urlencode 'expireDays=30' \
--data-urlencode 'storageType=1' \
--data-urlencode 'flowLimit=1024'
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