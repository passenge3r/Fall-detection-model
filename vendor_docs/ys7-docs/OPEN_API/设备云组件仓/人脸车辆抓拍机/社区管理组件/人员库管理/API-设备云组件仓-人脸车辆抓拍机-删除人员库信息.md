# API-设备云组件仓-人脸车辆抓拍机-删除人员库信息

> 更新时间: 2026-06-30T12:09:59.000+08:00

> 文档ID: 1689 | 来源树: OPEN_API

---

## 删除人员库信息

- 接口功能

   删除人员库信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/delete`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | id | String | 人员库id | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/delete?id=5491684ca5794b819f9551ed6cf853fe' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": true
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | Boolean | 删除结果，true表示删除成功 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |