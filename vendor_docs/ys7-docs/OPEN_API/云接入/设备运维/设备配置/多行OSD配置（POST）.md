# 多行OSD配置（POST）

> 多行OSD配置（POST）

> 更新时间: 2026-06-11T14:52:24.000+08:00

> 文档ID: 5201 | 来源树: OPEN_API

---

## 多行OSD配置

- 接口功能

   多行OSD配置。托管/子账号：支持。权限：设备级Config。

- 请求地址

`https://open.ys7.com/api/v3/device/osd/multi/set`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | channelNo | String | 设备通道号，默认为1 | N |
| body | osdNames | String | OSD内容，多个OSD内容用英文逗号[,]隔开 | N |

- 请求示例

```
curl -X POST 'https://open.ys7.com/api/v3/device/osd/multi/set' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=BH6581041' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'osdNames=OSD名称,省级,地市,县市区,乡镇,地点信息'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "操作成功",
    "moreInfo": null
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta |
| meta.code | Int | code |
| meta.message | String | message |
| meta.moreInfo | Object | moreInfo |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 10002 | accessToken过期或异常 | 请重新获取accessToken |
| 10031 | 账号无权限访问此设备 | 请确认账号拥有该设备权限 |
| 20007 | 设备不在线 | 请确认设备在线后重试 |
| 20002 | 设备不存在 | 请检查设备序列号是否正确 |
| 20011 | 设备不支持或者设备异常 | 请确认设备支持该功能 |
| 20008 | 设备响应超时 | 请稍后重试 |
| 60020 | 设备不支持该信令 | 请确认设备支持该信令 |
| 20006 | 网络异常 | 请检查网络连接后重试 |