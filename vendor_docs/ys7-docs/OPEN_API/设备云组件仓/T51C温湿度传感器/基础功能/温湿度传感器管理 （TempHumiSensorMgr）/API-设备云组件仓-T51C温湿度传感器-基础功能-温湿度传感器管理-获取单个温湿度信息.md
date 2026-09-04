# API-设备云组件仓-T51C温湿度传感器-基础功能-温湿度传感器管理-获取单个温湿度信息

> API-设备云组件仓-T51C温湿度传感器-基础功能-温湿度传感器管理-获取单个温湿度信息

> 更新时间: 2026-05-25T16:41:20.000+08:00

> 文档ID: 1151 | 来源树: OPEN_API

---

## 获取单个温湿度信息 （GetTempHumiInfo）

本文档仅适用于设备型号 CS-T51C-BG，其余型号不保证可用。

- URL

https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/TempHumiSensorMgr/GetTempHumiInfo

- method

PUT

- header 请求头

| 名称 | value | 描述 | 是否必填 |
| --- | --- | --- | --- |
| Content-Type | application/json |  |  |
| accessToken | [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | 用户访问令牌 |  |

- request 请求参数

| 名称 | 参数位置 | 数据类型 | 请求参数描述 |
| --- | --- | --- | --- |
| deviceSerial | Path | String | 设备序列号 |

- request body 请求报文说明

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| ID | 温湿度传感器通道编号 | integer | [0,2147483647] |  | 必填 |

- request body 请求报文示例

```
{
	"ID":0
}
```

- response body 应答报文说明

| 字段标识 | 数据类型 | 响应字段描述 |
| --- | --- | --- |
| meta | object | 服务响应信息 |
| meta.code | integer | 服务响应状态码。参见响应码解释。 |
| meta.message | string | 服务响应状态描述 |
| meta.moreInfo | object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | string | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | string | 设备响应状态描述 |
| data | object | 业务参数，详细说明见下表 |

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| currentTime | 当前时间 | string | [1,] |  | 必填 |
| temperature | 设备环境温度 | number | [-273.0,1000.0] |  | 非必填 |
| humidity | 设备环境湿度 | number | [0.0,100.0] |  | 非必填 |

- response body 应答报文示例

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
  },
  "data": {
	"currentTime":"",
	"temperature":0.0,
	"humidity":0.0
}
}
```