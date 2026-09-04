# API-云接入-通用设备管理-设备信息查询-获取指定设备的通道信息

>  

> 更新时间: 2026-06-30T17:56:26.000+08:00

> 文档ID: 1478 | 来源树: OPEN_API

---

## 获取指定设备的通道信息

- 接口功能

   获取指定设备的通道信息。注：获取到的通道信息，若NVR设备自动上报关联的IPC信息则返回的是IPC的信息，若NVR设备不进行上报，将获取不到关联的IPC信息。

- 请求地址

`https://open.ys7.com/api/lapp/device/camera/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/camera/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734222'
```

- 返回数据

```
{
    "data": [
        {
            "deviceSerial": "427734222",
            "ipcSerial": "427734222",
            "channelNo": 1,
            "deviceName": "My(427734222)427734222",
            "channelName": "My(427734222)427734222",
            "localChannelName": "Camera 01",
            "status": 1,
            "isShared": "0",
            "picUrl": "https://portal.ys7.com/assets/imgs/public/homeDevice.jpeg",
            "isEncrypt": 0,
            "videoLevel": 2,
            "relatedIpc": false
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码，200表示成功 |
| msg | String | 状态描述 |
| data | Array<Object> | 通道信息列表 |
| data.deviceSerial | String | 设备序列号 |
| data.ipcSerial | String | IPC序列号 |
| data.channelNo | Int | 通道号 |
| data.deviceName | String | 设备名 |
| data.localName | String | 设备上报名称 |
| data.channelName | String | 通道名 |
| data.localChannelName | String | 本地通道名 |
| data.status | Int | 在线状态：0-不在线，1-在线，-1设备未上报 |
| data.isShared | String | 是否共享，0-未共享，1-已共享 |
| data.picUrl | String | 图片地址（大图），若在萤石客户端设置封面则返回封面图片，未设置则返回默认图片 |
| data.isEncrypt | Int | 是否加密，0：不加密，1：加密 |
| data.videoLevel | Int | 视频质量：0-流畅，1-均衡，2-高清，3-超清 |
| data.relatedIpc | Boolean | 当前通道是否关联IPC：true-是，false-否。设备未上报或者未关联都是false |
| data.isAdd | Int | 是否显示，0：隐藏，1：显示 |
| data.devType | String | camera设备类型 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 | 设备不存在 |
| 20014 | deviceSerial不合法 | deviceSerial不合法 |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |