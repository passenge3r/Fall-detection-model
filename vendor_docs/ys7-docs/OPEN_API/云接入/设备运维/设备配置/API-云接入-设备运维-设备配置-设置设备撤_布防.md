# API-云接入-设备运维-设备配置-设置设备撤/布防

> API-云接入-设备运维-设备配置-设置设备撤/布防

> 更新时间: 2026-06-09T13:54:47.000+08:00

> 文档ID: 701 | 来源树: OPEN_API

---

## 设置设备撤/布防

- 接口功能

  对设备布撤防状态进行修改（活动检测开关），实现布防和撤防功能，该接口需要设备支持能力集：support\_defence
- 请求地址

  `https://open.ys7.com/api/lapp/device/defence/set`
- 请求方式

  `POST`
- 子账户token请求所需最小权限

  `"Permission":"Config"` `"Resource":"Cam:序列号:通道号"`
- 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| accessToken | String | 授权过程获取的access\_token | Y |
| deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| isDefence | int | 具有防护能力设备布撤防状态：0-睡眠，8-在家，16-外出，普通IPC设备布撤防状态：0-撤防，1-布防 | Y |

- HTTP请求报文

```
POST /api/lapp/device/defence/set HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

accessToken=at.20h863523v1zfck75qgmwhoy7vl2teqp&deviceSerial=427734888&isDefence=1
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |