# 音频格式转码为AAC

> 更新时间: 2026-06-23T16:55:03.000+08:00

> 文档ID: 3735 | 来源树: OPEN_API

---

## 音频格式转码为AAC

- 接口功能

如果设备只支持AAC音频格式，需要调用该接口将音频格式转码为AAC，该接口支持设备级别以及通道级别。

- 接口说明

1、海康/萤石设备大部分设备出厂都是G.711的音频编码，集成SDK时，开放平台提供了对应音频编码的播放功能，具体可以集成SDK：[SDK集成](https://open.ys7.com/doc/zh/book/index/user.html)

2、若使用标准流RTMP时，直接在微信小程序端直接播放，则可能会遇到设备无法播放声音的情况，这时候需要将设备音频编码修改为AAC，目前开放平台提供了两个方法进行设置

方法1：海康设备可以通过连接本地配置，在 配置 - 视音频配置 - 音频里，修改音频编码，即可完成修改

萤石设备可以通过萤石工作室完成配置

通过接口修改：<https://open.ys7.com/help/2372> 该接口目前只支持部分设备，修改前请校验能力集

方法2：若开发者只需要修改RTMP编码，则可以使用本文档接口 <https://open.ys7.com/help/3735>

该接口由于需要云端消耗资源，因此是计费接口，计费价格请联系客服

由于该接口目前只针对RTMP，其他标准流HLS的音频暂不支持，请先使用 方法1

- 收费说明

| 名称 | 类型 | 价格 |
| --- | --- | --- |
| 收费政策 | 针对上云的设备，若其为G.711音频编码，平台提供云端转码AAC能力，从而满足视频播放时播放声音的需求 | 自2024年12月起开始限时免费提供，正式收费之前会提前通知 |

- 请求地址

`https://open.ys7.com/api/service/media/aac/transfer`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | Int | 实际取流通道，单目IPC：1，多目IPC或NVR则是具体需要转码的取流通道。不传默认使用0：仅全新未取过流的设备会即时生效，已取流的最多延迟3天生效（业务场景不建议使用） | N |
| query | enable | Int | 0-关闭音频格式转码为AAC，1-开启音频格式转码为AAC | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/media/aac/transfer?enable=1' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: L12345678' \
--header 'localIndex: 1'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应元信息 |
| meta.code | Int | 响应状态码 |
| meta.message | String | 响应消息 |
| meta.moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请求参数错误 |
| 10002 | accessToken过期或异常 | 令牌失效 |
| 10031 | 账号无权限访问此设备 | 权限不足 |
| 50000 | 服务异常 | 服务器异常 |
| 20002 | 设备不存在 | 设备未注册 |
| 20001 | 通道不存在 | 通道号错误 |