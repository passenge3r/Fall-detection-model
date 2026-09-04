# API-通用AI-人证核验-身份证二要素认证接口

> 更新时间: 2026-07-01T18:45:06.000+08:00

> 文档ID: 1345 | 来源树: AI

---

## 身份证二要素认证接口

- 接口功能

   输入身份证号与对应姓名，通过公安库认证，返回是否一致。

- 请求地址

`https://open.ys7.com/api/component/certificate/alp/cc`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | bizCode | String | 业务码 | Y |
| Body | name | String | 姓名 | Y |
| Body | cardno | String | 身份证号码 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/component/certificate/alp/cc?bizCode=xxxxx&accessToken=at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=张三' \
--data-urlencode 'cardno=330100199001010000'
```

- 返回数据

```
{
    "resultflow": "xxxxxxxxxxxxx",
    "code": "1",
    "msg": "验证一致"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 响应码 |
| msg | String | 返回信息 |
| resultflow | String | 结果流水号 |

- 返回码

| 返回码 | 返回消息 | 描述（是否通过公安认证） |
| --- | --- | --- |
| 1 | 验证一致 | 是 |
| 0 | 身份证信息有误 | 是 |
| -1 | 身份证信息与人像不匹配 | 是 |
| 2 | 失败，照片对比不一致 | 是 |
| 4 | 失败，身份证信息不一致 | 是 |
| 5 | 失败，证件不存在 | 是 |
| 6 | 失败，照片质量不佳 | 是 |
| 1001 | 请求参数格式错误 | 否 |
| 1002 | 用户名密码错误 | 否 |
| 1004 | 签名校验不通过，数据错误 | 否 |
| 1005 | 图片大小不符 | 否 |
| 1006 | 图像格式不支持 | 否 |
| 2002 | 连接数过多 | 否 |
| 2005 | 数据超时 | 否 |
| 4001 | 业务代码异常 | 否 |
| 4002 | 无权访问，请联系客服人员 | 否 |
| 9999 | 系统错误，或系统无法识别请求信息 | 否 |
| 10002 | accessToken异常或过期 | 否 |
| 50000 | 服务出现未知响应 | 否 |