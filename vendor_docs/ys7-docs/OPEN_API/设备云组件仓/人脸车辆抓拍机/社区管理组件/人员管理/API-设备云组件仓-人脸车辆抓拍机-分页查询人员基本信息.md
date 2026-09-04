# API-设备云组件仓-人脸车辆抓拍机-分页查询人员基本信息

> 更新时间: 2026-06-30T12:10:12.000+08:00

> 文档ID: 1694 | 来源树: OPEN_API

---

## 分页查询人员基本信息

- 接口功能

   分页查询人员基本信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/people/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | pageSize | String | 分页大小，默认为10，最大为50 | N |
| query | communityId | String | 小区id | Y |
| query | id | String | 分页offset，默认为空字符串 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/people/list?communityId=21befc41c31f4811ac8cf297d1b7618f&pageSize=10&id=' \
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
            "peopleId": "0372b4a5378741acbd887200a2ed4780",
            "peopleNo": "000010",
            "updateTime": "2023-05-08 10:36:28",
            "createTime": "2023-05-08 10:34:57",
            "peopleName": "张三Update22",
            "peopleAge": 29,
            "peopleGender": 1,
            "communityId": "21befc41c31f4811ac8cf297d1b7618f"
        },
        {
            "peopleId": "59a53cf40cb64ec4adff3a855a71f574",
            "peopleNo": "000009",
            "updateTime": "2023-04-28 17:21:17",
            "createTime": "2023-04-28 17:21:17",
            "peopleName": "张三",
            "peopleAge": 18,
            "peopleGender": 0,
            "communityId": "21befc41c31f4811ac8cf297d1b7618f"
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
| data | Array | 人员基本信息列表 |
| data[].peopleId | String | 人员id |
| data[].peopleNo | String | 人员编号 |
| data[].updateTime | String | 修改时间 |
| data[].createTime | String | 创建时间 |
| data[].peopleName | String | 人员姓名 |
| data[].peopleAge | Int | 年龄 |
| data[].peopleGender | Int | 性别，0-女，1-男 |
| data[].communityId | String | 小区id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |