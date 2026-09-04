# ezuikit-js 画面操作-录制.md

> 更新时间: 2026-05-25T16:44:30.000+08:00

> 文档ID: 4279 | 来源树: SDK及示例

---

# 录制

播放过程中录制画面，生成MP4文件下载到本地，或者获取MP4文件的Blob file数据。

使用录制功能时需要确保EZUIKit正在播放直播/预览画面。

**代码示例**

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
  downloadRecord: true, // 是否自动下载MP4至本地
  handleCapturePicture: (data) => {  // 截图监听事件，截图后返回结果
    console.log(data);
  }
});

// 开始录制
// fileName：文件名称，默认为结束录制时的时间戳
// validCode：验证码，录制加密视频时需要传入，否则会导致录制失败或MP4无法播放
player.startSave(fileName, validCode); 

//结束录制
player.stopSave();
```

#### 注意

- 8.0.5之前的EZUIKit版本直接录制设备的PS封装码流，需要用海康播放器VSPlayer进行播放。
- 8.0.5及之后的EZUIKit版本会在录制时将码流中转封装为普通MP4格式，可以在任意播放器、WEB浏览器中播放。