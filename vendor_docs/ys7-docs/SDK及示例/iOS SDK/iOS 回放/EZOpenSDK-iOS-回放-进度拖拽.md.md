# EZOpenSDK-iOS-回放-进度拖拽.md

> EZOpenSDK-iOS-回放-进度拖拽

> 更新时间: 2026-06-02T14:03:49.000+08:00

> 文档ID: 4090 | 来源树: SDK及示例

---

# 进度拖拽

回放时，支持拖拽进度条，跳转到指定的时间点进行查看。api如下

EZPlayer.h

```
/**
 *  根据偏移时间播放，播放过程中才能调用
 *  拖动进度条时调用此接口，调用前需判断下录像是否在播放中。如果录像不在播放中，需要return，不要调用此接口。
 *
 *  @param offsetTime 录像偏移时间
 */
- (void)seekPlayback:(NSDate *)offsetTime;
```

### 1. 第一步绘制UISlider组件

开发者需在设备回放页面创建一个UISlider组件，并添加拖动事件：UIControlEventValueChanged

### 2. 第二步计算拖拽后的时间并进行seek

UISlider组件拖拽后，当前UISlider的value值 \* 该录像片段总秒数 + 该录像片段开始时间，即为seek的时间点

**示例代码**：

```
- (void)duringValueChange:(id)sender {
    if (!_isPlaying) {// 不在播放中，拦截
        return;
    }
    if (self.duringSlider.value == 1) {
        [self.player stopPlayback];
        return;
    }
    NSDate *offsetTime = nil;
    if (_recordCategory == EZRecordCategoryDevice) {
        offsetTime = [_deviceRecord.startTime dateByAddingTimeInterval:_duringSeconds * self.duringSlider.value];
    } else {
        offsetTime = [_cloudRecord.startTime dateByAddingTimeInterval:_duringSeconds * self.duringSlider.value];
    }
    [_player seekPlayback:offsetTime];
}
```