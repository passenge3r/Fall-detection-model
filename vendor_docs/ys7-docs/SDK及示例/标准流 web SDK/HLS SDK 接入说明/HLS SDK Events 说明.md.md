# HLS SDK Events 说明.md

> HLS SDK Events 说明

> 更新时间: 2026-05-25T16:44:39.000+08:00

> 文档ID: 3716 | 来源树: SDK及示例

---

# HLS SDK Events 说明

| 事件 | 描述 | 支持 |
| --- | --- | --- |
| init | 初始化触发 | H264/H265 |
| volumeChange | 音量变化触发 | H264/H265 |
| wasm\_loaded | wasm 加载完成触发 | H264/H265 |
| wasm\_failed | wasm 加载失败触发 | H264/H265 |
| canplay | 音量变化触发 | H264 |
| loadeddata | 播放位置的视频帧（通常是第一帧）加载完成后触发 | H264 |
| waiting | 由于暂时缺少数据，播放已停止时触发 | H264 |
| error | 播放报错触发 | H264 |
| ended | 播放结束 （回放） | H264 |
| screenfullChange | 全局全屏时触发 | H264/H265 |
| resize | 调用 resize时触发 | H264/H265 |
| destroy | 销毁 | H264/H265 |