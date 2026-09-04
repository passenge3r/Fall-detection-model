# API-设备云组件仓-人脸车辆抓拍机-分页查询人员库信息

> 更新时间: 2026-06-30T12:09:53.000+08:00

> 文档ID: 1687 | 来源树: OPEN_API

---

## 分页查询人员库信息

- 接口功能

   分页查询人员库的信息，包括人员库ID、名称、类别、与其相关联小区ID及创建、修改时间

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | communityId | String | 小区id | Y |
| query | id | String | 分页offset，默认为空字符串 | Y |
| query | pageSize | Int | 分页大小，默认为10，最大为50 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/peopleCategory/list?communityId=21befc41c31f4811ac8cf297d1b7618f&id=&pageSize=10' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": [
        {
            "id": "5491684ca5794b819f9551ed6cf853fe",
            "name": "保洁类Update",
            "categories": "保洁Update",
            "communityId": "21befc41c31f4811ac8cf297d1b7618f",
            "updateTime": "2023-05-08 10:19:43",
            "createTime": "2023-05-08 10:19:12"
        },
        {
            "id": "780f3d940b9c4684922b7a517780c8dd",
            "name": "安保类",
            "categories": "安保",
            "communityId": "21befc41c31f4811ac8cf297d1b7618f",
            "updateTime": "2023-04-28 15:06:34",
            "createTime": "2023-04-28 15:06:34"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | Array | 人员库信息列表 |
| data[].id | String | 人员库id |
| data[].name | String | 人员库名称 |
| data[].categories | String | 人员库类别 |
| data[].communityId | String | 小区id |
| data[].updateTime | String | 修改时间 |
| data[].createTime | String | 创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |