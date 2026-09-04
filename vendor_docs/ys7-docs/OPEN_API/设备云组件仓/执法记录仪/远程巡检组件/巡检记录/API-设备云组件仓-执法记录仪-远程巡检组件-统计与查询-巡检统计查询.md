# API-设备云组件仓-执法记录仪-远程巡检组件-统计与查询-巡检统计查询

> 更新时间: 2026-07-09T13:42:49.000+08:00

> 文档ID: 750 | 来源树: OPEN_API

---

## 巡检统计查询

- 接口功能

   根据输入条件查询巡检记录信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/stats/inspect`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | N |
| Query | queryDate | String | 查询日期，格式：yyyy-MM-dd，默认查询前一天的数据 | N |
| Query | inspectDistrict | String | 巡检区域 | N |
| Query | inspectDistrictId | String | 巡检区域id | N |
| Query | inspectDistrictCode | String | 巡检区域标识，worksite-工地 ，worksite即为工地场景的标识 | N |
| Query | pageStart | Int | 查询起始索引，默认：0 | N |
| Query | pageSize | Int | 查询最大返回记录数，默认：100，最大：100 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/stats/inspect?queryDate=xxxxx&inspectDistrict=xxxxx&inspectDistrictId=xxxxx&inspectDistrictCode=xxxxx&pageStart=xxxxx&pageSize=xxxxx' \
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
    "data": [
        {
            "deviceSerial": "889035619",
            "inspectDistrict": "测试区域",
            "inspectDistrictId": "测试区域",
            "inspectDistrictCode": "测试区域",
            "date": "2023-02-18",
            "inspectType": null,
            "inspectCount": 7,
            "maxInspectDuration": 152486,
            "minInspectDuration": 51083,
            "avgInspectDuration": 101784
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Array<object> | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误码描述 |
| data | Array<object> | data |
| deviceSerial | String | 设备序列号 |
| inspectDistrict | String | 巡检区域 |
| inspectDistrictId | String | 巡检区域id |
| inspectDistrictCode | String | 巡检区域标识 |
| date | String | 巡检日期 |
| inspectType | String | 巡检类型 |
| inspectCount | Int | 巡检次数 |
| maxInspectDuration | Int | 最长巡检时间 |
| minInspectDuration | Int | 最小巡检时间 |
| avgInspectDuration | Int | 平均巡检时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |