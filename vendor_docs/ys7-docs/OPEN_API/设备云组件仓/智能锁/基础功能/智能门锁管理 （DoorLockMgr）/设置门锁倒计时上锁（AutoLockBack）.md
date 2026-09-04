# 设置门锁倒计时上锁（AutoLockBack）

> 更新时间: 2026-06-17T18:11:15.000+08:00

> 文档ID: 4048 | 来源树: OPEN_API

---

## 设置门锁倒计时上锁（AutoLockBack）

- 接口功能

   倒计时上锁设置接口，适配Z5000FVS系列设备，支持托管和子账号，权限类型为设备级的CONFIG

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| header | accessToken | string | 用户访问令牌 | Y |
| header | deviceSerial | string | 设备序列号 | Y |
| body | localIndex | string | 资源序号 | Y |
| body | resourceCategory | string | 资源种类，描述资源的类型 | Y |
| body | domainIdentifier | string | 功能点领域，填写报备时的属性所在领域 | Y |
| body | propIdentifier | string | 功能点标识，填写报备时的属性标识符 | Y |
| body | enabled | string | 自动回锁使能开关 true-开false-关 | Y |
| body | lockBackTime | string | 自动回锁时间，单位：秒 取值范围[1,60] | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: DEVICE_SERIAL' \
--header 'Content-Type: application/json' \
--data-raw '{"localIndex":"value", "resourceCategory":"value", "domainIdentifier":"value", "propIdentifier":"value", "enabled":"value", "lockBackTime":"value"}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| meta | object | 响应信息 |
| -code | int | 响应码 |
| -message | string | 响应码说明 |
| -moreInfo | object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10031 | 账号无权限访问此设备 |  |
| 20007 | 设备不在线 |  |
| 20018 | 该用户不拥有该设备 |  |