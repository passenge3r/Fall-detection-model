# NVR设备隐藏IPC

> 更新时间: 2026-06-25T20:31:27.000+08:00

> 文档ID: 1815 | 来源树: OPEN_API

---

## NVR设备隐藏IPC

- 接口功能

   显示或者隐藏NVR下的通道

- 请求地址

`https://open.ys7.com/api/open/device/camera/limit`

- 请求方式

`POST`

- 子账户token请求所需最小权限

`"Permission":"config" "Resource":"dev:序列号"`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | channelNo | String | 通道号 | Y |
| body | enable | Int | 通道状态，1:显示，0:隐藏 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/open/device/camera/limit' \
--header 'accessToken: at.xxxxx' \
--data-raw 'deviceSerial=xxx&channelNo=1&enable=1'
```

- 返回数据

```
{"code":"string","msg":"string"}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 响应码值 |
| msg | String | 码值描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10031 | 子账户或萤石用户没有权限 |  |
| 20015 | 设备不支持该功能 |  |
| 20018 | 该用户不拥有该设备 |  |
| 10002 | accessToken过期或异常 |  |