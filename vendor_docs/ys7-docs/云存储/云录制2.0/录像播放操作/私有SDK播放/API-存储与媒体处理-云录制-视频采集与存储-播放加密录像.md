# API-存储与媒体处理-云录制-视频采集与存储-播放加密录像

> 更新时间: 2026-06-25T14:30:27.000+08:00

> 文档ID: 2044 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-播放加密录像

- 接口功能

   播放加密录像。

- 请求地址

`https://open.ys7.com/api/lapp/v2/live/address/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| body | accessToken | String | accessToken | Y |
| body | deviceSerial | String | 设备序列号例如427734222，均采用英文符号，限制最多50个字符 | Y |
| body | channelNo | Int | 通道号，非必选，默认为1 | N |
| body | protocol | Int | 流播放协议，1-ezopen、云录制仅支持为1 | N |
| body | code | String | ezopen协议地址的设备的视频加密密码 | N |
| body | expireTime | Int | 过期时长，单位秒；针对hls/rtmp/flv设置有效期，相对时间；30秒-720天 | N |
| body | type | String | 地址的类型，3-云存储录像回放，必选；回放仅支持ezopen协议 | Y |
| body | quality | Int | 视频清晰度，1-高清（主码流）、2-流畅（子码流） | N |
| body | startTime | String | 云录制录像回放开始时间，云录制开始结束时间必须在同一天，示例：2019-12-01 00:00:00 | Y |
| body | stopTime | String | 云录制录像回放结束时间，云录制开始结束时间必须在同一天，示例：2019-12-01 23:59:59 | Y |
| body | supportH265 | Int | 请判断播放端是否要求播放视频为H265编码格式，1表示需要，0表示不要求 | N |
| body | gbchannel | String | 国标设备的通道编号，视频通道编号ID | N |
| body | playbackSpeed | Int | 回放倍速 倍速为 1 2 4 8 传-1 为支持的最大倍速 仅支持protocol为4-flv 且 type为2-本地录像回放，3-云存储录像回放 | N |
| body | busType | Int | 云端录像类型(仅云存储录像生效)：默认0；0：普通回放，7：云录制录像（云录制录像仅支持ezopen协议） | Y |
| body | containerFormat | Int | HLS H265编码封装格式，0-ts，1-fMP4，不传默认为0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/v2/live/address/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734222' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'protocol=1' \
--data-urlencode 'type=3' \
--data-urlencode 'startTime=2019-12-01 00:00:00' \
--data-urlencode 'stopTime=2019-12-01 23:59:59' \
--data-urlencode 'busType=7'
```

- 返回数据

```
{
   "msg": "操作成功",
   "code": "200",
   "data": {
       "id": "558005911715250176",
       "url": "ezopen://open.ys7.com/C33368372/1.cloud.rec?busType=7",
       "expireTime": "2023-03-21 19:16:16"
   }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码，参考下方返回码。优先判断该错误码，返回200即表示成功 |
| msg | String | 状态描述 |
| data | Object | 数据 |
| -id | String | id |
| -url | String | 现仅支持EZOPEN协议直播地址，传入UIKIT时需要选择空间ID，示例：url: ezopen://open.ys7.com/abcde/1.cloud.rec?busType=7&spaceId=xxx 传入UIKIT链接：url+"&spaceId=xxx" |
| -expireTime | String | 直播地址有效期。expireTime参数为空时该字段无效 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 20001 | 通道不存在 | 通道不存在 |
| 20002 | 设备不存在 | 设备不存在 |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |
| 49999 | 数据异常 | 数据异常 |
| 60019 | 加密已开启 | 加密已开启 |
| 10001 | 无效参数 | 无效参数 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 10031 | 子账号或开发者用户无权限 | 子账号或开发者用户无权限 |