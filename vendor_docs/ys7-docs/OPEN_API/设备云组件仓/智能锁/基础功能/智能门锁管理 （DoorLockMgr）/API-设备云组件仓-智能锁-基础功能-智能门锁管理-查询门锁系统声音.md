# API-设备云组件仓-智能锁-基础功能-智能门锁管理-查询门锁系统声音

> 更新时间: 2026-07-09T13:46:06.000+08:00

> 文档ID: 805 | 来源树: OPEN_API

---

## 查询门锁系统声音

- 接口功能

   该接口用于查询门锁系统声音。本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁，其余型号不保证可用。如下接口调用需要联系萤石配置白名单，否则接口可能调用报错。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/DoorLockMgr/DoorLockSystemSound`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/DoorLockMgr/DoorLockSystemSound' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "sound": 0,
        "keyTone": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数 |
| data.sound | Integer | 提示音，0-静音，1-低音，2-中音，3-高音，4-自动 |
| data.keyTone | Integer | 按键音，0-静音，1-低音，2-中音，3-高音，4-自动 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 2003 | 设备不在线 |  |
| 10001 | 请求参数异常 |  |
| 10002 | 请求参数异常 |  |
| 50000 | 服务器异常 | 可提交“工单”解决相关问题 |
| 400 | 请求参数错误 |  |