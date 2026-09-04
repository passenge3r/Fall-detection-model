# 使用token鉴权

> 使用token鉴权

> 更新时间: 2026-05-25T16:36:29.000+08:00

> 文档ID: 2003 | 来源树: 音视频

---

# 使用token鉴权

![](https://resource.eziot.com/group2/M00/00/CD/CtwQFmWWTKGAN4vyAAFRFIRgzCA581.png)

## 服务端鉴权

开发者服务端在调用萤石云相关服务时，在接口中应该携带accesstoken用来验证开发者身份。

acsesstoken的获取的方式参考：[点击查看](/help/19)

accesstoken的授权范围是开发者的所有权限。

## 客户端鉴权

开发者客户端通过SDK与萤石云交互时，需要对每一次调用限定权限范围，可以通过JAVA SDK来指定授权范围，并生成token。

一个典型的入会token生成方法为：

```
GeneralResourceTokenGenerator generator = new GeneralResourceTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

GeneralResourceTokenParam param = new GeneralResourceTokenParam();
// 创建一个终端入会的action
Action joinRoomAction = new Action("ERTC_INFO");
//设置业务参数：strRoomId
joinRoomAction.setAttribute("strRoomId", "ID1699430483");
//设置业务参数：customId
joinRoomAction.setAttribute("customId", "7ca19da6c7164bc5ad7e0a");
param.addAction(joinRoomAction);
// 设置appid
param.setAppid("f758a146b2b24fc7b9705e232bce9f02");
// 设置过期时间，最长过期时间为604800秒（7天）
param.setExpire(604800);
String token = generator.generateToken(param);
```