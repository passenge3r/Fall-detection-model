# API-设备云组件仓-人脸车辆抓拍机-新增人员信息	

> 更新时间: 2026-06-30T12:10:02.000+08:00

> 文档ID: 1690 | 来源树: OPEN_API

---

## 新增人员信息

- 接口功能

   新增人员信息，具体信息包括人员编号、姓名、年龄、性别以及所属的小区

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/people/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | peopleNo | String | 人员编号 | Y |
| body | peopleName | String | 人员姓名 | Y |
| body | peopleAge | Int | 年龄 | Y |
| body | peopleGender | Int | 性别，0-女，1-男 | Y |
| body | communityId | String | 小区id | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/aicamera/people/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'peopleNo=000010' \
--data-urlencode 'peopleName=张三' \
--data-urlencode 'peopleAge=29' \
--data-urlencode 'peopleGender=1' \
--data-urlencode 'communityId=21befc41c31f4811ac8cf297d1b7618f'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": "0372b4a5378741acbd887200a2ed4780"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | String | 新增人员的人员id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |