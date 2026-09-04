# API-设备云组件-CS-T33-BW红外遥控器-基础功能-绑定红码方案控制指定类型的电器

>  

> 更新时间: 2026-06-30T10:58:38.000+08:00

> 文档ID: 1527 | 来源树: OPEN_API

---

## 绑定红码方案控制指定类型的电器

- 接口功能

   绑定红码方案控制指定类型的电器。

- 请求地址

`https://open.ys7.com/api/v3/device/infrared/remote/bind`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| body | type | Int | 设备类型id | Y |
| body | subType | Int | 遥控器子类型，用于区分同一类型遥控器，目前仅空调会使用此字段 | N |
| body | brandId | Int | 遥控器品牌id | Y |
| body | remoteId | Int | 遥控器使用的红码id | Y |
| body | name | String | 遥控器的名称 | N |
| body | mode | Int | 0:常规下发，全包下发；1:分包下发，不传默认是0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/infrared/remote/bind' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G12345678' \
--header 'Content-Type: application/json' \
--data-raw '{"type":1,"subType":0,"brandId":247,"remoteId":6386,"name":"遥控器","mode":0}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object |  |
| meta.code | Int | 返回码 |
| meta.message | String | 返回消息 |
| meta.moreInfo | Object | 更多信息 |
| data | Object | 返回数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 100031 | 子账户或萤石用户没有权限 | http状态码403 |
| 20007 | 设备不在线 | http状态码412 |
| 20018 | 该用户不拥有该设备 | http状态码403 |
| 20032 | 该用户下通道不存在 | http状态码404 |
| 20040 | 查询设备开关状态失败 | http状态码404 |
| 21001 | 获取红码支持的类型不存在 | http状态码404 |
| 21002 | 根据类型查询红码品牌列表不存在 | http状态码404 |
| 21003 | 根据类型和品牌查询红码方案不存在 | http状态码404 |
| 21004 | 调用红码服务绑定红码方案控制指定类型的电器出现异常 | http状态码500 |
| 21005 | 调用红码服务解绑红码方案控制指定类型的电器出现异常 | http状态码500 |
| 50000 | 服务异常 | http状态码500 |