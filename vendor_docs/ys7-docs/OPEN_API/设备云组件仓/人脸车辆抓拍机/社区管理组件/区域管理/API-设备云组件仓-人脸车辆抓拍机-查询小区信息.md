# API-设备云组件仓-人脸车辆抓拍机-查询小区信息

> 更新时间: 2026-06-30T12:09:42.000+08:00

> 文档ID: 1684 | 来源树: OPEN_API

---

## 查询小区信息

- 接口功能

   查询小区的名称、地理位置、物业联系人、创建及修改时间等信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/community/info`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | id | String | 小区id | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/community/info?id=小区id' \
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
    "id": "14d9757920cf4b1395b0a6241e25ab18",
    "province": "浙江省",
    "city": "杭州市",
    "district": "滨江区",
    "street": "西兴街道",
    "name": "绿城·晓风印月府Update",
    "address": "6幢1001室11Update",
    "estateManager": "物业负责人Update",
    "gpsLatitude": "gpsLatitudeUpdate",
    "gpsLongitude": "gpsLatitudeUpdate",
    "updateTime": "2023-04-24 11:31:08",
    "createTime": "2023-04-24 11:29:14"
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | Object | 小区信息 |
| data.id | String | 主键id |
| data.province | String | 省 |
| data.city | String | 市 |
| data.district | String | 区 |
| data.street | String | 街道 |
| data.name | String | 小区名称 |
| data.address | String | 详细信息 |
| data.estateManager | String | 物业联系人姓名 |
| data.gpsLatitude | String | gps纬度 |
| data.gpsLongitude | String | gps经度 |
| data.updateTime | String | 修改时间 |
| data.createTime | String | 创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |