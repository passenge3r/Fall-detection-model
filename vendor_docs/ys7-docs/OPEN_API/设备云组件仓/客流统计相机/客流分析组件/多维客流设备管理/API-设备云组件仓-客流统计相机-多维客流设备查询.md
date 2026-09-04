# API-设备云组件仓-客流统计相机-多维客流设备查询

>  

> 更新时间: 2026-06-30T11:48:30.000+08:00

> 文档ID: 1546 | 来源树: OPEN_API

---

## 多维客流设备查询

- 接口功能

   查询多维客流设备详细信息。

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/find`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | channelNo | String | 设备通道号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/peoplecounting/find' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G12345678' \
--header 'channelNo: 1'
```

- 返回数据

```
{
    "meta": {
        "code": 0,
        "message": "string"
    },
    "data": {
        "id": 0,
        "deviceSerial": "string",
        "channelNo": "string",
        "deviceName": "string",
        "regionTag": "string",
        "addTime": "string",
        "status": 1,
        "enable": true,
        "createTime": "string",
        "updateTime": "string"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 响应码值 |
| meta.message | String | 提示信息 |
| data | Object | 响应数据 |
| data.id | Int | 索引id |
| data.deviceSerial | String | 设备序列号 |
| data.channelNo | String | 设备通道号 |
| data.deviceName | String | 设备名称 |
| data.regionTag | String | 绑定区域 |
| data.addTime | String | 设备添加时间 |
| data.status | Int | 设备在线状态 0-不在线，1-在线 |
| data.enable | Boolean | 客流开关状态，true-开启 false-关闭 |
| data.createTime | String | 创建时间 |
| data.updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 20015 | 设备不支持该功能 | 设备不支持该功能 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |