# EZOpenSDK-iOS-回放-时间戳.md

> EZOpenSDK-iOS-回放-时间戳

> 更新时间: 2026-06-02T14:03:50.000+08:00

> 文档ID: 4091 | 来源树: SDK及示例

---

# 回放时间戳

录像片段回放时，提供当前播放帧时间戳。api如下  
  
EZPlayer.h

```
/**
 *  获取当前播放时间进度
 *
 *  @return 播放进度的NSDate数据
 */
- (NSDate *)getOSDTime;
```

获取到当前播放时间戳 - 录像片段的开始时间 = 当前已经播放的秒数，再刷新已回放秒数UILabel组件 和 回放进度UISlider组件

**示例代码**：

```
NSDate *currentTime = [_player getOSDTime];
if (!currentTime) {
    return;
}
NSLog(@"getOSDTime === %@", currentTime);
if (_recordCategory == EZRecordCategoryDevice) {// SD卡录像
    _playSeconds = [currentTime timeIntervalSinceDate:_deviceRecord.startTime];
} else {// 云存储录像
    _playSeconds = [currentTime timeIntervalSinceDate:_cloudRecord.startTime];
}
NSLog(@"_playSeconds === %f", _playSeconds);
if (_playSeconds > 0) {// 刷新UI
    self.playTimeLabel.text = [EZCommonTool convToUIDuration:_playSeconds];
    self.duringSlider.value = _playSeconds/_duringSeconds;
}
```

**注意**：v5.17起支持国标设备回放返回时间戳。如您的国标设备回放无法获取回放时间戳，请检查SDK版本号。