# API-设备云组件仓-执法记录仪-远程巡检组件-统计与查询-事件统计查询

> 更新时间: 2026-07-09T13:42:46.000+08:00

> 文档ID: 749 | 来源树: OPEN_API

---

## 巡检事件统计查询

- 接口功能

   根据输入条件查询巡检事件信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/stats/event`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | N |
| Query | inspectDistrict | String | 巡检区域 | N |
| Query | inspectDistrictId | String | 巡检区域id | N |
| Query | inspectDistrictCode | String | 巡检区域标识，worksite-工地 ，worksite即为工地场景的标识 | N |
| Query | pageStart | Int | 查询起始索引，默认：0 | N |
| Query | pageSize | Int | 查询最大返回记录数，默认：100，最大：100 | N |
| Query | queryDate | String | 查询日期，格式：yyyy-MM-dd | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/stats/event?inspectDistrict=xxxxx&inspectDistrictId=xxxxx&inspectDistrictCode=xxxxx&pageStart=xxxxx&pageSize=xxxxx&queryDate=xxxxx' \
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
            "date": "2023-02-18",
            "eventType": "有人劫狱",
            "evidenceFileSource": "cloud_record",
            "evidenceFileStatus": "0",
            "evidenceFileErrorCode": "",
            "count": 1
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| data | Array<object> | data |
| inspectDistrict | String | 巡检区域 |
| evidenceFileStatus | String | 文件状态 |
| evidenceFileSource | String | 文件来源 |
| evidenceFileErrorCode | String | 文件上传错误码 |
| eventType | String | 事件类型 |
| deviceSerial | String | 设备序列号 |
| date | String | 统计日期 |
| count | Int | 事件统计数量 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |