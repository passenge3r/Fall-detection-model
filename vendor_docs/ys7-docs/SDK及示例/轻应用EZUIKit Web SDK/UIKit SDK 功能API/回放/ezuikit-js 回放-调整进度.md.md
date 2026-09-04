# ezuikit-js 回放-调整进度.md

> 更新时间: 2026-05-25T16:44:31.000+08:00

> 文档ID: 4283 | 来源树: SDK及示例

---

# 回放进度

回放时，支持通过拼接参数，或者通过拖动进度条跳转到指定的时间点开始播放。

## 时间轴UI

EZUIKit提供的官方WEB回放模板pcRec、H5回放模板mobileRec内置时间轴UI，展示当前设备的录像片段以及正在播放的时间点，可以通过拖动时间轴，跳转至指定时间开始播放，或点击日历图标切换播放日期。

WEB回放模板pcRec支持调整时间轴单位刻度对应的时间跨度大小。

## 时间跳转

可以在初始化阶段或者播放过程中，通过参数配置及API实现时间跳转。

**代码示例**

HTML：

```
<div id="ezuikit-player"></div>
```

JS：

```
import EZUIKit from 'ezuikit-js';

// 初始化播放器时指定开始、结束播放时间
const player = new EZUIKit.EZUIKitPlayer({
  id:"ezuikit-player",
  url: "ezopen://open.ys7.com/${设备序列号}/${通道号}.rec?begin=20250414000000&end=20250414120000",
  accessToken:"",
  template:"pcRec",
  width: 600,
  height: 400,
  accessToken:"",
  autoPlay: true,
  audio: true,
  download: true,
  downloadRecord: true
});

// 播放过程中切换开始、结束播放时间
player.changePlayUrl({url: "ezopen://open.ys7.com/${设备序列号}/${通道号}.rec?begin=20250414000000&end=20250414120000"});
```

## 注意

- 指定开始结束时间的格式为：YYYYMMDDhhmmss，如20250414000000表示2025年4月14日0点0分0秒。
- EZUIKit暂不支持指定跨天的录像回放。