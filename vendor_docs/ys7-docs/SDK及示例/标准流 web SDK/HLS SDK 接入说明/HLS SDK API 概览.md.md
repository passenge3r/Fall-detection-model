# HLS SDK API 概览.md

> HLS SDK API 概览

> 更新时间: 2026-05-25T16:44:38.000+08:00

> 文档ID: 3714 | 来源树: SDK及示例

---

# HLS SDK API 概览

| API | 说明 | 类型 | 版本 |
| --- | --- | --- | --- |
| play | 播放 | play() => Promise | 0.1.0 |
| pause | 暂停 | pause() => void | 0.1.0 |
| fullscreen | 全屏（全局） | fullscreen() => Promise | 0.1.0 |
| exitFullscreen | 退出全屏（全局） | exitFullscreen() => Promise | 0.1.0 |
| resize | 调整尺寸 | resize(width: number, height: number) => Promise | 0.1.0 |
| setVolume | 设置音量大小 | setVolume(volume: number) => void | 0.1.0 |
| destroy | 销毁 | destroy() => void | 0.1.0 |
| setLogger | 设置日志打印 | setLogger(options: [LoggerOptions](https://www.npmjs.com/package/@ezuikit/utils-logger) ) => void | 0.1.0 |
| isPlaying | 当前的播放状态 | isPlaying() => boolean | 0.1.0 |
| getVersion | 获取播放器版本 | getVersion() => string | 0.1.0 |