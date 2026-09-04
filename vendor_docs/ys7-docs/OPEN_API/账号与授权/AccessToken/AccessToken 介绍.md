# AccessToken 介绍

> AccessToken

> 更新时间: 2026-05-25T16:38:00.000+08:00

> 文档ID: 19 | 来源树: OPEN_API

---

# AccessToken

AccessToken，即访问令牌。接口调用必备的公共参数之一，用于校验接口访问/调用是否有权限，有效期为7天，有效期内不需要重复申请，可以重复使用。  
有效期7天无法变更，请在业务端使用AccessToken的场景中，校验老Token的有效性和失效时重新获取Token的机制；  
新获取Token不会使老Token失效，每个Token独立拥有7天生命周期

> F:能否拥有无时间限制的token？  
> A:不能，token有效期是出于安全角度考虑，保障您在不规范操作后导致token泄露后能够将损失降至最小的策略

萤石支持两种oAuth授权方式获取AccessToken（推荐使用方式1 Client Credentials Grant）：

1. Client Credentials Grant

使用AppKey和Secret直接换取AccessToken，一般在服务端调用（出于安全考虑）再由您自己的云服务下发给客户端SDK使用，
接口见：[获取Token](/help/81)，
RFC 6749（oAuth标准）解释见：[Client Credentials Grant](https://tools.ietf.org/html/rfc6749#section-4.4)

```
     +---------+                                  +---------------+
     |         |                                  |               |
     |         |>--(A)- Client Authentication --->| Authorization |
     | Client  |                                  |     Server    |
     |         |<--(B)---- Access Token ---------<|               |
     |         |                                  |               |
     +---------+                                  +---------------+
```

2. Implicit Grant

使用客户端SDK嵌入的H5登录页，用户登录后SDK可以获取到AccessToken，
注意：这里需要您的应用使用萤石账户体系，如无需和萤石账户互动，请使用Client Credentials Grant方式。
接口见SDK的API文档，RFC 6749（oAuth标准）解释见：[Implicit Grant](https://tools.ietf.org/html/rfc6749#section-4.2)

```
     +----------+
     | Resource |
     |  Owner   |
     |          |
     +----------+
          ^
          |
         (B)
     +----|-----+          Client Identifier     +---------------+
     |         -+----(A)-- & Redirection URI --->|               |
     |  User-   |                                | Authorization |
     |  Agent  -|----(B)-- User authenticates -->|     Server    |
     |          |                                |               |
     |          |<---(C)--- Redirection URI ----<|               |
     |          |          with Access Token     +---------------+
     |          |            in Fragment
     |          |                                +---------------+
     |          |----(D)--- Redirection URI ---->|   Web-Hosted  |
     |          |          without Fragment      |     Client    |
     |          |                                |    Resource   |
     |     (F)  |<---(E)------- Script ---------<|               |
     |          |                                +---------------+
     +-|--------+
       |    |
      (A)  (G) Access Token
       |    |
       ^    v
     +---------+
     |         |
     |  Client |
     |         |
     +---------+
```

## 接口获取

请查看[API接口文档](/help/81)

## 官网获取

为了方便开发者试用，在开放平台官网也可以手动获取accessToken:
开发者服务-我的应用-应用秘钥