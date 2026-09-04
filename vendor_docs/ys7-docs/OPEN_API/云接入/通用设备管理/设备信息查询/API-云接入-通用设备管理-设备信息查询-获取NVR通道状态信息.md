# API-云接入-通用设备管理-设备信息查询-获取NVR通道状态信息

> 更新时间: 2026-07-09T13:33:36.000+08:00

> 文档ID: 676 | 来源树: OPEN_API

---

## 获取NVR通道状态信息

- 接口功能

   查询设备通道状态。 子账户token请求所需最小权限："Permission":"Get" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/v3/open/device/metadata/channel/status`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 授权过程获取的access\_token | Y |
| Header | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request GET  'https://open.ys7.com/api/v3/open/device/metadata/channel/status' \ 
--header  'accessToken: da.1l9n1lf7bfydue530l3t1piq8x65msb-4g3fy7x9uq-109ldkn-xu8zfofjw' \ 
--header  'deviceSerial: E08397579'
```

- 返回数据

```
{ 
     "result": { 
         "msg":  "Operation succeeded", 
         "code":  "200", 
         "data": { 
             "deviceSerial":  "E08397579", 
             "channelInfoList": [ 
                { 
                     "superDevChannel":  1, 
                     "status":  1 
                } 
            ], 
             "status":  1 
        } 
    } 
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| deviceSerial | String | 设备序列号 |
| status | Int | 0-离线 1-在线 |
| channelInfoList | Object | 子设备通道列表 |
| superDevChannel | Int | 通道号 |
| status | Int | 0-离线 1-在线 2-未上报,在托管的情况下代表无权限 |

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