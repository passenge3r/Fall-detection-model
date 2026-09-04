# ezuikit-js 预览-清晰度.md

> 更新时间: 2026-05-25T16:44:30.000+08:00

> 文档ID: 4285 | 来源树: SDK及示例

---

# 清晰度

一般摄像头支持多种视频清晰度，比如：标清、高清、超清、极清等，可以通过指令控制设备端推送不同清晰度的流实现清晰度切换。

## 指定清晰度

EZUIKit支持在初始化阶段通过参数配置目标清晰度。

## 清晰度切换

EZUIKit支持播放过程中通过按钮、API切换播放清晰度。

**代码示例**

```
import EZUIKit from 'ezuikit-js';

// 初始化播放器时指定清晰度quality
// 0: 流畅； 1: 标清; 2: 高清; 3: 超清; 4: 极清; 5: 3K; 6:4K; "pp"： "性能优先 (Performance Priority)"; "qp": "画质优先(Quality Priority)"
const player = new EZUIKit.EZUIKitPlayer({
  id:"ezuikit-player",
  url: "ezopen://open.ys7.com/${设备序列号}/${通道号}.live",
  accessToken: "",
  template: "pcLive",
  quality: 2,
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken: "",
  autoPlay: true,
  audio: true,
  download: true,
  downloadRecord: true
});

// 调用截图API触发截图功能
// videoLevel：目标清晰度，
player.changeVideoLevel(videoLevel);
```

## 注意

- 8.0.5之前的版本通过url中拼接【hd】标识决定从主码流/子码流取流，从而实现高清、标清的切换。
- 8.0.5及之后的版本会向设备查询当前支持的清晰度并渲染对应选项，切换清晰度时发送对应的切换指令给设备。
- 由于设备端一般只会推送同一个清晰度的流，因此在使用8.0.5及之后的版本时，当多人同时观看同一个设备画面，如果某个用户切换了清晰度，所有客户端的观看清晰度都会同时变化。