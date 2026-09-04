# API-设备云组件-CS-T33-BW红外遥控器-基础功能-根据设备类型和品牌查询红码

>  

> 更新时间: 2026-06-30T10:58:35.000+08:00

> 文档ID: 1526 | 来源树: OPEN_API

---

## 根据设备类型和品牌查询红码

- 接口功能

   根据类型和品牌查询红码。

- 请求地址

`https://open.ys7.com/api/service/device/metadata/infrared/remote`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | type | Int | 设备类型id | Y |
| query | brand | String | 品牌id | Y |
| query | index | Int | 红码方案序号，默认从1开始 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/device/metadata/infrared/remote?type=1&brand=247&index=1' \
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
        "baseVO": {
            "id": 6386,
            "frequency": 37890,
            "remoteType": 1,
            "tag": "99999",
            "tagValue": "00020ECD010008D9001400140014003C010004014300A1000000"
        },
        "functionsVO": {
            "modes": []
        },
        "keysVO": {
            "keys": [
                {
                    "keyId": "1",
                    "name": "POWER",
                    "displayName": "电源",
                    "pulse": "000317",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "10035",
                    "name": "A/V",
                    "displayName": "A/V",
                    "pulse": "0003EE",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "101",
                    "name": "9",
                    "displayName": "9",
                    "pulse": "000329",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "10195",
                    "name": "-/--",
                    "displayName": "-/--",
                    "pulse": "00032A",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "106",
                    "name": "MUTE",
                    "displayName": "静音",
                    "pulse": "00031C",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "116",
                    "name": "BACK",
                    "displayName": "返回",
                    "pulse": "00037B",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "121",
                    "name": "EXIT",
                    "displayName": "退出",
                    "pulse": "0003D7",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "131",
                    "name": "DISPLAY",
                    "displayName": "屏显",
                    "pulse": "0003D2",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "2187",
                    "name": "NORMAL",
                    "displayName": "标准化",
                    "pulse": "000310",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "271",
                    "name": "SOUND CHANNEL",
                    "displayName": "声道",
                    "pulse": "00037D",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "366",
                    "name": "NICAM",
                    "displayName": "丽音",
                    "pulse": "000300",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "42",
                    "name": "OK",
                    "displayName": "确认",
                    "pulse": "0003D7",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "43",
                    "name": "CH+",
                    "displayName": "频道+",
                    "pulse": "000319",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "44",
                    "name": "CH-",
                    "displayName": "频道-",
                    "pulse": "000318",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "45",
                    "name": "MENU",
                    "displayName": "菜单",
                    "pulse": "00037A",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "46",
                    "name": "NAVIGATE_UP",
                    "displayName": "上",
                    "pulse": "00037E",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "47",
                    "name": "NAVIGATE_DOWN",
                    "displayName": "下",
                    "pulse": "00037F",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "48",
                    "name": "NAVIGATE_LEFT",
                    "displayName": "左",
                    "pulse": "00035B",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "49",
                    "name": "NAVIGATE_RIGHT",
                    "displayName": "右",
                    "pulse": "00035A",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "50",
                    "name": "VOL+",
                    "displayName": "音量+",
                    "pulse": "00031E",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "51",
                    "name": "VOL-",
                    "displayName": "音量-",
                    "pulse": "00031F",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "56",
                    "name": "0",
                    "displayName": "0",
                    "pulse": "00032B",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "61",
                    "name": "1",
                    "displayName": "1",
                    "pulse": "000321",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "66",
                    "name": "2",
                    "displayName": "2",
                    "pulse": "000322",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "71",
                    "name": "3",
                    "displayName": "3",
                    "pulse": "000323",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "76",
                    "name": "4",
                    "displayName": "4",
                    "pulse": "000324",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "81",
                    "name": "5",
                    "displayName": "5",
                    "pulse": "000325",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "86",
                    "name": "6",
                    "displayName": "6",
                    "pulse": "000326",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "91",
                    "name": "7",
                    "displayName": "7",
                    "pulse": "000327",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "96",
                    "name": "8",
                    "displayName": "8",
                    "pulse": "000328",
                    "tag": null,
                    "tagValue": null
                },
                {
                    "keyId": "9790",
                    "name": "12",
                    "displayName": "12",
                    "pulse": "00032C",
                    "tag": null,
                    "tagValue": null
                }
            ]
        },
        "total": 1,
        "now": 1,
        "hasNext": false
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 返回码 |
| meta.message | String | 返回消息 |
| meta.moreInfo | Object | 更多信息 |
| data | Object | 返回数据 |
| data.baseVO | Object | 基础信息 |
| data.baseVO.id | Int | 红码id |
| data.baseVO.frequency | Int | 红码频率 |
| data.baseVO.remoteType | Int | 遥控器类型 |
| data.baseVO.tag | String | 标签 |
| data.baseVO.tagValue | String | 标签值 |
| data.functionsVO | Object | 功能信息 |
| data.functionsVO.modes | Array | 模式列表 |
| data.keysVO | Object | 按键信息 |
| data.keysVO.keys | Array<Object> | 按键列表 |
| data.keysVO.keys.keyId | String | 按键id |
| data.keysVO.keys.name | String | 按键名称 |
| data.keysVO.keys.displayName | String | 按键显示名称 |
| data.keysVO.keys.pulse | String | 脉冲编码 |
| data.keysVO.keys.tag | String | 标签 |
| data.keysVO.keys.tagValue | String | 标签值 |
| data.total | Int | 总数 |
| data.now | Int | 当前序号 |
| data.hasNext | Boolean | 是否有下一个 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 100031 | 子账户或萤石用户没有权限 | http状态码403 |
| 20007 | 设备不在线 | http状态码412 |
| 20018 | 该用户不拥有该设备 | http状态码403 |
| 20032 | 该用户下通道不存在 | http状态码404 |
| 20040 | 查询设备开关状态失败 | http状态码404 |
| 21001 | 获取红码支持的类型不存在 | http状态码404 |
| 21002 | 根据类型查询红码品牌列表不存在 | http状态码404 |
| 21003 | 根据类型和品牌查询红码方案不存在 | http状态码404 |
| 21004 | 调用红码服务绑定红码方案控制指定类型的电器出现异常 | http状态码500 |
| 21005 | 调用红码服务解绑红码方案控制指定类型的电器出现异常 | http状态码500 |
| 50000 | 服务异常 | http状态码500 |