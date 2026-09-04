# FLV SDK API概览

> FLV SDK API概览

> 更新时间: 2026-05-25T16:44:37.000+08:00

> 文档ID: 3708 | 来源树: SDK及示例

---

# FLV SDK API 概览

| API | 说明 | 类型 | 版本 |
| --- | --- | --- | --- |
| play | 播放 | play(options?：string | [FlvOptions](https://ezviz-openbiz.github.io/EZUIKit-flv/global.html#FlvOptions)) => Promise | 1.0.0 |
| pause | 暂停 | pause() => Promise | 1.0.0 |
| resize | 重新调整视图大小 | play(options?) => Promise | 1.0.0 |
| setLogger | 设置日志打印 | setLogger(options: [LoggerOptions](https://www.npmjs.com/package/@ezuikit/utils-logger) ) => void | 1.0.2 |
| setVolume | 设置音量, 音量 0～1 | setVolume(Volume: number) => void | 1.0.0 |
| getVolume | 获取音量， 音量 0～1 | getVolume() => number | 1.0.0 |
| setRotate | 设置旋转角度，支持，0(默认), 90, 180, 270 四个值。 | setRotate(options?) => Promise | 1.0.0 |
| fullscreen | 设置全屏 | fullscreen(options?) => Promise | 1.0.2 |
| exitFullscreen | 取消全屏 | exitFullscreen(options?) => Promise | 1.0.2 |
| getState | 获取播放器的状态 | getState() => [Object](https://ezviz-openbiz.github.io/EZUIKit-flv/global.html#PlayerState) | 1.0.0 |
| getVersion | 获取版本 | getVersion() => string | 1.0.0 |
| destroy | 销毁 | destroy() => void | 1.0.0 |

[FLV API](https://ezviz-openbiz.github.io/EZUIKit-flv/EzuikitFlv.html)