# 设备云组件-API-无感睡眠仪-每日心率统计：根据日期统计当天每10分钟心率

> 更新时间: 2026-06-25T20:31:50.000+08:00

> 文档ID: 1839 | 来源树: OPEN_API

---

## 每日心率统计：根据日期统计当天每10分钟心率

- 接口功能

   根据日期统计当天每10分钟心率

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/daily/average/hearts`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceId | String | 设备ID | Y |
| query | date | String | 查询日期 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/daily/average/hearts?deviceId=1659395903666028545&date=2023-05-20' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {
        "avg": 0,
        "max": 0,
        "min": 0,
        "count": 0,
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
| minutesList | Array<Object> | 心率统计数据集 |
| --avg | Int | 心率平均值 |
| --max | Int | 心率最大值 |
| --min | Int | 心率最小值 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |