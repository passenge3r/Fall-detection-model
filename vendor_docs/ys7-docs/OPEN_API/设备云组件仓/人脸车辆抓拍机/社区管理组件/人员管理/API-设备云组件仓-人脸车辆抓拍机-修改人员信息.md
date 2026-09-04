# API-设备云组件仓-人脸车辆抓拍机-修改人员信息	

> 更新时间: 2026-06-30T12:10:05.000+08:00

> 文档ID: 1691 | 来源树: OPEN_API

---

## 修改人员信息

- 接口功能

   修改人员信息，可修改已添加人员的姓名、年龄以及性别信息，人员所属小区无法修改

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/people/update`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | peopleId | String | 人员id | Y |
| body | peopleName | String | 人员姓名 | Y |
| body | peopleAge | Int | 年龄 | Y |
| body | peopleGender | Int | 性别，0-女，1-男 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/aicamera/people/update' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'peopleId=0372b4a5378741acbd887200a2ed4780' \
--data-urlencode 'peopleName=张三' \
--data-urlencode 'peopleAge=29' \
--data-urlencode 'peopleGender=1'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |