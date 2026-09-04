# 设备云组件-API-无感睡眠仪-每周、月、年睡眠统计：根据时间范围、时间区间统计睡眠质量

> 更新时间: 2026-06-25T20:31:58.000+08:00

> 文档ID: 1843 | 来源树: OPEN_API

---

## 每周、月、年睡眠统计：根据时间范围、时间区间统计睡眠质量

- 接口功能

   根据时间范围、时间区间统计每周、月、年睡眠质量

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/sleep`

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
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/sleep?deviceId=1659395903666028545&dateFormat=DAY&startDate=2023-05-20&endDate=2023-05-22' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {
        "deviceId": "1659395903666028545",
        "list": [
            {
                "stages": {
                    "MIDDLE": 0,
                    "LIGHT": 9150.0000,
                    "DEEP": 7050.0000,
                    "WAKEFUL": 3660.0000,
                    "UNKNOWN": 0
                },
                "ts": "2023-05-20"
            }
        ],
        "items": [
            {
                "name": "平均睡眠时长",
                "value": 33440.0,
                "referenceMax": 36000,
                "referenceMin": 21600,
                "unit": "小时"
            },
            {
                "name": "平均浅睡比例",
                "value": 0.21,
                "referenceMax": 55,
                "unit": "%"
            },
            {
                "name": "平均深睡比例",
                "value": 0.20,
                "referenceMax": 60,
                "referenceMin": 20,
                "unit": "%"
            }
        ]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| deviceId | String | 唯一id |
| items | Array<Object> | 睡眠统计指标数据集 |
| --name | String | 指标名称 |
| --value | Float | 值 |
| --referenceMax | Int | 上限参考值 |
| --referenceMin | Int | 下限参考值 |
| --unit | String | 单位 |
| list | Array<Object> | 睡眠质量统计数据集 |
| --stages | Object | 睡眠状态时长统计 |
| ---LIGHT | Float | 浅睡时长 |
| ---DEEP | Float | 深睡时长 |
| ---WAKEFUL | Float | 清醒时长 |
| ---UNKNOWN | Float | 未知 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |