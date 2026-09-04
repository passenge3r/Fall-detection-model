# EZOpenSDK-demo使用指南.md

> EZOpenSDK-demo使用指南

> 更新时间: 2026-06-02T14:03:35.000+08:00

> 文档ID: 4148 | 来源树: SDK及示例

---

# Demo使用指南

**注意：产品、技术支持、测试等非开发者可以下载安卓SDK包，将压缩包中的EzvizSDK-Demo.apk安装到安卓手机上后，即可进行体验或者测试。iOS 应用安装涉及到证书问题，由开发者使用自己公司的证书进行打包。**

## Demo和SDK下载

[点击下载](https://open.ys7.com/cn/s/download)

![下载页面](https://resource.eziot.com/group2/M00/01/00/CtwQF2fY2qGAYyVIAAIatA3GUoo682.png)

## Demo首页

![Demo首页](https://resource.eziot.com/group1/M00/01/84/CtwQEmfOUauAQBYFAAF9rSELcTI536.png)

  

登录页面中输入框信息说明：

| 输入框 | 是否必填 | 释义 |
| --- | --- | --- |
| 服务器区域 | 是 | 国内选择Asia-China，海外选择对应的区域。选择后ApiUrl和WebUrl会自动填充。 |
| ApiUrl |  | 选择"服务器区域"自动填充 |
| WebUrl |  | 选择"服务器区域"自动填充 |
| AppKey | 是 | [从开发者网站获取](https://open.ys7.com/console/application.html) |
| AccessToken | 是 | [从开发者网站获取](https://open.ys7.com/console/application.html) |
| 指定设备 |  | 输入一个序列号后，在设备列表里只会展示该设备！如果一个账号下设备很多，可能找不到某设备，建议输入该设备的序列号 |

  

输入以上3个必填项后，点击“开始体验！”，即可进入设备列表页面。

**注意**：此登录页面实为AppKey 和 AccessToken有效性的验证过程。点击“开始体验！”，调用的是EZOpenSDK.getDeviceList接口，如果接口能响应成功，说明AppKey 和 AccessToken有效，开发者可对账号下的设备进行取流、控制等操作。

## 设备列表页面

![设备列表页面](https://resource.eziot.com/group2/M00/00/FF/CtwQF2fOVKqALVD6AAKUT5dpMG0597.png)

**各个功能模块根据上图注释进入体验。**

## 各大区ApiUrl 和 AuthUrl

| 区域 | ApiUrl | AuthUrl |
| --- | --- | --- |
| 国内 | https://open.ys7.com | https://openauth.ys7.com |
| 海外 | https://open.ezvizlife.com | https://openauth.ezvizlife.com |
| 海外：俄罗斯 | https://irusopen.ezvizru.com | https://irusopenauth.ezvizru.com |
| 海外：亚洲 | https://isgpopen.ezvizlife.com | https://isgpopenauth.ezvizlife.com |
| 海外：北美洲 | https://iusopen.ezvizlife.com | https://iusopenauth.ezvizlife.com |
| 海外：南美洲 | https://isaopen.ezvizlife.com | https://isaopenauth.ezvizlife.com |
| 海外：欧洲 | https://ieuopen.ezvizlife.com | https://ieuopenauth.ezvizlife.com |

## Demo相关文件路径

### Android

rootPath=/sdcard/Android/data/ezviz.ezopensdk

码流文件路径：${rootPath}/files/streams

录像下载路径：${rootPath}/cache/0\_OpenSDK/Records

对讲码流路径：${rootPath}/files/talkback

录制码流路径：${rootPath}/cache/0\_OpenSDK/Records

调试日志路径：${rootPath}/files/0\_OpenSDK（必须打开手机的开发者模式！连接Android Studio的时候，也可以将Logcat中的信息Ctrl+A、Ctrl+C复制出来）

崩溃记录路径：${rootPath}/files/0\_OpenSDK/crash.txt

### iOS

码流文件路径：啄木鸟→SandBox→Documents/ezopensdk/EZSavedStreamData

录像下载路径：啄木鸟→SandBox→Documents/ezopensdk/DeviceRecord

对讲设备端码流：啄木鸟→SandBox→Documents/ezopensdk/EZSavedIntercomData/AudioDataFromDevice.data

对讲手机端码流：啄木鸟→SandBox→Documents/ezopensdk/EZSavedIntercomData/AudioDataFromiPhone.data

录制码流路径：啄木鸟→SandBox→tmp

调试日志路径：啄木鸟→SandBox→Documents/ezopensdk/Log（测试手机拔掉数据线，不要连接Xcode；否则日志输出路径是Xcode的调试栏区域）

崩溃记录路径：啄木鸟→Crash

### Harmony

rootPath=/data/app/el2/100/base/com.ezviz.videogo

码流文件路径：${rootPath}/haps/entry/cache/EZSavedStreamData

录像下载路径：${rootPath}/haps/entry/cache/DeviceRecord

对讲码流路径：${rootPath}/haps/entry/cache/EZSavedIntercomData

录制码流路径：${rootPath}/haps/entry/cache/LocalRecord

崩溃记录路径：${rootPath}/haps/entry/cache/CrashLog

## 萤石Demo工程日志获取

### 萤石Android Demo工程日志获取

#### 如果您是Android开发者：

1、请使用Android开发工具Android Studio运行压缩包中的EzvizSDK-Android工程；

2、复现问题后，选中Android Studio最下方工具栏中Logcat，使用Ctrl+A、Ctrl+C将Logcat中所有日志信息复制出来粘贴到txt文档中即可。
![Logcat日志](https://resource.eziot.com/group1/M00/01/91/CtwQE2itaEaAP3HMAANbdaW-Wfc810.png)

#### 如果您是产品、测试、技术支持等非Android开发人员：

1、请先打开您的安卓手机的开发者模式。每个品牌手机设置方式有所不同，请自行查询完成；

2、请在您的安卓手机上安装压缩包中的EzvizSDK-Demo.apk，安装成功后打开demo应用；

3、复现问题后，获取日志文件。文件路径：手机文件管理-Android/data/ezviz.ezopensdk/files/0\_OpenSDK

### 萤石iOS Demo工程日志获取

#### 如果您是iOS开发者：

1、请使用iOS开发工具Xcode运行压缩包中的EZOpenSDKDemo工程，Demo运行步骤请查看压缩包中的【README(集成必读).txt】文档；

2、复现问题后，打开Xcode最下方调试栏，使用Ctrl+A、Ctrl+C将Logcat中所有日志信息复制出来粘贴到txt文档中即可。
![iOS调试栏](https://resource.eziot.com/group1/M00/01/91/CtwQEmitbWuAPzacAARSbb_whK8486.png)

#### 如果您是产品、测试、技术支持等非iOS开发人员：

由于iOS证书的限制，萤石方无法提供iOS Demo安装包。

1、请先让您公司的iOS开发者给您安装iOS Demo应用；

2、复现问题后，获取日志文件。文件路径：应用屏幕上的啄木鸟→SandBox→Documents/ezopensdk/Log