# API-设备云组件仓-智能电梯网络摄像机-视频功能-视频直播与回放

> 更新时间: 2026-06-30T11:54:19.000+08:00

> 文档ID: 1599 | 来源树: OPEN_API

---

## 视频直播与回放

- 接口功能

   根据appKey和secret获取accessToken，获取指定有效期的直播地址。萤石平台提供了多种服务，可以支持在web、PC、APP端、H5等多种终端进行取流，通过HLS协议和RTMP协议实现预览。

- 请求地址

`https://open.ys7.com/api/lapp/v2/live/address/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 用户访问令牌 | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 通道号，普通摄像头默认为1，多通道设备可填实际通道号 | N |
| body | expireTime | Int | 过期时长，单位秒；针对hls/rtmp协议设置有效期，相对时间；30秒-7天 | N |
| body | protocol | Int | 播放协议，1-ezopen、2-hls、3-rtmp、4-flv，默认为1 | N |
| body | code | String | 设备的视频加密密码，针对ezopen协议设置有效，hls/rtmp不支持加密视频 | N |
| body | quality | Int | 视频清晰度，1-高清（主码流）、2-流畅（子码流） | N |
| body | type | Int | 1-预览，2-本地录像回放，3-云存储录像回放，默认为1；回放针对ezopen协议设置有效，hls/rtmp不支持回放 | N |
| body | startTime | String | 本地录像/云存储录像回放开始时间，示例：2019-12-01 00:00:00 | N |
| body | stopTime | String | 本地录像/云存储录像回放结束时间，示例：2019-12-02 00:00:00 | N |
| body | supportH265 | Int | 播放端是否要求播放视频为H265编码格式，1表示需要，0表示不要求 | N |
| body | gbchannel | String | 国标设备的通道编号，视频通道编号ID | N |
| body | playbackSpeed | Int | 回放倍速，倍速为1/2/4/8，传-1为支持的最大倍速，仅支持protocol为4-flv且type为2-本地录像回放、3-云存储录像回放 | N |
| body | busType | Int | 云端录像类型(仅云存储录像生效)，默认0，0-普通回放，7-云录制录像 | N |
| body | containerFormat | Int | HLS H265编码封装格式，0-ts，1-fMP4，不传默认为0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/v2/live/address/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734222' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'protocol=2' \
--data-urlencode 'quality=1' \
--data-urlencode 'type=1'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功",
    "data": {
        "id": "424537743",
        "url": "https://open.ys7.com/v3/openlive/427734222_1_1.m3u8?expire=1640966400&id=424537743",
        "expireTime": "2021-12-31 00:00:00"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示操作成功 |
| msg | String | 返回信息描述 |
| data | Object | 直播地址信息 |
| data.id | String | 直播地址唯一标识 |
| data.url | String | 直播/回放地址 |
| data.expireTime | String | 地址过期时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 无效参数 | 请检查请求参数 |
| 10002 | accessToken过期或异常 | 请重新获取accessToken |
| 10031 | 子账号或开发者用户无权限 | 请检查账号权限 |
| 20001 | 通道不存在 | 请检查通道号 |
| 20002 | 设备不存在 | 请检查设备序列号 |
| 20007 | 设备不在线 | 请检查设备在线状态 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 60019 | 加密已开启 | 请先关闭视频加密或传入加密密码 |