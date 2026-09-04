# 获取AccessToken

> 更新时间: 2026-06-01T16:48:46.000+08:00

> 文档ID: 81 | 来源树: OPEN_API

---

## 根据appKey和secret获取accessToken

- 接口功能

该接口用于管理员账号根据 `appKey` 和 `appSecret` 获取 `accessToken`，`appKey` 和 `appSecret` 可在官网-开发者服务-[我的应用](https://open.ys7.com/console/application.html)中获取。

> 注意：① AccessToken，即访问令牌，是接口调用必备的公共参数之一，用于校验接口访问/调用是否有权限，有效期为 7 天，有效期内不需要重复申请，可以重复使用；② 有效期 7 天无法变更，请在业务端使用 AccessToken 的场景中，建立校验老 Token 有效性和失效后重新获取 Token 的机制；③ 新获取 Token 不会使老 Token 失效，每个 Token 独立拥有 7 天生命周期；④ 由于 Token 属于用户身份认证令牌，在用户变更身份信息（用户注销、密码修改）后会将旧的 Token 进行失效处理。

> 注意：请在即将过期或接口报错 10002 时重新获取 accessToken，请勿频繁调用避免占用过多接口调用次数。最佳实践是在本地进行缓存，给对应有权限的用户使用，而不是在每次使用业务接口前获取一次。

- 请求地址

`https://open.ys7.com/api/lapp/token/get`

- 请求方式

`POST`

- 请求参数

| 位置 | 参数名 | 类型 | 说明 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | appKey | String | 应用唯一标识，可在官网-开发者服务-[我的应用](https://open.ys7.com/console/application.html)中获取 | Y |
| Body | appSecret | String | 应用密钥，可在官网-开发者服务-[我的应用](https://open.ys7.com/console/application.html)中获取 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/token/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'appKey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
--data-urlencode 'appSecret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

- 返回数据

```
{
    "data": {
        "accessToken": "at.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "expireTime": 1470810222045
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| accessToken | String | 获取到的 accessToken |
| expireTime | Long | accessToken 过期时间，毫秒级时间戳 |

- 返回码

| 返回码 | 返回消息 | 详细描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10005 | appKey异常 | appKey 被冻结 |
| 10017 | appKey不存在 | 确认 appKey 是否正确 |
| 10030 | appKey和appSecret不匹配 | appKey 与 appSecret 不一致，请检查或重新生成 |
| 49999 | 数据异常 | 接口调用异常 |