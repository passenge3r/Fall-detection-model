# 设置长时间未体动时间（PUT）

>  

> 更新时间: 2026-06-22T10:26:41.000+08:00

> 文档ID: 3990 | 来源树: OPEN_API

---

## 设置长时间未体动时间

- 接口功能

   设置长时间未体动时间

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/SleepDetector/MotionLessDuration`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | data | Int | 长时间未体动时间 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/SleepDetector/MotionLessDuration'
--header 'accessToken: at.xxxxx'
--header 'Content-Type: application/json'
--data-raw '60'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "成功",
    "moreInfo": {
      "deviceMeta": {
        "code": "0x00000000",
        "errorMsg": "Succeeded."
      }
    }
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |