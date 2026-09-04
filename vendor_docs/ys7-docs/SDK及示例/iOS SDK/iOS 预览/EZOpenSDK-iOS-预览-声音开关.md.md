# EZOpenSDK-iOS-预览-声音开关.md

> EZOpenSDK-iOS-预览-声音开关

> 更新时间: 2026-06-02T14:03:47.000+08:00

> 文档ID: 4081 | 来源树: SDK及示例

---

# 声音开关

画面预览时，可以开启或者关闭声音。

### 声音关闭

EZPlayer.h

```
/**
 *  关闭声音
 *
 *  @return YES/NO
 */
- (BOOL)closeSound;
```

示例代码：

```
[_player closeSound];
```

### 声音开启

EZPlayer.h

```
/**
 *  开启声音
 *
 *  @return YES/NO
 */
- (BOOL)openSound;
```

示例代码：

```
[_player openSound];
```

**注意**：取流成功后，画面声音默认是开启的；如需静音播放，请在接收到播放成功消息后关闭声音。

示例代码：

```
/** 播放器播放成功消息回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    NSLog(@"player: %@, didReceivedMessage: %d", player, (int)messageCode);
    if (messageCode == PLAYER_REALPLAY_START) {
        ...
        if (!_isOpenSound) {
            [_player closeSound];
        }
        ...
    }
```