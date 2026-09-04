# 设备云组件-API-无感睡眠仪-每周、月呼吸率统计-根据时间范围、时间区间统计风险评估等级

> 更新时间: 2026-06-25T20:31:45.000+08:00

> 文档ID: 1837 | 来源树: OPEN_API

---

## 每周、月呼吸率统计：根据时间范围、时间区间统计风险评估等级

- 接口功能

   根据时间范围、时间区间统计每周、月呼吸率及风险评估等级

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/risk/breaths`

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
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/risk/breaths?deviceId=1659395903666028545&dateFormat=DAY&startDate=2023-05-19&endDate=2023-05-22' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {
        "list": [
            {
                "riskRank": "FREE",
                "ts": "2023-05-19"
            }
        ],
        "deviceId": "1659395903666028545",
        "riskRanks": {
            "MIDDLE": "0",
            "HIGH": "0",
            "LOW": "0",
            "FREE": "4",
            "UNKNOWN": "0"
        }
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| deviceId | String | 设备id |
| list | Array<Object> | 呼吸率统计数据集 |
| --riskRank | String | 睡眠呼吸风险评估等级：FREE=无风险；LOW=低风险；MIDDLE=中风险；HIGH=高风险，可用值：FREE、HIGH、LOW、MIDDLE、UNKNOWN |
| --ts | String | 时间戳 |
| riskRanks | Object | 睡眠呼吸风险评估统计集 |
| --MIDDLE | String | MIDDLE次数 |
| --HIGH | String | HIGH次数 |
| --LOW | String | LOW次数 |
| --FREE | String | FREE次数 |
| --UNKNOWN | String | UNKNOWN次数 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |