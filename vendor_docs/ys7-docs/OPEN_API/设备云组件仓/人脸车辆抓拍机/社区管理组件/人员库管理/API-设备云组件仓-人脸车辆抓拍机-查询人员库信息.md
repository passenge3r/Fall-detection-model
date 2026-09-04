# API-设备云组件仓-人脸车辆抓拍机-查询人员库信息

> 更新时间: 2026-06-30T12:09:57.000+08:00

> 文档ID: 1688 | 来源树: OPEN_API

---

## 查询人员库信息

- 接口功能

   查询人员库的信息，包括人员库名称、类别、相关联小区id、创建及修改时间

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/info`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | id | String | 人员库id | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/info?id=5491684ca5794b819f9551ed6cf853fe' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "id": "5491684ca5794b819f9551ed6cf853fe",
        "name": "保洁类Update",
        "categories": "保洁Update",
        "communityId": "21befc41c31f4811ac8cf297d1b7618f",
        "updateTime": "2023-05-08 10:19:43",
        "createTime": "2023-05-08 10:19:12"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | Object | 人员库信息 |
| data.id | String | 人员库id |
| data.name | String | 人员库名称 |
| data.categories | String | 人员库类别 |
| data.communityId | String | 小区id |
| data.updateTime | String | 修改时间 |
| data.createTime | String | 创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |