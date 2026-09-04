# API-设备云组件-安全帽-获取单个设备信息

>  

> 更新时间: 2026-06-30T17:56:30.000+08:00

> 文档ID: 1479 | 来源树: OPEN_API

---

## 获取单个设备信息

- 接口功能

查询用户下指定设备的基本信息。其中，针对安全帽相机（DS-MCH208），支持查询设备序列号、设备名称等。接口分类：平台能力。

- 请求地址

`https://open.ys7.com/api/lapp/device/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/info' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734222'
```

- 返回数据

更详细内容请参考 <https://open.ys7.com/help/672>

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 设备信息 |
| code | String | 状态码，200表示成功 |
| msg | String | 状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |