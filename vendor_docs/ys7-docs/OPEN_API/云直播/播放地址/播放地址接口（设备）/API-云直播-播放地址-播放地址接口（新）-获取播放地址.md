# API-云直播-播放地址-播放地址接口（新）-获取播放地址

> API-云直播-播放地址-播放地址接口（新）-获取播放地址

> 更新时间: 2026-07-24T10:14:24.000+08:00

> 文档ID: 1414 | 来源树: OPEN_API

---

## 获取播放地址

- 接口功能：

  该接口用于通过设备序列号、通道号获取单台设备的播放地址信息，无法获取永久有效期播放地址。
- 请求地址

  `https://open.ys7.com/api/lapp/v2/live/address/get`
- 子账户token请求所需最小权限

  `"Permission":"Real,Replay" "Resource":"dev:序列号"`
- 小权限token（仅支持设备类小权限）

  `"action":"Real" "resourceCatagory":"video"`
- 请求方式

  `POST`
- 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| accessToken | String | 授权过程获取的access\_token | Y |
| deviceSerial | String | 设备序列号例如427734222，均采用英文符号，限制最多50个字符 | Y |
| channelNo | Integer | 通道号，非必选，默认为1 | N |
| protocol | Integer | 流播放协议，1-ezopen、2-hls、3-rtmp、4-flv，5-llhls 默认为1 | N |
| code | String | ezopen协议地址的设备的视频加密密码 | N |
| expireTime | Integer | 过期时长，单位秒；针对hls/rtmp/flv设置有效期，相对时间；30秒-720天 | N |
| type | String | 地址的类型，1-预览，2-本地录像回放，3-云存储录像回放，非必选，默认为1；回放仅支持rtmp、ezopen、flv、llhls协议。云录制2.0获取播放地址请参考：<https://open.ys7.com/help/2044> | N |
| quality | Integer | 预览视频清晰度【仅针对预览生效，录像回放不支持切换清晰度】，1-高清（主码流）、2-流畅（子码流） | N |
| startTime | String | 本地录像/云存储录像回放开始时间,云存储开始结束时间必须在同一天，示例：2019-12-01 00:00:00 | N |
| stopTime | String | 本地录像/云存储录像回放结束时间,云存储开始结束时间必须在同一天，示例：2019-12-01 23:59:59 | N |
| supportH265 | Integer | 请判断播放端是否要求播放视频为H265编码格式,1表示需要，0表示不要求 | N |
| containerFormat | Integer | 封装格式，仅在选择hls协议且supportH265=1的情况下生效，0-ts、1-fMP4，不传默认为0 | N |
| mute | Integer | 开启静音 ,1: 静音，0:不静音（ 默认），服务端静音，开启后客户端非静音也不会有声音。备注：该选项只针对RTMP、HTTP-FLV、HLS有效。 | N |
| playbackSpeed | String | 回放倍速。倍速为 -1（ 支持的最大倍速）、0.5、1、2、4、8、16；  仅支持protocol为4-flv  且  type为2-本地录像回放（ 部分设备可能不支持16倍速） 或者 3-云存储录像回放 | N |
| gbchannel | String | 国标设备的通道编号，视频通道编号ID | N |
| diserr | String | 是否禁用错误码图片（目前该功能在 protocol=4 flv协议生效），1-禁用，0-不禁用（默认） | N |

- HTTP请求报文

```
POST /api/lapp/v2/live/address/get HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

accessToken=at.dunwhxt2azk02hcn7phqygsybbw0wv6p&deviceSerial=C78957921&channelNo=1
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

- 返回字段：

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码，参考下方返回码。**优先判断该错误码，返回200即表示成功**。 |
| msg | String | 状态描述 |
| id | String | 标识直播地址url唯一值 |
| url | String | 直播地址 |
| expireTime | long | 直播地址有效期。**expireTime参数为空时该字段无效** |

> 注意：该接口请求时先解析code属性，如果返回200即表示成功，可继续解析data属性的内容，每一个地址对象中先解析ret属性，如果返回200表示成功，再根据status属性和exception属性判断是否存在异常。

- 返回码

| 返回码 | 返回消息 | 备注 |
| --- | --- | --- |
| 200 | 操作成功，获取指定有效期的直播地址 | 请求成功 |
| 201 | Created |  |
| 401 | Unauthorized |  |
| 403 | Forbidden |  |
| 404 | Not Found |  |
| 403 | 用户不存在 |  |