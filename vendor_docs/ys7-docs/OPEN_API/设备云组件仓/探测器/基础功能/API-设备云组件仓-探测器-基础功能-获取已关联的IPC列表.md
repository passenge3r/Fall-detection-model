# API-设备云组件仓-探测器-基础功能-获取已关联的IPC列表

> 更新时间: 2026-07-01T18:44:02.000+08:00

> 文档ID: 1317 | 来源树: OPEN_API

---

## 获取已关联的IPC列表

- 接口功能

   该接口用于获取设备已关联的IPC设备列表（需要设备支持告警联动功能）。子账户token请求所需最小权限："Permission":"Get"，"Resource":"dev:序列号"。

- 请求地址

`https://open.ys7.com/api/lapp/detector/ipc/list/bind`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 网关设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | detectorSerial | String | 探测器序列号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/detector/ipc/list/bind' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=465538888' \
--data-urlencode 'detectorSerial=470289999'
```

- 返回数据

```
{
    "data": [
        {
            "detectorSerial": "470289999",
            "ipcSerial": "558815555"
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| data | Array | 已关联的IPC列表 |
| data[].detectorSerial | String | 探测器序列号 |
| data[].ipcSerial | String | 关联的IPC设备序列号 |

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
| 60020 | 不支持该命令 | 设备不支持关联IPC |