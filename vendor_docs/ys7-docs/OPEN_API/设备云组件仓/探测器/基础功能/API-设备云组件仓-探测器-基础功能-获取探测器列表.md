# API-设备云组件仓-探测器-基础功能-获取探测器列表

> 更新时间: 2026-07-01T18:43:47.000+08:00

> 文档ID: 1311 | 来源树: OPEN_API

---

## 获取探测器列表

- 接口功能

   该接口用于获取设备下关联的探测器列表（需要设备支持关联探测器）。子账户token请求所需最小权限："Permission":"Get"，"Resource":"dev:序列号"。

- 请求地址

`https://open.ys7.com/api/lapp/detector/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 网关设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/detector/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510888'
```

- 返回数据

```
{
    "result": {
        "data": [
            {
                "detectorSerial": "594012222",
                "detectorType": "callhelp",
                "detectorState": 1,
                "detectorTypeName": "紧急按钮",
                "location": "紧急按钮",
                "zfStatus": 0,
                "uvStatus": 0,
                "iwcStatus": 0,
                "olStatus": 0,
                "atHomeEnable": 1,
                "outerEnable": 1,
                "sleepEnable": 1
            },
            {
                "detectorSerial": "303333333",
                "detectorType": "waterlogging",
                "detectorState": 1,
                "detectorTypeName": "水浸",
                "location": "卫生间",
                "zfStatus": 0,
                "uvStatus": 0,
                "iwcStatus": 0,
                "olStatus": 1,
                "atHomeEnable": 1,
                "outerEnable": 1,
                "sleepEnable": 1
            }
        ],
        "code": "200",
        "msg": "操作成功!"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| result.code | String | 返回码，200表示成功 |
| result.msg | String | 返回信息 |
| result.data | Array | 探测器列表 |
| detectorSerial | String | 探测器序列号 |
| detectorType | String | 探测器类型 |
| detectorState | Int | 探测器与设备是否连通：0-非联通，1-联通 |
| detectorTypeName | String | 探测器类型名称 |
| location | String | 探测器位置（自定义），对应修改后的名称 |
| zfStatus | Int | 防区故障：0-恢复，1-产生 |
| uvStatus | Int | 电池欠压：0-恢复，1-产生 |
| iwcStatus | Int | 无线干扰：0-恢复，1-产生 |
| olStatus | Int | 离线：0-恢复，1-产生 |
| atHomeEnable | Int | 在家是否使能：0-关闭，1-开启 |
| outerEnable | Int | 外出是否使能：0-关闭，1-开启 |
| sleepEnable | Int | 睡眠模式是否使能：0-关闭，1-开启 |

   防区故障、电池欠压、无线干扰、离线几种属于故障类型。“产生”表示产生故障，“恢复”表示故障恢复。

**探测器类型名称：**

| 探测器类型 | 探测器类型名称 |
| --- | --- |
| V | 视频设备 |
| I | 告警输入设备 |
| O | 告警输出设备 |
| PIR | 红外探测器 |
| FIRE | 烟感探测器 |
| MAGNETOMETER | 门磁传感器 |
| GAS | 可燃气体 |
| WATERLOGGING | 水浸 |
| CALLHELP | 紧急按钮 |
| TELECONTROL | 遥控器 |
| ALERTOR | 告警器 |
| KEYBOARD | 键盘 |
| CURTAIN | 幕帘 |
| MOVE\_MAGNETOMETER | 单体门磁 |

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
| 60020 | 不支持该命令 | 该设备不支持关联探测器 |