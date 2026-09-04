# API-设备云组件仓-探测器-基础功能-删除探测器

> 更新时间: 2026-07-01T18:43:55.000+08:00

> 文档ID: 1314 | 来源树: OPEN_API

---

## 删除探测器

- 接口功能

   该接口用于删除设备下关联的探测器（需要设备支持远程删除探测器）。子账户token请求所需最小权限："Permission":"Config"，"Resource":"dev:序列号"。

- 请求地址

`https://open.ys7.com/api/lapp/detector/delete`

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
curl --location --request POST 'https://open.ys7.com/api/lapp/detector/delete' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=569262222' \
--data-urlencode 'detectorSerial=604216666'
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
| 60020 | 不支持该命令 | 设备不支持远程删除探测器 |