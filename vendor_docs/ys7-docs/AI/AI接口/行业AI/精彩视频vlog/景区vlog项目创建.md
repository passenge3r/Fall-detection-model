# 景区vlog项目创建

> 更新时间: 2026-06-23T10:20:42.000+08:00

> 文档ID: 3976 | 来源树: AI

---

## 景区vlog项目创建

### 接口功能

- 景区vlog项目创建

### 请求地址

`https://open.ys7.com/api/service/open/scenic/spot/vlog/project`

### 请求方式

`POST`

### 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | projectId | String | 项目id，长度1-31 | Y |
| Body | projectName | String | 项目名称，长度1-256 | Y |

### 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/open/scenic/spot/vlog/project' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'projectId=182137project' \
--data-urlencode 'projectName=项目名称'
```

### 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": true
}
```

### 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应元数据 |
| meta.code | Int | 状态码 |
| meta.message | String | 状态描述 |
| meta.moreInfo | Object | 附加信息 |
| data | Boolean | 操作结果 |

### 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 400 | 参数错误 | 请求参数有误 |
| 500 | 服务器异常 | 服务器内部错误 |