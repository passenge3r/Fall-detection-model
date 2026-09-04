# ezuikit-js 画面操作-截图.md

> 更新时间: 2026-05-25T16:44:29.000+08:00

> 文档ID: 4278 | 来源树: SDK及示例

---

# 截图 & 抓图

## 截图

播放过程中，在WEB浏览器端对当前画面进行截图操作，可直接下载图片到本地，或者获取图片的base64数据。

### 触发截图

EZUIKit官方提供的WEB预览模板pcLive、WEB回放模板pcRec、H5预览模板mobileLive、H5回放模板mobileRec均提供截图UI按钮，您也可以通过API触发截图。

可以通过以下2种方法获取截图结果：  
1、初始化SDK的时候传入handleCapturePicture回调方法  
2、初始化SDK时绑定截图接口的事件监听器

**代码示例**

```
import EZUIKit from "ezuikit-js";

// 初始化播放器时注册截图监听事件
const player = new EZUIKit.EZUIKitPlayer({
  id:"ezuikit-player",
  url: "ezopen://open.ys7.com/${设备序列号}/${通道号}.live",
  accessToken:" ",
  template:"pcLive",
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken:"",
  autoPlay: true,
  audio: true,
  download: true, // 是否自动下载图片至本地
  downloadRecord: true,
  handleCapturePicture: (res) => {  // 方法一：传入截图监听事件，截图后返回结果
    console.log("capturePicture callback:", res);
  }
});

// 方法二：注册截图监听事件
player.eventEmitter.on("capturePicture", (res) => { console.log("capturePicture eventEmitter callback:", res); });

// 调用截图API触发截图功能
player.capturePicture();
```

## 抓图

给在线设备下发信令，让设备上传当前图片到云端存储，**抓图将在服务器端保留2个小时**；返回值为图片的url地址。

抓图功能不依赖EZUIKit的初始化播放，可以直接通过OPEN API触发，参考：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/687)。