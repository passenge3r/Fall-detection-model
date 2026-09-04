# API-设备云组件仓-客流统计相机-多维客流设备删除

>  

> 更新时间: 2026-06-30T11:48:32.000+08:00

> 文档ID: 1547 | 来源树: OPEN_API

---

## 多维客流设备删除

- 接口功能

   将多维客流设备删除。

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/del`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | channelNo | String | 设备通道号 | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/devicekit/peoplecounting/del' \
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
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 20015 | 设备不支持该功能 | 设备不支持该功能 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |