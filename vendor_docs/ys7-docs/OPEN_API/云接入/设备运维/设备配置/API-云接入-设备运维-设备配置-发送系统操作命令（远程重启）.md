# API-云接入-设备运维-设备配置-发送系统操作命令（远程重启）

>  

> 更新时间: 2026-06-30T11:48:01.000+08:00

> 文档ID: 1532 | 来源树: OPEN_API

---

## 发送系统操作命令

- 接口功能

   发送系统操作命令。

- 请求地址

`https://open.ys7.com/api/v3/device/systemOperate`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 局部资源标识 | N |
| body | systemOperation | String | 系统级操作命令，SHUTDOWN：关机，REBOOT：重启，RESET：重置。并不是所有设备都支持所有的系统级操作命令，需要看实际操作的设备 | Y |
| body | delay | Int | 延迟多久，时间单位分钟，默认是0，最大为15，超过15的按照15计算 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/systemOperate' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G12345678' \
--header 'Content-Type: application/json' \
--data-raw '{"systemOperation":"REBOOT","delay":0}'
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
| meta | Object | 服务响应信息 |
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