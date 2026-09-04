# API-设备云组件仓-指纹锁-基础功能-启动指纹锁验证

> 更新时间: 2026-07-01T18:45:09.000+08:00

> 文档ID: 1351 | 来源树: OPEN_API

---

## 启动指纹锁验证

- 接口功能

   该接口用于启动指纹锁的本地验证。指纹锁设备直接调用[添加设备接口](https://open.ys7.com/help/54#device_option-api1)会返回错误，需先调用该接口启用本地验证（本地验证需要操作设备），再轮询调用[添加设备接口](https://open.ys7.com/help/54#device_option-api1)来关联指纹锁，该流程需在120s内完成。本节接口只支持萤石联网指纹门锁，[购买门锁](https://www.ys7.com/item/2056.html)。子账户token请求所需最小权限：Permission=Config，Resource=dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/local/verify`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/local/verify' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734203'
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
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20014 | deviceSerial不合法 | 检查设备序列号是否正确 |
| 20605 | 其他用户正在认证中 | 稍后重试 |
| 20609 | 设备响应超时，门锁通信故障或者电量不足，请重试 | 稍后重试 |
| 49999 | 数据异常 | 接口调用异常 |