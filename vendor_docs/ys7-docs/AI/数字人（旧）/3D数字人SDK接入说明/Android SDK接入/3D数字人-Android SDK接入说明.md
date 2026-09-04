# 3D数字人-Android SDK接入说明

> 3D数字人-Android SDK接入说明

> 更新时间: 2026-05-25T16:37:56.000+08:00

> 文档ID: 2426 | 来源树: AI

---

# 3D数字人 Android 云渲染SDK

> 目前3D数字人 Android端主要是支持云渲染，端渲染主要应用在类似于中控屏等设备上，对设备性能有一定要求，因此目前Android端渲染SDK未对外开放，可以参考云渲染SDK，或者联系客服获取端渲染SDK

### 一. 准备工作

#### 1.1 账号注册

进入萤石云开放平台<https://open.ys7.com/cn/s/index> , 进行账号注册 ;

#### 1.2 获取AccessToken

1. 进入萤石开放平台->控制台->基础服务->账号中心->应用信息->获取AppKey、Secret；

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086096744_image.png)

2. 点击“通过接口获取”，进入<https://open.ys7.com/help/19>，根据接口获取AccessToken；

#### 1.3 创建数字人项目

3. 进入萤石开放平台->控制台->产品中心->AI服务->数字人->会话互动

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086252086_image_1.png)

2. 获取appId

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086261769_image_2.png)

3. 购买2d互动数字人并发,获取uid(请联系产品经理开通对应的并发)

### 二.如何接入

#### 2.1 集成环境

4. 接入语言: Kotlin/JAVA
5. 库名称: ezviz-dh-release.aar
6. 环境准备:支持 Android minsdk 28
7. 开发环境: Android Studio 2.6及以上
8. NDK支持架构: armeabi-v7a, arm64-v8a