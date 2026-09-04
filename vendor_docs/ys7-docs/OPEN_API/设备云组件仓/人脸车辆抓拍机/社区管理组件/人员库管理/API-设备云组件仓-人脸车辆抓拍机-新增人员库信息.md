# API-设备云组件仓-人脸车辆抓拍机-新增人员库信息

> 更新时间: 2026-06-30T12:09:44.000+08:00

> 文档ID: 1685 | 来源树: OPEN_API

---

## 新增人员库信息

- 接口功能

   新增人员库信息，包括人员库名称、类别及相关联的小区id，一个小区可对应多个人员库，用户可自定义人员库名称进行区分

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | name | String | 人员库名称 | Y |
| body | categories | String | 人员库类别 | Y |
| body | communityId | String | 小区id | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=人员库名称' \
--data-urlencode 'categories=人员库类别' \
--data-urlencode 'communityId=小区id'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "操作成功"
  },
  "data": "5491684ca5794b819f9551ed6cf853fe"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | String | 新增人员库的id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |