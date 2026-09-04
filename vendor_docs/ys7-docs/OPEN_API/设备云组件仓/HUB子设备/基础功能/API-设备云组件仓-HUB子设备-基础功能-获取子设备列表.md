# API-设备云组件仓-HUB子设备-基础功能-获取子设备列表

> 更新时间: 2026-07-01T18:45:24.000+08:00

> 文档ID: 1356 | 来源树: OPEN_API

---

## 获取子设备列表

- 接口功能

   该接口用于查询指定HUB设备关联的子设备列表。子账户token请求所需最小权限：Permission=Get，Resource=dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/hub/device/sub/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | HUB设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | version | String | 版本号 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/hub/device/sub/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510888'
```

- 返回数据

```
{
    "data": [
        {
            "deviceSerial": "596510888-E38012760",
            "deviceName": null,
            "type": 1,
            "deviceCoverUrl": "https://i.ys7.com/image/CS-T3-A/1.jpeg",
            "deviceType": "CS-T3-A",
            "subDeviceStatusVos": [
                {
                    "channelNo": 0,
                    "key": "DetectorDefencePlan",
                    "value": "1"
                }
            ]
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
| data | Array | 子设备列表 |
| data[].deviceSerial | String | 子设备序列号 |
| data[].deviceName | String | 子设备名称 |
| data[].type | Int | 子设备类型：1-探测器 2-开关 |
| data[].deviceCoverUrl | String | 设备封面(全路径) |
| data[].deviceType | String | 设备类型 |
| data[].subDeviceStatusVos | Array | 子设备状态 |
| data[].subDeviceStatusVos[].channelNo | Int | 通道号 |
| data[].subDeviceStatusVos[].key | String | 状态key |
| data[].subDeviceStatusVos[].value | String | 状态值 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 | 设备序列号输入有误或者设备未被添加 |
| 20014 | deviceSerial不合法 | 检查设备序列号是否正确 |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |