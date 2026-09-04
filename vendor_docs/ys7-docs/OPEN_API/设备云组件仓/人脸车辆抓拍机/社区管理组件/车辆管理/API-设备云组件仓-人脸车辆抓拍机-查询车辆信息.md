# API-设备云组件仓-人脸车辆抓拍机-查询车辆信息

> 更新时间: 2026-06-30T11:55:17.000+08:00

> 文档ID: 1622 | 来源树: OPEN_API

---

## 车辆信息查询

- 接口功能

   车辆信息查询，获取车牌颜色、类型、车身颜色、车辆品牌等信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/vehicle/info`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | communityId | String | 车辆所属小区id | Y |
| query | plateNumber | String | 车牌号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/vehicle/info?communityId=21befc41c31f4811ac8cf297d1b7618f&plateNumber=浙A·00006' \
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
        "id": "6e4bb8cde80e4b419f11e39797e9504e",
        "plateNumber": "浙A·00006",
        "plateColor": "蓝色",
        "vehicleType": "小型汽车",
        "vehicleColor": "黑色",
        "vehicleLogo": "奥迪",
        "vehicleLabel": "A6",
        "communityId": "21befc41c31f4811ac8cf297d1b7618f",
        "updateTime": "2024-01-01 12:00:00",
        "createTime": "2024-01-01 12:00:00"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| data | Object | 服务响应 |
| data.id | String | 车辆id |
| data.plateNumber | String | 车牌号 |
| data.plateColor | String | 车牌颜色 |
| data.vehicleType | String | 车辆类型 |
| data.vehicleColor | String | 车身颜色 |
| data.vehicleLogo | String | 车辆品牌 |
| data.vehicleLabel | String | 车辆标签 |
| data.communityId | String | 车辆所属小区id |
| data.updateTime | String | 修改时间 |
| data.createTime | String | 创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |