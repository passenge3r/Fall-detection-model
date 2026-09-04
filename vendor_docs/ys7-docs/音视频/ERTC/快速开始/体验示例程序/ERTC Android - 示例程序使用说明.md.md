# ERTC Android - 示例程序使用说明.md

> Demo使用说明

> 更新时间: 2026-05-25T16:36:28.000+08:00

> 文档ID: 1977 | 来源树: 音视频

---

# ERTC Android - 示例程序使用说明

在正式使⽤ERTC服务之前，你可以使⽤我们提前编译好的⽰例程序来体验基本功能。

## 1、下载示例程序

### (1) Android示例程序：[点击下载](https://open.ys7.com/cn/s/download#:~:text=%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97-,%E8%90%A4%E7%9F%B3%E5%AE%9E%E6%97%B6%E9%9F%B3%E8%A7%86%E9%A2%91ERTC,-Windows(C%2B%2B))

### (2) 使用微信扫描下面二维码

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUxvmALs9GAAAMDbNTJXg250.png)

## 2、填写AppID字段

### a. 进入示例程序首页

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WTyvWAMZbwAADEUqSpdLM389.png)

### b. 填写AppID字段

成功创建项⽬后，萤⽯云会给每个项⽬⾃动分配⼀个APP ID作为项⽬唯⼀标识。你可以在项⽬管理⻚⾯查看项⽬的App ID。
![file tree](https://resource.eziot.com/group2/M00/00/CC/CtwQFmWOJ5yAEI0xAAEnKFzLGbM670.jpg)

## 3、加入房间

点击“会议Demo”按钮进入到加入会议页面,填写会议ID、用户ID，Token根据会议ID、用户ID在官网生成

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQEmWTy-aAUSaNAAHifZ4QLkA465.png)

在我们已经开启的ERTC项⽬中，我们⽤roomid区分不同的会话，userid区分不同的⽤户。加⼊相同roomid的不同⽤户将被拉⼊同⼀个会话。

## 4、打开本地摄像头

开启本地摄像头，点击如下按钮：

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WTzN-AcIODAADczkVp0xc182.png)

## 5、打开本地麦克风

开启本地麦克风，点击如下按钮：

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQEmWTzNyAQqG7AADYGIZMDZ0117.png)

## 6、开启屏幕共享

开启屏幕共享，点击如下按钮：

![file tree](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WTzNiATHUIAAEBlwvC9MM602.png)

## 7、订阅

- 当远端用户开启摄像头时，本示例程序会自动订阅远端用户的视频
- 当远端用户开启麦克风时，本示例程序会自动订阅远端用户的音频
- 当远端用户开启屏幕共享时，本示例程序会自动订阅远端用户的屏幕共享