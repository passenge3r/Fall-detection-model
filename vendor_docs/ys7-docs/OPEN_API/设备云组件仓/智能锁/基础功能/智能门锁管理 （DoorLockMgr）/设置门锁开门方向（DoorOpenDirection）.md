# 设置门锁开门方向（DoorOpenDirection）

> 更新时间: 2026-06-17T18:04:40.000+08:00

> 文档ID: 4047 | 来源树: OPEN_API

---

## 设置门锁开门方向（DoorOpenDirection）

- 接口功能

   开门方向设置接口，适配Z5000FVS系列设备，支持托管和子账号，权限类型为设备级的CONFIG

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
| body | direction | string | 开门方向 left-左开right-右开。开门方向要和锁安装时的门把手开门方向保持一致，否则会出现门锁死的情况，慎重修改 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: XXXXXXX' \
--header 'deviceSerial: XXXXXX' \
--header 'localIndex: 0' \
--header 'resourceCategory: DoorLock' \
--header 'domainIdentifier: DoorLockMgr' \
--header 'propIdentifier: DoorOpenDirection' \
--header 'Content-Type: application/json' \
--data '{
	"direction": "left"
}'
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