# API-云接入-通用设备管理-设备信息查询-获取单个设备信息

> 更新时间: 2026-07-09T18:39:28.000+08:00

> 文档ID: 672 | 来源树: OPEN_API

---

## 获取单个设备信息

- 接口功能

   获取单个设备信息

- 请求地址

`https://open.ys7.com/api/lapp/device/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 访问令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/info' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx'
```

- 返回数据

```
{
    "msg": "Operation succeeded",
    "code": "200",
    "data": {
        "deviceSerial": "BF7513110",
        "deviceName": "CS-CTQ6X(BF7513110)",
        "localName": "CS-CTQ6X(BF7513110)",
        "model": "CS-CTQ6X-V105-1J4WF",
        "status": 0,
        "defence": 1,
        "isEncrypt": 0,
        "alarmSoundMode": 2,
        "offlineNotify": 0,
        "category": "CS-CTQ6X",
        "parentCategory": "IPC",
        "updateTime": 1766124737000,
        "netType": "wire",
        "signal": "100%",
        "riskLevel": 0,
        "netAddress": "122.224.169.38",
        "localAddress": "10.11.149.98",
        "netName": "eth0",
        "ssid": ""
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 响应提示说明 |
| code | String | 响应结果状态码 |
| data | Object | 设备信息 |
| deviceSerial | String | 设备序列号 |
| deviceName | String | 设备名称 |
| localName | String | 设备上报名称 |
| model | String | 设备型号 |
| status | Int | 设备状态 0-不在线,1-在线 |
| defence | Int | 撤防状态 0-撤防,1-布防 |
| isEncrypt | Int | 是否加密 0-未加密,1-加密 |
| alarmSoundMode | Int | 告警声音模式,0-短叫，1-长叫，2-静音 |
| offlineNotify | Int | 设备下线是否通知,0-不通知 1-通知 |
| category | String | 设备大类 |
| parentCategory | String | 设备二级类目 |
| updateTime | Int | 修改时间 |
| netType | String | 网络类型 |
| signal | String | 信号强度 |
| riskLevel | Int | 设备风险安全等级，0-安全，大于零，有风险，风险越高，值越大 |
| netAddress | String | 设备IP地址 |
| localAddress | String | 设备局域网IP地址 |
| netName | String | 网络名称 |
| ssid | String | SSID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 无效参数 | 参数为空或格式不正确 |