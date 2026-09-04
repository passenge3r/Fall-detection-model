# API-设备云组件仓-人脸车辆抓拍机-修改小区信息

> 更新时间: 2026-06-30T12:07:57.000+08:00

> 文档ID: 1682 | 来源树: OPEN_API

---

## 修改小区信息

- 接口功能

   修改小区的位置信息及小区名称、物业联系人姓名信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/community/update`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | id | String | 小区id | Y |
| body | province | String | 省 | Y |
| body | city | String | 市 | Y |
| body | district | String | 区 | Y |
| body | street | String | 街道 | Y |
| body | address | String | 详细信息 | Y |
| body | name | String | 小区名称 | Y |
| body | estateManager | String | 物业联系人姓名 | Y |
| body | gpsLatitude | String | gps纬度 | Y |
| body | gpsLongitude | String | gps经度 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/aicamera/community/update' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'id=小区id' \
--data-urlencode 'province=浙江省' \
--data-urlencode 'city=杭州市' \
--data-urlencode 'district=滨江区' \
--data-urlencode 'street=西兴街道' \
--data-urlencode 'address=6幢1001室' \
--data-urlencode 'name=小区名称' \
--data-urlencode 'estateManager=物业联系人姓名' \
--data-urlencode 'gpsLatitude=gps纬度' \
--data-urlencode 'gpsLongitude=gps经度'
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