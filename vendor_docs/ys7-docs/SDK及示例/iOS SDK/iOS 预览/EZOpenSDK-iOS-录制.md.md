# EZOpenSDK-iOS-录制.md

> EZOpenSDK-iOS-录制

> 更新时间: 2026-07-09T15:28:14.000+08:00

> 文档ID: 4103 | 来源树: SDK及示例

---

# 录制

提供录像能力，集成后可以对当前`预览或回放`画面进行录像，一般是某一段时长录像，并提供保存。

## 开始录制

EZPlayer.h

```
/**
 * 预览/回放时开始本地录像录制功能
 * 注意：录制的MP4视频时长 和 应用层录制时长 对比是没有意义的。因为应用层计时器一直在走，但是网络异常导致画面卡住 或 设备码流异常（比如帧丢失、跳帧等情况）都会影响录制的时长
 * 验证标准如下：
 * 1、录制的MP4视频播放开始画面中的时间戳 与 实际开始录制时画面中的时间戳是否相近。
 * 2、录制的MP4视频播放结束画面中的时间戳 与 实际结束录制时画面中的时间戳是否相近。
 *
 * @param path 文件存储路径
 *
 * @return YES/NO
 */
- (BOOL)startLocalRecordWithPathExt:(NSString *)path;
```

**注意**：预览或回放取流过程中才能开始录制功能。

示例代码：

```
// 开始本地录像
// 创建文件
NSDate *date = [NSDate date];
_filePath = [NSString stringWithFormat:@"%@/%@.mp4", PATH_LocalRecord, [date formattedDateWithFormat:@"yyyyMMddHHmmss"]];
[FCFileManager createFileAtPath:_filePath overwrite:YES];
// 创建录制定时器
if (!_recordTimer) {
    _recordTimer = [NSTimer scheduledTimerWithTimeInterval:1.0 target:self selector:@selector(timerStart:) userInfo:nil repeats:YES];
}
// 开始录制
[_player startLocalRecordWithPathExt:_filePath];
```

## 结束录制

EZPlayer.h

```
/**
 * 结束预览/回放录像录制，并生成mp4录制文件
 *
 * @param complete 操作是否成功 YES/NO
 */
- (void)stopLocalRecordExt:(void (^)(BOOL ret))complete;
```

示例代码：

```
[_player stopLocalRecordExt:^(BOOL ret) {
    NSLog(@"%d", ret);
    // 销毁录制定时器
    [_recordTimer invalidate];
    _recordTimer = nil;
    // 可将录制的mp4文件转存到系统相册
    [self saveRecordToPhotosAlbum:_filePath];
    _filePath = nil;
}];
```

**注意**：如果用户没有主动调用停止录制，页面退出的时候，开发者需要在-viewWillDisappear函数中停止录制。