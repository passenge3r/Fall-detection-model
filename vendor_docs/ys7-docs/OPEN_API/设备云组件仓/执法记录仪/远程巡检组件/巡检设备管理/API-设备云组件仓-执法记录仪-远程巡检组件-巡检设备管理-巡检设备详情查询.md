# API-设备云组件仓-执法记录仪-远程巡检组件-巡检设备管理-巡检设备详情查询

> 更新时间: 2026-07-09T13:41:59.000+08:00

> 文档ID: 743 | 来源树: OPEN_API

---

## 查询巡检设备

- 接口功能

根据设备序列号查询巡检设备的详细信息，包括设备名称、巡检区域、巡检区域ID、巡检区域标识、设备在线状态与经纬度信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "deviceSerial": "L51049602",
        "deviceName": "设备名称",
        "inspectDistrict": "设备区域",
        "inspectDistrictId": "04eb9593f0dd4842a01d4b017fa25f1f",
        "inspectDistrictCode": "worksite",
        "status": 0,
        "latitude": 30.205653,
        "longitude": 120.215713
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| data | Object | 业务数据 |
| deviceSerial | String | 设备序列号 |
| deviceName | String | 设备名称 |
| inspectDistrict | String | 巡检区域 ，与这台设备相关联的工地区域 |
| inspectDistrictId | String | 巡检区域id |
| inspectDistrictCode | String | 巡检区域标识，worksite-工地 ，worksite即为工地场景的标识 |
| status | Int | 设备在线状态 0-不在线，1-在线 |
| latitude | Number | 纬度，例：30.205653 |
| longitude | Number | 经度，例：120.215713 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |