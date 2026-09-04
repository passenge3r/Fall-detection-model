# API-云接入-通用设备管理-设备管理-修改云端设备名称

> 更新时间: 2026-07-09T18:39:21.000+08:00

> 文档ID: 667 | 来源树: OPEN_API

---

## 修改云端设备名称

- 接口功能

   修改设备名称 子账户token请求所需最小权限："Permission":"Update" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/lapp/device/name/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | deviceName | String | 设备名称，长度不大于50字节，不能包含特殊字符 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/name/update' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'deviceName=xxxxx'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 响应结果状态码 |
| msg | String | 响应提示说明 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |