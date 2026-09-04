# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-查询区域信息

> 更新时间: 2026-06-30T11:55:19.000+08:00

> 文档ID: 1623 | 来源树: OPEN_API

---

## 查询区域信息

- 接口功能

   获取区域信息，区域是为了方便用户组织管理电梯提出来的概念，用户可根据业务需要创建区域，并将电梯与区域关联管理。

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/worksite/query`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | worksiteId | String | 区域id | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/worksite/query?worksiteId=b877b4bbbc734d4386d77beb85164766' \
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
        "worksiteName": "示例区域",
        "longitude": 120.21,
        "latitude": 30.21,
        "province": "浙江省",
        "city": "杭州市",
        "district": "滨江区",
        "street": "西兴街道",
        "worksiteRegion": "",
        "note": "",
        "createTime": "2024-01-01 12:00:00",
        "updateTime": "2024-01-01 12:00:00"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Object | 响应体 |
| data.worksiteName | String | 工地名称 |
| data.longitude | Float | 经度 |
| data.latitude | Float | 纬度 |
| data.province | String | 省 |
| data.city | String | 市 |
| data.district | String | 区 |
| data.street | String | 街道 |
| data.worksiteRegion | String | 所在区域 |
| data.note | String | 备注信息 |
| data.createTime | String | 创建时间 |
| data.updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |