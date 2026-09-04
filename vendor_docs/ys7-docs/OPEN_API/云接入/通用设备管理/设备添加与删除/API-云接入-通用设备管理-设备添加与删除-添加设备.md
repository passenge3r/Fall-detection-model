# API-云接入-通用设备管理-设备添加与删除-添加设备

> 更新时间: 2026-07-09T18:39:05.000+08:00

> 文档ID: 661 | 来源树: OPEN_API

---

## 添加设备

- 接口功能

   添加设备到账号下

- 请求地址

`https://open.ys7.com/api/lapp/device/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | validateCode | String | 设备验证码，设备机身上的六位大写字母 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'validateCode=ABCDEF'
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
| 20002 | 设备不存在 | 该接口出现这个错误码表示设备未注册至萤石云 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20010 | 设备验证码错误 | 检查设备验证码是否错误 |
| 20011 | 设备添加失败 | 检查设备网络等是否正常 |
| 20013 | 设备已被别人添加 | 该设备已被别的账号添加 |
| 20014 | deviceSerial不合法 |  |
| 20017 | 设备已被自己添加 | 设备已经添加到该账号下 |
| 20038 | 设备token失效 |  |
| 49999 | 数据异常 | 接口调用异常 |
| 60066 | 海康设备不能使用出场时的默认验证码 | [本地更新验证码](https://statics.ys7.com/device/image/servicepic/16.png) |
| 60058 | 设备上线后未绑定状态需要确权才能添加 | 1、[设备确权接口](https://open.ys7.com/help/664)2、[确权快速操作](https://open.ys7.com/bbs/article/106) |
| 60034 | 禁止绑定设备，此类设备需要关联NVR使用 | 此设备不支持直连云服务，请将设备先关联到海康硬盘录像机 |
| 60085 | 设备冻结且存在高风险 | [设备确权接口](https://open.ys7.com/help/664) |
| 60086 | 设备存在高风险,需重启确权 | [设备确权接口](https://open.ys7.com/help/664) |