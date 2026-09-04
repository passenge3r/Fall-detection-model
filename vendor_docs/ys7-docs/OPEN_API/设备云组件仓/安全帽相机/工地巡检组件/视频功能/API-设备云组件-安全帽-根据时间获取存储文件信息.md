# API-设备云组件-安全帽-根据时间获取存储文件信息

>  

> 更新时间: 2026-06-30T11:47:34.000+08:00

> 文档ID: 1491 | 来源树: OPEN_API

---

## 根据时间获取存储文件信息

- 接口功能

该接口用于根据时间获取存储文件信息。其中，针对安全帽相机（DS-MCH208），该设备支持云存储功能。接口分类：平台能力。

- 请求地址

`https://open.ys7.com/api/lapp/video/by/time`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 访问令牌 | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 通道号，非必选，默认为1 | N |
| body | startTime | Long | 起始时间，时间格式为：1378345128000，非必选，默认为当天0点 | N |
| body | endTime | Long | 结束时间，时间格式为：1378345128000，非必选，默认为当前时间 | N |
| body | recType | Int | 回放源，0-系统自动选择，1-云存储，2-本地录像，非必选，默认为0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/video/by/time' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=G12345678' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'startTime=1378345128000' \
--data-urlencode 'endTime=1378345128000' \
--data-urlencode 'recType=0'
```

- 返回数据

更详细内容参考 [https://open.ys7.com/help/660](https://open.ys7.com/help/6609)

- 返回字段

更详细内容参考 <https://open.ys7.com/help/660>

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |