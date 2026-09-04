# API-设备云组件仓-执法记录仪-远程巡检组件-巡检设备管理-更新巡检设备

> 更新时间: 2026-07-09T13:42:02.000+08:00

> 文档ID: 742 | 来源树: OPEN_API

---

## 更新巡检设备

- 接口功能

更新与区域关联的巡检设备信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | accessToken，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | inspectDistrict | String | 巡检区域 | N |
| Body | inspectDistrictId | String | 巡检区域id | Y |
| Body | inspectDistrictCode | String | 巡检区域标识，worksite-工地 ，worksite即为工地场景的标识 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/bodycamera' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'inspectDistrict=xxxxx' \
--data-urlencode 'inspectDistrictId=xxxxx' \
--data-urlencode 'inspectDistrictCode=xxxxx'
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
| code | Int | 错误码 |
| message | String | 错误描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |