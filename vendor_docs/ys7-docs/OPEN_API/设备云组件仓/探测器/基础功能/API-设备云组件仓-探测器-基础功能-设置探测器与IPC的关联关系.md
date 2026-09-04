# API-设备云组件仓-探测器-基础功能-设置探测器与IPC的关联关系

> 更新时间: 2026-07-01T18:44:04.000+08:00

> 文档ID: 1318 | 来源树: OPEN_API

---

## 设置探测器与IPC的关联关系

- 接口功能

   该接口用于设置设备关联的探测器与IPC设备的关联关系（需要设备支持告警联动功能）。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/detector/ipc/relation/set`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 网关设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | detectorSerial | String | 探测器序列号 | Y |
| Body | ipcSerial | String | IPC设备序列号 | Y |
| Body | operation | Int | 操作：0-删除，1-绑定 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/detector/ipc/relation/set' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=465538888' \
--data-urlencode 'detectorSerial=470289999' \
--data-urlencode 'ipcSerial=558815555' \
--data-urlencode 'operation=0'
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
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确或者操作失败 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持关联IPC功能 |