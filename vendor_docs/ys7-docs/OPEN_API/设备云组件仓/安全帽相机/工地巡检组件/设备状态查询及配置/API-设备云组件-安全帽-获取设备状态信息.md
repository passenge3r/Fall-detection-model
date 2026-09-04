# API-设备云组件-安全帽-获取设备状态信息

>  

> 更新时间: 2026-06-30T17:57:14.000+08:00

> 文档ID: 1480 | 来源树: OPEN_API

---

## 获取设备状态信息

### 接口功能

该接口用于根据序列号通道号获取设备状态信息。其中，针对安全帽相机（DS-MCH208），支持隐私状态、告警声音模式、云存储状态等。接口分类：平台能力。

### 请求地址

https://open.ys7.com/api/lapp/device/status/get

### 请求方式

POST

### 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| body | channel | Int | 通道号，默认为1 | N |

### 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/status/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=DEVICE_SERIAL' \
--data-urlencode 'channel=1'
```

### 返回数据

更详细内容请参考 <https://open.ys7.com/help/1478>

### 返回字段

更详细内容请参考 <https://open.ys7.com/help/1478>

### 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | success | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20007 | Device off line | 设备不在线 |
| 20018 | The user doesn't own the device | 该用户不拥有该设备 |