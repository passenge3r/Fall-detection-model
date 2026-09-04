# MT2查询开合百分比

> 更新时间: 2026-06-23T17:33:46.000+08:00

> 文档ID: 2811 | 来源树: OPEN_API

---

## MT2查询开合百分比

- 接口功能

   查询窗帘当前开合百分比。支持托管及子账号，设备级，校验权限为Get。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 萤石开放API访问令牌 | Y |
| Header | Content-Type | String | application/json | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 资源序号，描述资源类型下的序号 | Y |
| Header | resourceCategory | String | 资源种类，描述资源的类型，固定值：Curtain | Y |
| Header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，固定值：CurtainCtrl | Y |
| Header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，固定值：OpeningClosingPercentage | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--header 'deviceSerial: {deviceSerial}' \
--header 'localIndex: 0' \
--header 'resourceCategory: Curtain' \
--header 'domainIdentifier: CurtainCtrl' \
--header 'propIdentifier: OpeningClosingPercentage'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "percent": 30
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，参见返回码说明 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| data | Object | 业务参数，详细说明见下表 |
| data.percent | Integer | 窗帘当前开合百分比，取值范围：0~100 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 10001 | 参数错误 | 参数错误 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 10031 | 账号无权限访问此设备 | 子账户或萤石用户没有权限 |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |
| 70018 | 资源不存在 | 资源不存在 |
| 50000 | 服务异常 | 服务异常 |