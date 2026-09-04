# EZOpenSDK-harmony-回放-进度拖拽.md

> EZOpenSDK-harmony-回放-进度拖拽

> 更新时间: 2026-06-02T14:03:58.000+08:00

> 文档ID: 4205 | 来源树: SDK及示例

---

# 进度拖拽

回放时，支持拖拽进度条，跳转到指定的时间点进行查看。api如下

EZPlayer

```
/**
 * 根据偏移时间播放，播放过程中才能调用
 * 拖动进度条时调用此接口，调用前需判断下录像是否在播放中。如果录像不在播放中，需要return，不要调用此接口。
 * @param offsetTime 录像偏移时间
 */
async seekPlayback(offsetTime: Date);
```

### 1. 第一步绘制SeekBar组件

开发者需在设备回放页面创建一个Slider组件，并设置onChange监听

### 2. 第二步计算拖拽后的时间并进行seek

Slider组件拖拽后，当前Slider的value值 \* 该录像片段总秒数 + 该录像片段开始时间，即为seek的时间点

**示例代码**：

```
Slider({ value: this.sliderValue })
  .trackColor(Color.Gray)
  .flexShrink(1)
  .onChange(async (value: number, mode: SliderChangeMode) => {
    // do something
    // 拖动结束后回调
    if (mode == SliderChangeMode.End) {
      this.sliderValue = value
      await this.onSliderChange(value)
    }
  })


  /** 播放进程条拖动 */
  async onSliderChange(value: number) {
    if (!this.isPlaying) {// 不在播放中，拦截
      return
    }
    if (value == 100) {
      await this.player?.stopPlayback()
      return
    }
    let secondsAfterStartTime = this.duringSeconds * (value / 100)

    let offsetTime: Date | null = null
    if (this.recordCategory == EZRecordCategory.EZRecordCategoryDevice) {
      if (this.deviceRecord) {
        offsetTime = new Date(this.deviceRecord.startTime.getTime() + secondsAfterStartTime * 1000)
      }
    } else {
      if (this.cloudRecord) {
        offsetTime = new Date(this.cloudRecord.startTime.getTime() + secondsAfterStartTime * 1000)
      }
    }
    if (!offsetTime) {
      return
    }
    clearInterval(this.sliderTimerIntervalID)
    await this.player?.seekPlayback(offsetTime)
    // do something
  }
```