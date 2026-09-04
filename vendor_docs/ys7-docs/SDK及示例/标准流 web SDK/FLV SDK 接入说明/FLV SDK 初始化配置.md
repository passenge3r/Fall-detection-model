# FLV SDK 初始化配置

> FLV SDK 初始化配置

> 更新时间: 2026-05-25T16:44:36.000+08:00

> 文档ID: 3711 | 来源树: SDK及示例

---

# FLV SDK 初始化配置

| option | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| container | string | HTMLElement |  | 渲染容器 |
| id | string |  | 渲染容器id 优先级比 container 高 |
| videoBuffer | number | 可选 | 设置最大缓冲时长，单位秒，播放器会自动消除延迟。 |
| decoder | string | 可选 | 解码库worker地址 默认 decoder.js, wasm 文件要和decoder在同一个文件夹中 |
| staticPath | string | 可选 | 静态资源的了路径 |
| autoPlay | boolean | 可选 | 自动播放 默认false |
| hasAudio | boolean | 可选 | 是否有音频，如果设置false，则不对音频数据解码，提升性能。 |
| volume | number | 可选 | 音量大小, 默认 0.8。 |
| debug | boolean | 可选 | 是否开启控制台调试打印。默认 false |
| timeout | number | 可选 | 设置超时时长, 单位秒, 在连接成功之前(loading)和播放中途(heart),如果超过设定时长无数据返回,则回调timeout事件。默认 10 |
| heartTimeout | number | 可选 | 设置超时时长, 单位秒， 播放中途,如果超过设定时长无数据返回,则回调timeout事件。默认 5 |
| heartTimeoutReplayTimes | number | 可选 | heartTimeoutReplay 重试次数。默认 3 |
| loadingTimeout | number | 可选 | 设置超时时长, 单位秒。默认 10 |
| loadingTimeoutReplay | boolean | 可选 | 是否开启loading超时之后自动再播放, 默认 true |
| keepScreenOn | boolean | 可选 | 开启屏幕常亮，在手机浏览器上, canvas标签渲染视频并不会像video标签那样保持屏幕常亮。默认 false |
| muted | boolean | 可选 | 是否开启声音，默认是关闭声音播放的。默认 true |
| useMSE | boolean | 可选 | 是否开启MediaSource硬解码。视频编码只支持H.264视频（Safari on iOS不支持）。默认 false |
| themeData | [Object](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/blob/master/themeData.md) | 可选 | 是否自定义主题。 |

[详细 FLV 配置项](https://ezviz-openbiz.github.io/EZUIKit-flv/EzuikitFlv.html)