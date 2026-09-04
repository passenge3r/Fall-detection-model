# 设备云组件-API-无感睡眠仪-每周、月、年心率统计：根据时间范围、时间区间统计心率

> 更新时间: 2026-06-25T20:31:51.000+08:00

> 文档ID: 1840 | 来源树: OPEN_API

---

## 每周、月、年心率统计：根据时间范围、时间区间统计心率

- 接口功能

   根据时间范围、时间区间统计每周、月、年心率

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/hearts`

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
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/hearts?deviceId=1658712676529897474&dateFormat=DAY&startDate=2023-05-17&endDate=2023-05-19' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {
        "dailyList": [
            {
                "avg": 68.646570000,
                "max": 78,
                "min": 55,
                "anomaly": 0.00,
                "ts": "2023-05-17"
            }
        ],
        "deviceId": "1658712676529897474",
        "avg": 68.56184,
        "max": 79,
        "min": 55,
        "count": 158,
        "highCount": 0,
        "lowCount": 0,
        "lowHighCount": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| avg | Float | 心率平均值 |
| count | Int | 总测量次数 |
| max | Int | 心率最大值 |
| min | Int | 心率最小值 |
| deviceId | String | 设备id |
| highCount | Int | 极高心率次数，极高心率≥160bpm |
| lowCount | Int | 极低心率次数，极低心率＜45bpm |
| lowHighCount | Int | 不规则心率次数，在统计维度范围内既有极高心率又有极低心率 |
| dailyList | Array<Object> | 心率统计数据集 |
| --avg | Float | 平均心率 |
| --max | Int | 最大心率 |
| --min | Int | 最小心率 |
| --anomaly | Float | 异常心率 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |