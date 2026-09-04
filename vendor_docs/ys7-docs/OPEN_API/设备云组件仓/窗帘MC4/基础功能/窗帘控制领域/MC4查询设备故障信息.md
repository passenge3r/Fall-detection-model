# MC4查询设备故障信息

> 更新时间: 2026-06-25T14:25:16.000+08:00

> 文档ID: 2019 | 来源树: OPEN_API

---

## MC4查询设备故障信息

- 接口功能

   查询MC4窗帘电机设备故障信息

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 用户访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | Int | 资源描述，描述资源类型下的序号，示例：0 | Y |
| header | resourceCategory | String | 资源种类，描述资源的类型，示例：Curtain | Y |
| header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，示例：CurtainCtrl | Y |
| header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，示例：Fault | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: BG9859941' \
--header 'localIndex: 0' \
--header 'resourceCategory: Curtain' \
--header 'domainIdentifier: CurtainCtrl' \
--header 'propIdentifier: Fault'
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
  },
  "data": {
    "faultCode": 0
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数 |
| data.faultCode | Int | 故障码，0x0000正常，0x0001~0xFFFF工作异常，范围[0,65535] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 操作成功 |