# 睡眠伴侣EP-获取睡眠报告

> 更新时间: 2026-06-24T15:57:02.000+08:00

> 文档ID: 2097 | 来源树: OPEN_API

---

## 森思泰克睡眠仪-获取睡眠报告

- 接口功能

   森思泰克睡眠夜灯-获取睡眠报告

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/whst/sleepReport/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | startDate | String | 开始日期，格式：yyyy-MM-dd | Y |
| query | endDate | String | 结束日期，格式：yyyy-MM-dd | Y |
| query | deviceSerial | String | 设备序列号 | Y |
| query | zipResponse | Boolean | 压缩报告结构体，去除图表分期数据 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/whst/sleepReport/list?startDate=2023-11-22&endDate=2023-11-23&deviceSerial=xxxxxxxxxx&zipResponse=false' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "date": "2023-11-23",
            "reportStartTime": "2023-11-22 23:00:00",
            "reportEndTime": "2023-11-23 22:59:00",
            "sleepAnalysis": {
                "timeOutput": [
                    {"type": 1, "hour": 23, "minute": 54},
                    {"type": 3, "hour": 8, "minute": 38},
                    {"type": 2, "hour": 2, "minute": 50},
                    {"type": 4, "hour": 8, "minute": 38},
                    {"type": 5, "hour": 8, "minute": 44},
                    {"type": 6, "hour": 2, "minute": 56},
                    {"type": 7, "hour": 3, "minute": 57},
                    {"type": 8, "hour": 1, "minute": 52},
                    {"type": 9, "hour": 5, "minute": 49},
                    {"type": 10, "hour": 0, "minute": 0},
                    {"type": 11, "hour": 22, "minute": 58},
                    {"type": 12, "hour": 23, "minute": 0}
                ],
                "leaveBedCount": 0,
                "moveOutPut": {
                    "moveTimes": 36,
                    "moveTimePerHour": 4.1221375
                },
                "percentageOutPut": {
                    "awakePercentage": 33.587788,
                    "lightPercentage": 45.229008,
                    "deepPercentage": 21.183205,
                    "sleepPoint": 67
                },
                "resultCode": 0
            },
            "canBeRefreshed": false
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Array<Object> | 返回数据 |
| -date | String | 报告日期，格式：yyyy-MM-dd |
| -reportStartTime | String | 报告起始时间，yyyy-MM-dd HH:mm:ss |
| -reportEndTime | String | 报告结束时间，yyyy-MM-dd HH:mm:ss |
| -sleepAnalysis | Object | 睡眠报告 |
| --timeOutput | Array | 各项时间统计值，例如上床时间、深睡时长等；1=上床时刻,2=入睡时刻,3=醒来时刻,4=起床时刻,5=在床时长,6=清醒时长,7=浅睡时长,8=深睡时长,9=睡眠总时长,10=离床总时长,11=时间记录结束时刻,12=时间记录开始时刻 |
| --meanBreathFreqOutPut | Float | 平均呼吸频率 |
| --meanHeartFreqOutPut | Float | 平均心跳频率 |
| --leaveBedOutPut | Array | 各次离床的时间 |
| --leaveBedCount | Int | 离床次数 |
| --freqRecordOutput | Array | 呼吸心跳频率记录，5分钟记录一次，共有recordCount条数据，用于频率曲线绘制 |
| --recordCount | Int | 频率记录的次数 |
| --countBreathOutPut | Array | 各呼吸频率的出现次数,数组的第0~59位的数据分别表示呼吸频率0~59出现的次数 |
| --countHeartOutPut | Array | 各心跳频率的出现次数,数组的第0~149位的数据分别表示心跳频率0~149出现的次数 |
| --moveOutPut | String | 体动情况 |
| --percentageOutPut | String | 深睡、浅睡、清醒百分比、睡眠打分 |
| --classifyResult | String | 各时刻的分期结果和分期指数 |
| --minNumOutPut | Int | 输出的时刻数 |
| --sleepProblem | Array | 输出的睡眠问题，每1位代表1个问题，为0代表没有该问题，为1代表有该问题。 |
| --resultCode | Int | 0=正常；4001=报告可信度低（2h<=有效在床时间<4h）；4002=报告可信度无效（有效在床时间<2h） |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码200 |
| 500 | 服务器异常 | HTTP状态码500 |
| 400 | 参数错误 | HTTP状态码400 |