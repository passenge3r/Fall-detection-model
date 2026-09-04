# API-云接入-通用设备管理-设备管理-NVR设备关联IPC

> 更新时间: 2026-07-09T18:39:26.000+08:00

> 文档ID: 669 | 来源树: OPEN_API

---

## NVR设备关联IPC

- 接口功能

   该接口用于NVR设备关联IPC 子账户token请求所需最小权限："Permission":"Config" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/device/ipc/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | ipcSerial | String | 待关联的IPC设备序列号 | Y |
| Body | channelNo | Int | 非必选参数，不为空表示给指定通道关联IPC，为空表示给通道1关联IPC | N |
| Body | validateCode | String | 非必选参数，IPC设备验证码，默认为空 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/ipc/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'ipcSerial=xxxxx' \
--data-urlencode 'validateCode='
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
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 未知错误 | 设备返回其他错误码 |
| 60020 | 不支持该命令 | 确认设备是否支持关联IPC |
| 60040 | 添加的设备不在同一局域网 |  |
| 60041 | 添加的设备被其他设备关联或响应超时 |  |
| 60042 | 添加的设备密码错误 |  |
| 60043 | 添加的设备超出最大数量 |  |
| 60044 | 添加的设备网络不可达超时 |  |
| 60045 | 添加的设备的IP和其他通道的IP冲突 |  |
| 60046 | 添加的设备的IP和本设备的IP冲突 |  |
| 60047 | 码流类型不支持 |  |
| 60048 | 带宽超出系统接入带宽 |  |
| 60049 | IP或者端口不合法 |  |
| 60050 | 添加的设备版本不支持需要升级才能接入 |  |
| 60051 | 添加的设备不支持接入 |  |
| 60052 | 添加的设备通道号出错 |  |
| 60053 | 添加的设备分辨率不支持 |  |
| 60054 | 添加的设备账号被锁定 |  |
| 60055 | 添加的设备取码流出错 | 检查IPC设备码流 |