# API-存储与媒体处理-云录制-项目操作-删除项目

> API-存储与媒体处理-云录制-项目操作-删除项目

> 更新时间: 2026-05-25T16:37:20.000+08:00

> 文档ID: 1366 | 来源树: 云存储

---

## 删除项目

https://open.ys7.com/api/open/cloud/v1/project/{projectId}

接口名称：删除项目

接口描述：删除项目

### **请求**

**请求示例**

```
curl -X DELETE \
  'https://open.ys7.com/api/open/cloud/v1/project/333?accessToken=at.cz52cslwb2dpac9s8d2wmmri72d1lix6-5c09lw8s6k-1kzsoyd-zhwd78nlb' \
  -H 'Postman-Token: 30c1fb57-9b47-44cf-89ae-69324086d1fb' \
  -H 'cache-control: no-cache'
```

**请求方式**

DELETE

**请求头（header）**

此接口无此参数

**路径参数**

请用参数值代替路径中的{参数名称}

| 名称 | 数据类型 | 必须 | 描述 |
| --- | --- | --- | --- |
| projectId | string | 是 | 项目ID，项目的唯一标识，需输入已创建的项目ID |

**请求参数（params）**

| 名称 | 数据类型 | 必须 | 描述 |
| --- | --- | --- | --- |
| accessToken | string | 是 | 用户令牌 |

### **响应**

**响应头**

**响应体**

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

---

| 名称 | 数据类型 | 描述 |
| --- | --- | --- |
| meta | [MetaInfo](https://open.ys7.com/help/438#open_cloud_data-api1) | 返回状态码及信息 |

### **响应码解释**

| 错误码 | 错误描述 | 解决方案 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |