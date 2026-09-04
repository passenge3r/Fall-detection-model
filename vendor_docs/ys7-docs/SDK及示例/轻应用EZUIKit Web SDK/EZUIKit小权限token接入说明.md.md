# EZUIKit小权限token接入说明.md

> EZUIKit小权限token接入说明

> 更新时间: 2026-05-25T16:44:29.000+08:00

> 文档ID: 4293 | 来源树: SDK及示例

---

# **一、说明**

- accessToken为B账号大token，具有当前账号下所有设备的操作权限，若希望限制token的权限范围或指定允许操作的设备，可以使用小权限token
- 接入小权限token需要具备前、后端开发能力
- 服务端集成Java SDK，开发接口用于生成小权限token
- 前端请求服务接口获取小权限token，在ezuikit初始化阶段按要求格式传入

# **二、生成token**

- ezuikit接收6个类型的小权限token，详情见下表
- 取流token、设备类-video token为取流播放必要token，若不传无法正常播放
- 其他token用于对讲、设备操作、模板详情获取等，可以不传，不影响核心的取流播放

| key | 类型 | 资源类型及规则参数 | 对应javaSDK中的类（https://open.ys7.com/help/1873） |
| --- | --- | --- | --- |
| streamToken.live | 预览取流token | { "actionType": "PREVIEW", "resourceCategory": "global" } | com.ezviz.open.sdk.auth.token.stream.StreamTokenGenerator |
| streamToken.rec | 回放取流token | { "actionType": "PLAYBACK", "resourceCategory": "global" } | com.ezviz.open.sdk.auth.token.stream.StreamTokenGenerator |
| streamToken.talk | 对讲token | { "actionType": "TALK", "resourceCategory": "global" } | com.ezviz.open.sdk.auth.token.stream.StreamTokenGenerator |
| deviceToken.video | 设备类-video资源 | { "action": "\*", "resourceCategory": "video" } | com.ezviz.open.sdk.auth.token.device.DeviceGeneralTokenGenerator |
| deviceToken.global | 设备类-global资源 | { "action": "\*", "resourceCategory": "global" } | com.ezviz.open.sdk.auth.token.device.DeviceGeneralTokenGenerator |
| httpToken.url | 非设备类 | { "urlPattern": "/\*\*" } | com.ezviz.open.sdk.auth.token.nondevice.NonDeviceOpsTokenGenerator |

# **三、传参**

### **3.1 参数格式**

- ezuikit要求初始化阶段以固定格式传入小权限token
- 具体格式及token资源类型可从ezuikit类的原型链中获取
- 格式如下

```
// 从ezuikit类中获取token格式及资源类型
console.log(EZUIKit.EZUIKitPlayer.prototype.tokenSchema)
 
EZUIKitPlayer.prototype.tokenSchema = {
 // 取流、对讲
 streamToken: {
 live: { "actionType": "PREVIEW", "resourceCategory": "global" },
 rec: { "actionType": "PLAYBACK", "resourceCategory": "global" },
 talk: { "actionType": "TALK", "resourceCategory": "global" }
 },
 // 设备类
 deviceToken: {
 video: { "action": "*", "resourceCategory": "video" },
 global: { "action": "*", "resourceCategory": "global" }
 },
 // 非设备类
 httpToken: {
 url: { "urlPattern": "/**" }
 }
};
```

### **3.2 初始化传参**

- 根据格式获取的token资源类型生成对应小权限token后，需要回填至结构体对象中
- 按原格式回传给ezuikit，启用小权限token，示例如下

```
const player = new EZUIKit.EZUIKitPlayer({
 id: "player",
 width: 600,
 height: 400,
 url: "ezopen://open.ys7.cpm/xxx/1.live",
 token: {
     // 取流、对讲
     streamToken: {
         live: "tk.xxx",
         rec: "tk.xxx",
         talk: "tk.xxx"
     },
     // 设备类
     deviceToken: {
         video: "tk.xxx",
         global: "tk.xxx"
     },
     // 非设备类
     httpToken: {
         url: "tk.xxx"
     }
 }
})
```

### **3.3 兼容性**

- ezuikit已处理向前兼容，保留了accessToken取流逻辑
- accessToken使用优先级高于小权限token，最终的token使用逻辑见下表

| 初始化时传入的token字段 | 结果 |
| --- | --- |
| accessToken+token | 使用accessToken |
| accessToken | 使用accessToken |
| token | 使用小权限token |
| 都没传 | 取流失败，报错 |