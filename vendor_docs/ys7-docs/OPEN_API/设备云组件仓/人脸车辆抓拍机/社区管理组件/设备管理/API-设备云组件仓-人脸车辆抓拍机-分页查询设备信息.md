# API-设备云组件仓-人脸车辆抓拍机-分页查询设备信息

> 更新时间: 2026-06-30T12:07:37.000+08:00

> 文档ID: 1678 | 来源树: OPEN_API

---

## 分页查询设备信息

- 接口功能

   分页查询设备的基本信息以及设备创建、修改、绑定区域的时间、在线状态、最近上线时间等信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/device/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | communityId | String | 小区id | Y |
| query | id | String | 分页offset，默认为空字符串 | N |
| query | pageSize | Int | 分页大小，默认为10，最大为50 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/aicamera/device/list?communityId=小区id&id=&pageSize=10' \
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
      "id": "ca93714d123e43b0beb823476c324b69",
      "deviceSerial": "L19165790",
      "gpsLatitude": "gpsLatitudeUpdate",
      "gpsLongitude": "gpsLongitudeUpdate",
      "bindTime": "2023-05-10 12:41:30",
      "communityId": "21befc41c31f4811ac8cf297d1b7618f",
      "updateTime": "2023-05-10 12:42:15",
      "createTime": "2023-05-10 12:41:30",
      "deviceName": "DS-2CD7A27EVWDV2-LZS/Q1(L19165790)",
      "status": 1,
      "regTime": "2023-05-10 12:30:34"
    },
    {
      "id": "186c868078af453a84a8f4a3eedb4ebe",
      "deviceSerial": "K73665963",
      "gpsLatitude": "gpsLatitude",
      "gpsLongitude": "gpsLongitude",
      "bindTime": "2023-05-08 20:19:15",
      "communityId": "21befc41c31f4811ac8cf297d1b7618f",
      "updateTime": "2023-05-08 20:19:14",
      "createTime": "2023-05-08 20:19:14",
      "deviceName": "DS-2CD7A27EWD-IZS(K73665963)",
      "status": 1,
      "regTime": "2023-05-10 12:30:46"
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
| data | Array | 设备信息列表 |
| data[].id | String | 主键id |
| data[].deviceSerial | String | 设备序列号 |
| data[].gpsLatitude | String | gps纬度 |
| data[].gpsLongitude | String | gps经度 |
| data[].bindTime | String | 绑定时间 |
| data[].communityId | String | 小区id |
| data[].updateTime | String | 修改时间 |
| data[].createTime | String | 创建时间 |
| data[].deviceName | String | 设备名称 |
| data[].status | Int | 设备在线状态，ONLINE为1，其他均为0 |
| data[].regTime | String | 最近上线时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |