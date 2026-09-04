# API-设备云组件仓-智能电梯网络摄像机-视频功能-根据时间获取存储文件信息

> 更新时间: 2026-06-30T11:54:22.000+08:00

> 文档ID: 1600 | 来源树: OPEN_API

---

## 根据时间获取存储文件信息

- 接口功能

   该接口用于根据时间获取存储文件信息。其中，针对安全帽相机（DS-MCH208），该设备支持云存储功能。

- 请求地址

`https://open.ys7.com/api/lapp/video/by/time`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 用户访问令牌 | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | N |
| body | channelNo | String | 通道号，普通摄像头默认为1，多通道设备可填实际通道号 | N |
| body | startTime | String | 本地录像/云存储录像回放开始时间，示例：2019-12-01 00:00:00 | N |
| body | stopTime | String | 本地录像/云存储录像回放结束时间，示例：2019-12-02 00:00:00 | N |
| body | recType | Int | 回放源，0-系统自动选择，1-云存储，2-本地录像，默认为0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/video/by/time' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734222' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'startTime=2019-12-01 00:00:00' \
--data-urlencode 'stopTime=2019-12-02 00:00:00' \
--data-urlencode 'recType=0'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功",
    "data": [
        {
            "deviceSerial": "427734222",
            "channelNo": 1,
            "startTime": 1575129600000,
            "stopTime": 1575216000000,
            "fileType": 1
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示操作成功 |
| msg | String | 返回信息描述 |
| data | Array | 存储文件信息列表 |
| data[].deviceSerial | String | 设备序列号 |
| data[].channelNo | Int | 通道号 |
| data[].startTime | Long | 录像开始时间（毫秒时间戳） |
| data[].stopTime | Long | 录像结束时间（毫秒时间戳） |
| data[].fileType | Int | 文件类型，1-云存储，2-本地录像 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 10002 | accessToken过期或异常 | 请重新获取accessToken |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |