# 设置PIR检测区域

> 更新时间: 2026-06-30T12:11:23.000+08:00

> 文档ID: 1730 | 来源树: OPEN_API

---

## 设置PIR检测区域

- 接口功能

   设置PIR检测区域

- 请求地址

`https://open.ys7.com/api/v3/device/pir/set`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 设备通道号 | Y |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | area | String | 区域设置，如表顺序排列，每个值按位取值 例 [1,2,4,8,6] 则选中区域为序号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/pir/set' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: K69690868' \
--header 'localIndex: 1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'area=1,2'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示操作成功 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请求参数错误 |
| 10002 | accessToken过期或异常 | 令牌失效，需重新获取 |
| 20007 | 设备不在线 | 设备离线 |
| 20014 | deviceSerial无效 | 设备序列号无效 |
| 10031 | 账号无权限访问此设备 | 账号无权限 |
| 60012 | 未知错误 | 未知错误 |