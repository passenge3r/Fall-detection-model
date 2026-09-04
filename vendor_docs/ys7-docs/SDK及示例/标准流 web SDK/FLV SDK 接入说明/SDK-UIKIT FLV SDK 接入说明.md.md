# SDK-UIKIT FLV SDK 接入说明.md

> 更新时间: 2026-05-25T16:44:36.000+08:00

> 文档ID: 1812 | 来源树: SDK及示例

---

# FLV SDK 接入及使用说明

## npm 使用

```
npm install ezuikit-flv
```

### 初始化

```
import 'ezuikit-flv/style.css'; // @since 2.0.0
import EzuikitFlv from 'ezuikit-flv'

const player = new EzuikitFlv({
  url: 'play url', // https://play.com/9999.flv
  id: 'id', // support element id
  // decoder: 'decoder.js', // 自定义解码库加载地址， 默认放置在服务器根目录下
  autoPlay: true,
  // themeData: null // 忽略主题 @since 2.0.0
});
```

## umd使用

```
<!--  容器节点  -->
<div id='container-id'>
<!-- ezuikit-flv css file  `node_modules/ezuikit-flv/style.css`-->
<link rel="stylesheet" href="./style.css" />
<!-- ezuikit-js umd file  `node_modules/ezuikit-flv/index.js`-->
<script src='./index.js'></script>
<script>
const player = new EzuikitFlv({
    url: "play url", // https://play.com/9999.flv
    container: "container-id", // support element id or element
    // decoder: "decoder.js", // 自定义解码库加载地址， 默认放置在服务器根目录下
  // themeData: null // 忽略主题 @since 2.0.0
})

player.play()
</script>
```

## 开启硬解

```
// 初始化配置项， 如果浏览器不支持， 会自动切换到软解
useMSE: true
```

## 事件监听

- `error` 错误事件监听

```
player.on("error", (error) => {
    console.log(error)
})
```

  

| 错误类型 | 错误code | 错误描述 |
| --- | --- | --- |
| EzuikitFlv.fetchError | `NetworkError` | 请求错误 |
| EzuikitFlv.wasmDecodeError | `wasmDecodeError` | wasm 解码失败 |
| EzuikitFlv.playError | `playIsNotPauseOrUrlIsNull` | 播放失败 |

- `play` 播放

```
player.on("play", (info) => {
    console.log(info)
})
```

- `videoInfo` 视频流信息

```
player.on("videoInfo", (info) => {
    console.log(info)
})
```

- `audioInfo` 音频信息（仅软解）

```
player.on("audioInfo", (info) => {
    console.log(info)
})
```

- `fullscreen` 全屏/取消全屏

```
player.on("fullscreen", (info) => {
    console.log(info)
})
```

- 音量变化

```
player.on("volumechange", (volume, muted) => {
    console.log(volume, muted)
})
```

注意： 暂不提供CDN地址， decoder静态资源需要放置在自己的服务器下（`node_modules/ezuikit-flv`下 `decoder.wasm` 和 `decoder.js` 文件， 这两个文件需要在同一个文件夹下）

注意： 暂不提供CDN地址，decoder静态资源需要放置在自己的服务器下（`node_modules/ezuikit-flv`下 `decoder.wasm` 和 `decoder.js` 文件， 这两个文件需要在同一个文件夹下）

注意： 暂不提供CDN地址，decoder静态资源需要放置在自己的服务器下（`node_modules/ezuikit-flv`下 `decoder.wasm` 和 `decoder.js` 文件， 这两个文件需要在同一个文件夹下）

## 配置文档

初始化配置项，请查看github文档页：

[GITHUB options查看地址](https://ezviz-openbiz.github.io/EZUIKit-flv/global.html#FlvOptions)