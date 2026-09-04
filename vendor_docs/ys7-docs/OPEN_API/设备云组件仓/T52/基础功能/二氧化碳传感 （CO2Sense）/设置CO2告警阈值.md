# 设置CO2告警阈值

> 更新时间: 2026-06-25T14:21:13.000+08:00

> 文档ID: 1954 | 来源树: OPEN_API

---

## 设置CO2告警阈值

- 接口功能

   设置CO2告警阈值（通过OTAP协议设置设备的CO2告警阈值属性）

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | Integer | 资源描述，描述资源类型下的序号，如0 | Y |
| Header | resourceCategory | String | 资源种类，描述资源的类型，如global | Y |
| Header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，如CO2Sense | Y |
| Header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，如CO2AlarmThreshold | Y |
| Body | maxCO2 | Integer | 最大浓度，范围[0,100] | N |
| Body | minCO2 | Integer | 最小浓度，范围[0,100] | N |
| Body | enabled | Boolean | 告警使能 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: [设备序列号]' \
--header 'localIndex: 0' \
--header 'resourceCategory: global' \
--header 'domainIdentifier: CO2Sense' \
--header 'propIdentifier: CO2AlarmThreshold' \
--data-raw '{"maxCO2": 0, "minCO2": 0, "enabled": true}'
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
| 10001 | 请求参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 49999 | 数据异常 | 接口调用异常 |