# digital-websdk接入引导

> digital-websdk接入引导

> 更新时间: 2026-05-25T16:37:54.000+08:00

> 文档ID: 2850 | 来源树: AI

---

# 接入引导

> 本教程基于 1.x 版本

本章主要介绍如何快速地将萤石数字人SDK集成到您的项目中。

## 准备工作

### 1.1 账号注册

进入萤石云开放平台https://open.ys7.com/cn/s/index，进行账号注册

### 1.2 获取AccessToken

1.2.1 进入萤石开放平台->控制台->基础服务->账号中心->应用信息->获取AppKey、Secret  
  
![](https://appres.ys7.com/AppYs-SmartCustomerService/1718086096744_image.png)
  
1.2.2 点击“通过接口获取”，进入https://open.ys7.com/help/19，根据接口获取AccessToken

### 1.3 创建数字人项目

1.3.1 进入萤石开放平台->控制台->产品中心->AI服务->数字人->会话互动  
  
![](https://appres.ys7.com/AppYs-SmartCustomerService/1718086252086_image_1.png)  
1.3.2 获取appId
  
![](https://appres.ys7.com/AppYs-SmartCustomerService/1718086261769_image_2.png)  
1.3.3 购买2d互动数字人并发,获取uid(请联系产品经理开通对应的并发)

## 项目接入

### npm 集成

1. 您可以在项目中使用 `npm` 安装 `digital-websdk`。

```
npm install digital-websdk
```

2. 初始化

```
import DigitalWebsdk from 'digital-websdk'

const digitalSDK = new DigitalWebsdk()
```

### API 调用

#### 启动数字人

```
digitalSDK.createSession({
  accessToken: xxxx,
  appId: xxx,
  uid: xxx,
  element: "my-player",
})
.then()
.catch();
// 返回promise
```

  

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| accessToken | 开放平台accessToken | 在开放平台控制台获取，或[接口获取](/help/19) | string | at.d8yfi7bb1d1p5aw7v8oztfdsa1djra0n46-5mnfk598bc-0annlcz-a3gi2pj | 是 |
| appId | 数字人应用id | 在开放平台控制台创建数字人项目获取 | string | ebadss8529d954813214d3cb4192d3c781 | 是 |
| uid | 设备唯一标识 | 购买2d互动数字人并发,获取uid(请联系产品经理开通对应的并发) | string | "12345" | 是 |
| element | dom元素ID | - | string | "my-player" | 是 |

#### 驱动数字人语音播报

```
digitalSDK.play({
  data: "text",
  interrupt: true, // 是否打断上一次播报，可配合data传空字符串，停止当前播报
});
// 无返回值
```

#### 关闭数字人

```
digitalSDK.closeSession()
// 无返回值
```

#### 事件监听

```
sdk.on("error", (msg) => {
  // msg: { code: xxx, message: xxx }
  // 详情看错误码规范
});
sdk.on("load", (msg) => {
  // 数字人加载成功
});
sdk.on("reconnecting", (msg) => {
  if (msg.count >= 30) {
    // 网络重连失败
  } else {
    // 网络正在重连，重连次数：count
  }
});
```