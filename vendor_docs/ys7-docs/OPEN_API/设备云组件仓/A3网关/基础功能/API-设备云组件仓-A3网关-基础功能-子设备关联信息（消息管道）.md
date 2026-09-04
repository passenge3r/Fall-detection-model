# API-设备云组件仓-A3网关-基础功能-子设备关联信息（消息管道）

> API-设备云组件仓-A3网关-基础功能-子设备关联信息（消息管道）

> 更新时间: 2026-05-25T16:40:30.000+08:00

> 文档ID: 882 | 来源树: OPEN_API

---

## 子设备关联消息

本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。

注：网关下子设备相关接口需用长序列号调用 例：C87654321-C12345678

| **header** | **Object** | **设备信息** |
| --- | --- | --- |
| type | String | 消息类型：ys.hub.connect表示子设备关联消息 |
| deviceId | String | 设备序列号 |
| channelNo | String | 设备通道号 |
| messageId | String | 消息唯一ID |

| **body** | **Object** | **设备上传的消息** |
| --- | --- | --- |
| hubSerial | String | hub设备序列号 |
| occurTime | String | 发生时间，格式：yyyy-MM-dd HH:mm:ss |
| msgType | String | HUB\_CONNNECT\_STATUS |
| childs | String | 关联的子设备列表 |

Child对象

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| connected | String | 联通状态：0-未联通、1-联通 |
| childDevGlobalId | String | 子设备序列号 |
| childLocalId | String | 子设备本地ID |
| type | String | 子设备型号子 |
| version | String | 子设备版本号 |

- 示例

```
{

"header": {

        "messageTime": 1605617130109,

        "channelNo": 0,

        "messageId": "5fb3c5eab785de0086a0fa9e",

        "type": "ys.hub.connect",

        "deviceId": "fe33db3e0fee4e7f94:be4af88dd3ab44bd"

    },

    "body": {

        "msgType": "HUB_CHILD_LIST",

        "occurTime": "2020-11-17 20:45:30",

        "hubSerial": "fe33db3e0fee4e7f94:be4af88dd3ab44bd",

        "childs": [

            {

                "connected": 1,

                "childDevGlobalId":
"fe33db3e0fee4e7f94:be4af88dd3ab44bd-c82bd4c3bc",

                "childLocalId":
"c82bd4c3bc",

                "type":
"iDS-6704NX/FA-B-V2",

                "version":
"V4.1.61 build 190515"

            },

            {

                "connected": 1,

                "childDevGlobalId":
"fe33db3e0fee4e7f94:be4af88dd3ab44bd-d9e3485bf7",

                "childLocalId":
"d9e3485bf7",

                "type":
"DS-2CD7247HWD-A",

                "version":
"V5.5.64 build 181113"

            },

            {

                "connected": 1,

                "childDevGlobalId":
"fe33db3e0fee4e7f94:be4af88dd3ab44bd-ca6f40f5fd",

                "childLocalId":
"ca6f40f5fd",

                "type":
"DS-2CD7A47HWD-XZS",

                "version":
"V5.5.73 build 190131"

            }

        ]

    }

}
```

子设备上下线信息

消息类型：ys.hub.connect

| **header** | **Object** | **消息头信息** |
| --- | --- | --- |
| deviceId | String | 设备ID |
| channelNo | Integer | 通道号 |
| type | String | 消息类型 |
| messageTime | Long | 消息投递时间，非必须 |

| **body** | **Object** | **设备上传的消息** |
| --- | --- | --- |
| hubSerial | String | 父设备全局ID |
| occurTime | String | 发生时间，yyyy-MM-dd HH:mm:ss |
| msgType | String | 固定值，HUB\_CONNECT\_STATUS |
| childs | Array | 子设备信息列表 |

Child信息

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| childDevGlobalId | String | 子设备全局ID |
| connected | Integer | 0：断线；1：在线 |