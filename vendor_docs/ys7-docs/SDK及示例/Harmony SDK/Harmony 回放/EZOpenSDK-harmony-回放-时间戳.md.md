# EZOpenSDK-harmony-回放-时间戳.md

> EZOpenSDK-harmony-回放-时间戳

> 更新时间: 2026-06-02T14:03:58.000+08:00

> 文档ID: 4206 | 来源树: SDK及示例

---

# 回放时间戳

录像片段回放时，提供当前播放帧时间戳。api如下

EZPlayer

```
/**
 * 获取当前播放时间进度
 * @returns 播放进度的NSDate数据
 */
async getOSDTime(): Promise<Date | null>;
```

获取到当前播放时间戳 - 录像片段的开始时间 = 当前已经播放的秒数，再刷新已回放秒数Text组件 和 回放进度Slider组件

**示例代码**：

```
let currentTime = await this.player?.getOSDTime()
if (!currentTime) {
  return
}
if (this.recordCategory == EZRecordCategory.EZRecordCategoryDevice && this.deviceRecord) {
  this.playSeconds = EZTimeUtil.compareDates(currentTime, this.deviceRecord.startTime)
} else if (this.recordCategory == EZRecordCategory.EZRecordCategoryCloud && this.cloudRecord) {
  this.playSeconds = EZTimeUtil.compareDates(currentTime, this.cloudRecord.startTime)
}

// 播放时长 < 0 ||  > 录像总时长，置0处理
if (this.playSeconds < 0 || this.playSeconds > this.duringSeconds) {
  this.playSeconds = 0
}
this.playTime = TimeUtil.formatSeconds(this.playSeconds)
this.sliderValue = (this.playSeconds / this.duringSeconds) * 100
```

**注意**：暂不支持国标设备回放返回时间戳。