# API-云接入-通用设备管理-设备信息查询-获取设备状态信息

> 更新时间: 2026-07-09T13:33:30.000+08:00

> 文档ID: 675 | 来源树: OPEN_API

---

## 获取设备状态信息

- 接口功能

该接口用于根据序列号通道号获取设备状态信息。子账户token请求所需最小权限 "Permission":"Get" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/lapp/device/status/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channel | Int | 通道号,默认为1 | N |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/device/status/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.20h863523v1zfck75qgmwhoy7vl2teqp' \
--data-urlencode 'deviceSerial=427734168' \
--data-urlencode 'channel=1'
```

- 返回数据

```
{
    "data": {
        "privacyStatus": 0,
        "pirStatus": -2,
        "alarmSoundMode": 2,
        "battryStatus": -1,
        "lockSignal": -1,
        "diskNum": 1,
        "diskState": "0---------------",
        "cloudType": 0,
        "cloudStatus": 2,
        "nvrDiskNum": 1,
        "nvrDiskState": "0---------------"
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| privacyStatus | Int | 隐私状态: 0：隐私状态关闭；1：隐私状态打开；-1：初始值；2：不支持,C1专用,-2:设备没有上报或者设备不支持该状态 |
| pirStatus | Int | 红外状态，1：红外启用，0：红外禁用，-1：初始值，2：不支持,-2:设备没有上报或者设备不支持该状态 |
| alarmSoundMode | Int | 告警声音模式，0：短叫，1：长叫，2：静音,3:自定义语音,-1:设备没有上报或者设备不支持该状态 |
| battryStatus | Int | 电池电量,1到100(%)，-1:设备没有上报或者设备不支持该状态 |
| lockSignal | Int | 门锁和网关间的无线信号，百分比表示 差值超过10上报,-1:设备没有上报或者设备不支持该状态 |
| diskNum | Int | 挂载的sd硬盘数量,-1:设备没有上报或者设备不支持该状态 |
| diskState | String | sd硬盘状态:0:正常;1:存储介质错;2:未格式化;3:正在格式化;返回形式:一个硬盘表示为"0---------------",两个硬盘表示为"00--------------",以此类推;-1:设备没有上报或者设备不支持该状态 |
| cloudStatus | Int | 云存储状态: -2:设备不支持;-1: 未开通;0: 未激活;1: 激活;2: 过期 |
| nvrDiskNum | Int | NVR上挂载的硬盘数量: -1:设备没有上报或者设备不支持;-2:未关联,类似于NVR类型的上级设备 |
| nvrDiskState | String | NVR上挂载的硬盘状态:0:正常;1:存储介质错;2:未格式化;3:正在格式化;返回形式:一个硬盘表示为"0---------------",两个硬盘表示为"00--------------",以此类推;-1:设备没有上报或者设备不支持该状态;-2:未关联,类似于NVR类型的上级设备 |
| netAddress | String | 设备IP地址 |
| signal | Int | 设备的信号强度 0-100，-1：设备未上报或不支持 |
| wakeUpStatus | Int | 低功耗设备运行状态 0:正常 1:休眠 -1:设备未上报或不支持 |
| cloudChannelList | Array | 设备通道号和设备侧云存储上报开关状态 0:关闭 1:开启 设备不支持该状态返回空 |

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