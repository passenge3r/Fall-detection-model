# API-存储与媒体处理-云录制-图片采集与存储-时间点视频抽帧接口

> 更新时间: 2026-06-30T17:53:19.000+08:00

> 文档ID: 1389 | 来源树: 云存储

---

## 开始视频抽帧接口——按时间点抽帧

- 接口功能

   按时间点对视频进行抽帧。

   云端抽帧要求：需要去控制台创建存储空间(https://open.ys7.com/help/1975)或者通过接口创建(https://open.ys7.com/help/556)，其次需要接入云录制消息推送(https://open.ys7.com/help/1384)，然后开启云录制，抽帧指定时间区间内云端要求有录像。

   本地抽帧要求：设备有SD卡，抽帧指定时间区间范围内本地SD卡要求有录像。

- 请求地址

`https://open.ys7.com/api/v3/open/cloud/video/frame/timing/start`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID。projectId和resultSpaceId不能同时为空 | N |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | resultSpaceId | Long | 云抓拍业务空间id，由空间列表查询接口(https://open.ys7.com/help/5230)获取，projectId和resultSpaceId不能同时为空；如果resultSpaceId有效，则优先使用resultSpaceId保存到云抓拍存储空间 | N |
| Body | channelNo | Int | 通道号，默认可填1 | Y |
| Body | validateCode | String | 视频解密密钥，设备视频加密情况必需 | N |
| Body | recType | String | local-本地录像 cloud-云存储录像 live-实时 | Y |
| Body | devProto | String | 设备协议，若为空，标识萤石协议；若为gb28181，标识国标设备；默认为空 | N |
| Body | frameModel | Int | 抽帧模式，0：普通模式 1：错峰抽帧模式 2：抽I帧模式；不填默认:0 | N |
| Body | streamType | String | 码流类型，实时抽帧可以选择，1：高清（主码流）2：标清（子码流）；非实时帧建议选择1：高清（主码流）；默认为1 | N |
| Body | timingPoints | String | 抽帧时间点列表，格式: yyyyMMddHHmmss,yyyyMMddHHmmss，时间点以英文逗号分隔 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/open/cloud/video/frame/timing/start' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'projectId=001' \
--data-urlencode 'deviceSerial=G12262381' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'recType=cloud' \
--data-urlencode 'timingPoints=20230104163000,20230104163500'
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
        "taskId": "eba536dd28274723ac6870f16576a037"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 返回任务信息 |
| data.taskId | String | 任务ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |