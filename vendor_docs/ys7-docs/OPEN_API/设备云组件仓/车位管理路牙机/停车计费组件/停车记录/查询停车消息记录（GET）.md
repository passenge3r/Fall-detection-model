# 查询停车消息记录（GET）

>  

> 更新时间: 2026-06-30T17:55:52.000+08:00

> 文档ID: 1473 | 来源树: OPEN_API

---

## 查询停车消息记录

- 接口功能

   查询停车消息记录。

- 请求地址

`https://open.ys7.com/api/service/devicekit/parking/msgRecord`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | accessToken | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| query | id | Int | 起始消息记录id，查出数据不包含该id | Y |
| query | pageSize | Int | 分页大小，小于50 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/parking/msgRecord?id=0&pageSize=10' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: K90123422'
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
            "msgId": 1,
            "deviceSerial": "K90123422",
            "msgType": 2,
            "msgTime": "2023-04-27 12:00:15",
            "picUrl": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "plateNumber": "",
            "confidence": 0.0
        },
        {
            "msgId": 3,
            "deviceSerial": "K90123422",
            "msgType": 2,
            "msgTime": "2023-04-27 12:30:21",
            "picUrl": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "plateNumber": "",
            "confidence": 0.0
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |
| data | Array<Object> | 消息记录列表 |
| data.msgId | Int | 消息id |
| data.deviceSerial | String | 设备序列号 |
| data.msgType | Int | 消息类型 1-入车记录，2-定时抓拍记录，3-出车记录 |
| data.msgTime | String | 消息时间 |
| data.picUrl | String | 图片地址 |
| data.plateNumber | String | 车牌号 |
| data.confidence | Int | 置信度 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 50000 | 服务器异常 | 服务器异常 |