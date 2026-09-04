# 设备云组件-API-无感睡眠仪-异常心率统计：根据时间范围，每10分钟为区间统计心率

> 更新时间: 2026-06-25T20:31:53.000+08:00

> 文档ID: 1841 | 来源树: OPEN_API

---

## 异常心率统计：根据时间范围，每10分钟为区间统计心率

- 接口功能

   根据时间范围，每10分钟为区间统计异常心率

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/anomaly/hearts`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceId | String | 设备ID | Y |
| query | dateFormat | String | 统计时间模式：SECOND=按秒统计；MINUTE=按分钟统计；HOUR=按小时统计；DAY=按天统计；MONTH=按月统计 | Y |
| query | startDate | String | 查询开始日期 | Y |
| query | endDate | String | 查询结束日期 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/anomaly/hearts?deviceId=1659395903666028545&dateFormat=DAY&startDate=2023-05-20&endDate=2023-05-22' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "page": "1",
    "pageSize": "20",
    "total": "1",
    "pageCount": "1",
    "data": [
        {
            "heartType": "LOW",
            "heartAvg": 48.55507,
            "heartMax": 68,
            "heartMin": 45,
            "ts": "2023-05-20 03:10:00"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | Int | 状态码，200表示成功 |
| message | String | 业务提示语 |
| total | String | 总记录数 |
| pageCount | String | 总页数 |
| page | String | 当前页码 |
| pageSize | String | 每一页的数目 |
| data | Array<Object> | 具体业务的数据对象 |
| --heartType | String | 异常心率类型，可用值：HIGH、LOW、LOW\_HIGH、NORMAL |
| --heartAvg | Float | 心率平均值 |
| --heartMax | Int | 心率最大值 |
| --heartMin | Int | 心率最小值 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |