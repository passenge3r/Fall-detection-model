# EZOpenSDK-iOS-回放-暂停恢复.md

> EZOpenSDK-iOS-回放-暂停恢复

> 更新时间: 2026-06-02T14:03:49.000+08:00

> 文档ID: 4089 | 来源树: SDK及示例

---

# 回放暂停/恢复

### 回放暂停

回放时，支持暂停播放。api如下  
EZPlayer.h

```
/**
 *  暂停远程回放播放
 */
- (BOOL)pausePlayback;
```

### 回放恢复

回放暂停后，支持恢复播放。api如下  
EZPlayer.h

```
/**
 *  继续远程回放播放
 */
- (BOOL)resumePlayback;
```