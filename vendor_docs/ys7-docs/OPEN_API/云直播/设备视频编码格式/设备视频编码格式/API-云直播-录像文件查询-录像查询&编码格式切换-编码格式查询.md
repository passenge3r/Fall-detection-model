# API-云直播-录像文件查询-录像查询&编码格式切换-编码格式查询

> 更新时间: 2026-07-31T17:39:27.000+08:00

> 文档ID: 1595 | 来源树: OPEN_API

---

## 编码格式查询

- 接口功能

设备视频编码格式查询接口。该API支持托管设备，需要授予托管权限：CONFIG

- 请求地址

`https://open.ys7.com/api/v3/das/device/video/encode`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | channelNo | Int | 通道号，默认为1 | N |
| query | streamType | Int | 码流，1-主码流，2-子码流 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/das/device/video/encode?streamType=1' \
--header 'deviceSerial: XXXXX' \
--header 'channelNo: 1' \
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
        "videoCode": 1
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |
| data | Object | 响应体 |
| data.videoCode | Int | 编码格式，0-私有H264，1-标准H264，2-标准MPEG4，3-标准MPEG2，4-MJPEG，5-标准H265，6-SMART264，7-SMART265（常见为标准H264(1)和标准H265(5)） |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 10002 | accessToken异常或过期 | 请重新获取accessToken |
| 10005 | appKey异常 | 请检查appKey |
| 20001 | 通道不存在 | 请检查通道号 |
| 20006 | 网络异常 | 请检查网络 |
| 20007 | 设备不在线 | 请检查设备在线状态 |
| 20008 | 设备响应超时 | 请重试 |
| 20014 | deviceSerial不合法 | 请检查设备序列号 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 60020 | 不支持该命令 | 设备不支持该命令 |