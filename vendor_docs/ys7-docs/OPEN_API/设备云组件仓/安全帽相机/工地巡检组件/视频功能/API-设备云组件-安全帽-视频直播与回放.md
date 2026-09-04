# API-设备云组件-安全帽-视频直播与回放

>  

> 更新时间: 2026-06-30T11:47:52.000+08:00

> 文档ID: 1490 | 来源树: OPEN_API

---

## 获取播放地址

- 接口功能

   该接口用于通过设备序列号、通道号获取单台设备的播放地址信息，无法获取永久有效期播放地址。

- 请求地址

`https://open.ys7.com/api/lapp/v2/live/address/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号，例如427734222，均采用英文符号，限制最多50个字符 | Y |
| body | channelNo | Int | 通道号，非必选，默认为1 | N |
| body | protocol | Int | 流播放协议，1-ezopen、2-hls、3-rtmp、4-flv，默认为1 | N |
| body | code | String | ezopen协议地址的设备的视频加密密码 | N |
| body | expireTime | Int | 过期时长，单位秒；针对hls/rtmp/flv设置有效期，相对时间；30秒-720天 | N |
| body | type | String | 地址的类型，1-预览，2-本地录像回放，3-云存储录像回放，非必选，默认为1；回放仅支持rtmp、ezopen、flv协议 | N |
| body | quality | Int | 视频清晰度，1-高清（主码流）、2-流畅（子码流） | N |
| body | startTime | String | 本地录像/云存储录像回放开始时间，云存储开始结束时间必须在同一天，示例：2019-12-01 00:00:00 | N |
| body | stopTime | String | 本地录像/云存储录像回放结束时间，云存储开始结束时间必须在同一天，示例：2019-12-01 23:59:59 | N |
| body | supportH265 | Int | 请判断播放端是否要求播放视频为H265编码格式，1表示需要，0表示不要求 | N |
| body | playbackSpeed | String | 回放倍速，倍速为-1(支持的最大倍速)、0.5、1、2、4、8、16；仅支持protocol为4-flv且type为2-本地录像回放或3-云存储录像回放 | N |
| body | gbchannel | String | 国标设备的通道编号，视频通道编号ID | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/v2/live/address/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=C78957921' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "msg": "Operation succeeded",
    "code": "200",
    "data": {
        "id": "254708522214232064",
        "url": "https://open.ys7.com/v3/openlive/C78957921_1_1.m3u8?expire=1606999273&id=254708522214232064&t=093e5c6668d981e0f0b8d2593d69bdc98060407d1b2f42eaaa17a62b15ee4f99&ev=100",
        "expireTime": "2020-12-03 20:41:13"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码，返回200即表示成功 |
| msg | String | 状态描述 |
| data | Object | 返回数据 |
| data.id | String | 地址id |
| data.url | String | 直播地址 |
| data.expireTime | String | 直播地址有效期，expireTime参数为空时该字段无效 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 201 | Created | Created |
| 401 | Unauthorized | Unauthorized |
| 403 | Forbidden | Forbidden |
| 404 | Not Found | Not Found |
| 403 | 用户不存在 | 用户不存在 |