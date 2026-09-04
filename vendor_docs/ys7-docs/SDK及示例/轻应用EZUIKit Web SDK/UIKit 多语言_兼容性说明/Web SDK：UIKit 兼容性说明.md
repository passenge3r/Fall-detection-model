# Web SDK：UIKit 兼容性说明

> UIKit Javascript 

> 更新时间: 2026-07-01T11:53:53.000+08:00

> 文档ID: 31 | 来源树: SDK及示例

---

# Web SDK：UIKit 兼容性说明

## 简介

UIKit，是基于萤石开放平台OpenSDK封装的UI组件，使用过程中不必学习专业的业务概念，更不用调用繁琐的接口，能够以极简的嵌入方式，快速在您的应用中集成视频功能。

## 适用协议

UIKit适用于开放平台[EZOPEN协议](https://open.ys7.com/help/23)私有协议视频。

## 兼容性说明

### 适用浏览器

UIKIt 采用浏览器 WebAssembly 特性，通过浏览器端上解析视频流，支持情况参考：

### 浏览器支持

#### PC端

- Chrome 57+
- Firefox 52+

#### 移动端：

- 谷歌chrome内核浏览器(谷歌浏览器移动版，微信内置浏览器）
- IOS Webkit 内核浏览器 (谷歌浏览器移动版，微信内置浏览器， Safari浏览器）
- 鸿蒙手机内核浏览器（鸿蒙自带浏览器，微信内置浏览器）

### 浏览器支持参考 [【can i use WebAssembly】](https://caniuse.com/?search=WebAssembly)

![](https://izhstatic.ys7.com/vasp-openweb/1782720508165_image_29.png)

#### 移动端

因手机性能差异部分手机机型存在不兼容情况，我们提供测试结论供参考，屏幕空间有限，建议仅初始化和播放可见区域视频实例，避免额外的性能消耗。

测试机型：

- 安卓：vivo s15e、vivo x60、红米K40、三星note10+、红米note7、oppo A37m、oppo reno4、小米8
- ios：iphone x、iphone12、iphone11、iphone xs max
- 鸿蒙：华为mate30

相关兼容性问题如下：

- 三星note10+（安卓11）、红米note7（安卓11）、红米K40自带浏览器无法打开H5预览/回放页面
- oppo A37m（安卓5）自带浏览器可以打开H5预览/回访页面，无画面显示
- 华为mate30 清晰度切换UI兼容性有问题
- oppo reno4 云台控制方向移动会额外显示一个框
- 小米8可以打开H5预览/回放页面,但无法加载画面

## 各类国产系统及浏览器的 WebAssembly 支持情况

| 系统/浏览器 | 内核类型 | WebAssembly 支持情况 |
| --- | --- | --- |
| 麒麟 / 银河麒麟（Kylin / NeoKylin） | 基于 Chromium / Firefox 内核 | 如果是新版 Chromium 内核（Chrome 90+），支持；老版本可能不支持或不完全支持 |
| 统信 UOS（UOS） | Chromium / Firefox | 新版本 Chromium 内核支持 |
| 深度 Deepin (DDE) | Chromium 内核 | 新版支持 |
| 中国版 IE（国产安全 IE） | Trident 内核（老 IE 核心） | 不支持 |
| 国产安全浏览器 / 360 浏览器 / 猎豹等 | 多为双核（Trident + Chromium） | Chromium 核心部分新版支持；WebAssembly 支持；老 Trident 核心不支持 |

## 更新日志可能不及时，请关注最新版本UIKit版本更新内容，关注发布功能