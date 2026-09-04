# 设备云组件-API-无感睡眠仪-每日睡眠统计：获取统计分析睡眠质量

> 更新时间: 2026-06-25T20:31:55.000+08:00

> 文档ID: 1842 | 来源树: OPEN_API

---

## 每日睡眠统计：获取统计分析睡眠质量

- 接口功能

   获取每日统计分析睡眠质量

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/daily/sleep`

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
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/analysis/v1/devices/{deviceId}/daily/sleep?deviceId=1659395903666028545&date=2023-05-21' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {
        "deviceId": "1659395903666028545",
        "score": 55.62,
        "list": [
            {
                "stage": "LIGHT",
                "ts": "2023-05-21 23:30:00"
            }
        ],
        "items": [
            {
                "name": "睡眠时长",
                "value": 31380,
                "referenceMax": 36000,
                "referenceMin": 21600,
                "unit": "小时"
            },
            {
                "name": "浅睡比例",
                "value": 0.19,
                "referenceMax": 55,
                "unit": "%"
            },
            {
                "name": "深睡比例",
                "value": 0.28,
                "referenceMax": 60,
                "referenceMin": 20,
                "unit": "%"
            },
            {
                "name": "深睡连续性",
                "value": 47.41,
                "referenceMax": 100,
                "referenceMin": 70,
                "unit": "分"
            },
            {
                "name": "清醒次数",
                "value": 4,
                "referenceMax": 2,
                "referenceMin": 0,
                "unit": "次"
            }
        ]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| deviceId | String | 唯一id |
| score | Int | 评分 |
| items | Array<Object> | 睡眠统计指标数据集 |
| --name | String | 指标名称 |
| --value | Int | 值 |
| --referenceMax | Int | 上限参考值 |
| --referenceMin | Int | 下限参考值 |
| --unit | String | 单位 |
| list | Array<Object> | 睡眠质量统计数据集 |
| --stage | String | 睡眠状态 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |