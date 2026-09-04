# ezuikit-js 预览.md

> 更新时间: 2026-05-25T16:44:30.000+08:00

> 文档ID: 4284 | 来源树: SDK及示例

---

# 预览

实时从接入萤石云平台的设备取流，并在客户端解码播放设备当前画面。

## 1、初始化SDK

引入EZUIKit，初始化EZUIKit.EZUIKitPlayer模块

## 2、预览播放

默认状态下初始化成功后会自动开始播放

支持初始化EZUIKit.EZUIKitPlayer模块时传入【autoPlay:false】，配置不自动播放，后续手动调用play接口执行播放

## 3、结束播放

调用stop接口停止预览播放

## 4、销毁播放器

调用destroy接口销毁播放器实例，释放解码、样式、全局事件资源

**代码示例**

HTML：

```
<div id="ezuikit-player"></div>
```

JS：

```
import EZUIKit from 'ezuikit-js';

// 初始化播放器
const player = new EZUIKit.EZUIKitPlayer({
  id:"ezuikit-player",
  url: "ezopen://open.ys7.com/${设备序列号}/${通道号}.live",
  accessToken:"",
  template:"pcLive",
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken:"",
  autoPlay: true,
  audio: true,
  download: true,
  downloadRecord: true
});

// 开始播放（仅在autoPlay为false时需要调用）
player.play();

// 停止播放
player.stop()

// 销毁播放器
// 销毁api内置了停止播放、销毁DOM节点、释放资源逻辑
// 销毁SDK时直接调用destroy即可，无需额外调用stop或其他api
player.destroy();
```