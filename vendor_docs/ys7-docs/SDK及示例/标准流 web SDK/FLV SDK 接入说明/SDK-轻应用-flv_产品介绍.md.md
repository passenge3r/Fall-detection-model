# SDK-轻应用-flv_产品介绍.md

> SDK-轻应用-flv_产品介绍.md

> 更新时间: 2026-05-25T16:44:36.000+08:00

> 文档ID: 1852 | 来源树: SDK及示例

---

# Ezuikit-flv 产品介绍

ezuikit-flv 是一款开源的纯H5直播流播放器，通过Emscripten将音视频解码库编译成js（wasm) 运行于浏览器之中。兼容主流浏览器，可以运行在PC、手机、微信中，无需额外安装插件。

![Download](https://img.shields.io/npm/dm/ezuikit-flv.svg)

npm版本：![Version](https://img.shields.io/npm/v/ezuikit-flv.svg)

## 功能

- 支持解码H.264视频
- 支持解码H.265视频（FLV\_CODECID\_HEVC = 12, 定义FLV HEVC格式值为12）
- 支持2K视频
- 支持解码AAC音频
- 可设置播放缓冲区时长，可设置0缓冲极限低延迟（网络抖动会造成卡顿现象）
- 可创建多个播放实例
- 手机浏览器内打开长时间不会息屏
- 支持填充，等比，等比缩放 3种视频缩放模式
- 支持0，90，180，270度画面旋转
- 支持MediaSourceExtensions 硬件解码
- 支持MediaSourceExtensions硬解码失败的情况下自动切换到wasm软解码

### api文档

[GITHUB api文档查看地址](https://ezviz-openbiz.github.io/EZUIKit-flv/EzuikitFlv.html)

### examples

以下是我们提供的SDK demo，我们提供了目前主流的框架接入demo，若有其他框架请联系我们。

[base-app](https://github.com/Ezviz-OpenBiz/EZUIKit-flv/tree/master/examples/base-app)

[react-app](https://github.com/Ezviz-OpenBiz/EZUIKit-flv/tree/master/examples/react-app)

[vue-app](https://github.com/Ezviz-OpenBiz/EZUIKit-flv/tree/master/examples/vue-app)

uni-app 敬请期待

### 常见问题

- 初始化立即调用`play()` 不生效

  因为需要加载解码资源，`play` 不生效，可以设置 autoPlay= true
- 浏览器首次播放音频没有声音

  浏览器在首次播放音频时默认静音，需要人为触发一下页面（比如点击页面一下）， 浏览器本身的限制（有个别浏览器支持首次播放可以播放声音）
- 播放器（1.x 版本）为什么没有控件

  该SDK（1.x 版本）暂停不提供主题，仅提供api，主题开发者可以自己开发

  从2.x 版本开始已经支持主题
- 加载 wasm 为什么报错

  - 资源地址配置错误
  - 资源服务器不支持`content-type: application/wasm`