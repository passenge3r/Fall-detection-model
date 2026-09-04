# API-设备云组件仓-智能锁-基础功能-PIR侦测-设置PIR触发录像开关

> 更新时间: 2026-07-09T13:45:27.000+08:00

> 文档ID: 781 | 来源树: OPEN_API

---

## 设置PIR触发录像开关

- 接口功能

   该接口用于设置PIR触发录像开关。本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁，其余型号不保证可用。如下接口调用需要联系萤石配置白名单，否则接口可能调用报错。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/PIR/PirRecordSwitch`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | data | Integer | PIR触发录像开关，取值范围[0,1]：0-关闭，1-开启 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/PIR/PirRecordSwitch' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '1'
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