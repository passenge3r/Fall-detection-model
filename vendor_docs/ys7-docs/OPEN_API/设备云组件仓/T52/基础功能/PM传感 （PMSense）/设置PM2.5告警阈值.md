# 设置PM2.5告警阈值

> 更新时间: 2026-06-25T14:21:00.000+08:00

> 文档ID: 1950 | 来源树: OPEN_API

---

## 设置PM2.5告警阈值

- 接口功能

设置PM2.5告警阈值

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | Integer | 资源描述，描述资源类型下的序号，固定值0 | Y |
| Header | resourceCategory | String | 资源种类，描述资源的类型，固定值global | Y |
| Header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，固定值PMSense | Y |
| Header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，固定值PM2\_5AlarmThreshold | Y |
| Header | Content-Type | String | application/json | Y |
| Body | minPM2\_5 | Integer | 最小浓度，范围[0,100] | N |
| Body | maxPM2\_5 | Integer | 最大浓度，范围[0,100] | N |
| Body | enabled | Boolean | 告警使能 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: XXXXXXXXX' \
--header 'localIndex: 0' \
--header 'resourceCategory: global' \
--header 'domainIdentifier: PMSense' \
--header 'propIdentifier: PM2_5AlarmThreshold' \
--header 'Content-Type: application/json' \
--data-raw '{"minPM2_5":0,"maxPM2_5":100,"enabled":true}'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "成功",
    "moreInfo": {
      "deviceMeta": {
        "code": "0x00000000",
        "errorMsg": "Succeeded."
      }
    }
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请求参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 20001 | 设备不存在 | 请检查设备序列号是否正确 |
| 20002 | 设备不在线 | 请检查设备是否在线 |
| 20014 | 设备响应超时 | 请稍后重试 |