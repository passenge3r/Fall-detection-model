# API-设备云组件仓-T21智能人体存在传感器-基础功能-人形侦测-设置长时间停留检测自定义声音

> 更新时间: 2026-07-06T13:47:56.000+08:00

> 文档ID: 1120 | 来源树: OPEN_API

---

## 设置长时间停留检测自定义声音

- 接口功能

   该接口用于设置长时间停留检测自定义声音。本文档仅适用于设备型号 CS-T21-DG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/HumanDetection/LongStayCustomSound`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | sound | Integer | 自定义音效。取值范围[1,2,3,4,5,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]：1-叮咚，2-有人闯入，3-欢迎光临，4-请随手关门，5-请注意安全，20-微风，21-警告，22-叮，23-回声，24-退场，25-前进，26-激光，27-钢琴键，28-前奏，29-渐进，30-脉冲，31-叮咛，32-上课铃，33-激板，34-柔和，35-舒缓，36-滴答，37-按键音，38-振奋，39-圆舞曲 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/HumanDetection/LongStayCustomSound' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "sound": 1
}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "成功",
        "moreInfo": {
            "deviceMeta": {
                "code": "0x00000000",
                "errorMsg": "Succeeded."
            }
        }
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

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |