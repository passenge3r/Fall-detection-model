# API-设备云组件仓-门禁-基础功能-更新人员扩展信息

> 更新时间: 2026-07-06T13:47:12.000+08:00

> 文档ID: 1104 | 来源树: OPEN_API

---

## 更新人员扩展信息

- 接口功能

   该接口用于更新人员扩展信息，需提前[开通云录制服务](https://open.ys7.com/help/354)存储图片，支持更新人脸与卡权限。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/ext/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Body | empId | String | 人员id | Y |
| Body | faceImageUrl | String | 图片url,优先使用url | N |
| Body | base64FaceImageFile | String | BASE64编码的图片数据:最大1.5M | N |
| Body | empType | Integer | 用户类型标识:1-管理员，2-普通用户，3-工程用户，4-来宾（访客），5-黑名单人，默认普通用户 | N |
| Body | closeDelayEnable | String | 是否关门延迟标识:0或false-否，1或true-是，默认否 | N |
| Body | maxOpenDoorTime | Integer | 最大认证次数 默认0 取值范围[0,255] | N |
| Body | validEnable | String | 有效期使能标识:0-使能，1-不使能 默认1,为0的时候beginTime和endTime不能为空 | N |
| Body | beginTime | String | 有效期起始日期时间格式:yyyy-MM-dd HH:mm:ss | N |
| Body | endTime | String | 有效期结束日期时间格式:yyyy-MM-dd HH:mm:ss | N |
| Body | userVerifyMode | String | 人员验证方式:仅支持face 默认face | N |
| Body | label | String | 标签,不支持""输入 | N |
| Body | remarks | String | 备注,不支持""输入 | N |
| Body | cardType | String | 卡片类型:1-普通卡,2-巡更卡,3-胁迫卡,4-超级卡,5-解除卡,6-应急管理卡,默认普通卡 | N |
| Body | cardNo | String | 卡号 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/company/member/ext/update' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'empId=97a3f9cddf63462bad98654b70b74491' \
--data-urlencode 'faceImageUrl=https://' \
--data-urlencode 'base64FaceImageFile=data:image/xxx;base64,body' \
--data-urlencode 'empType=' \
--data-urlencode 'closeDelayEnable=' \
--data-urlencode 'maxOpenDoorTime=' \
--data-urlencode 'validEnable=' \
--data-urlencode 'beginTime=' \
--data-urlencode 'endTime=' \
--data-urlencode 'userVerifyMode=' \
--data-urlencode 'label=' \
--data-urlencode 'remarks=' \
--data-urlencode 'cardType=' \
--data-urlencode 'cardNo='
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| data | Null | 返回数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |