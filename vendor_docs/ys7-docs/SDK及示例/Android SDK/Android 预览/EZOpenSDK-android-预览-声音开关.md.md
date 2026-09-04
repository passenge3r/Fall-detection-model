# EZOpenSDK-android-预览-声音开关.md

> EZOpenSDK-android-预览-声音开关

> 更新时间: 2026-06-02T14:03:37.000+08:00

> 文档ID: 4155 | 来源树: SDK及示例

---

# 声音开关

画面预览时，可以开启或者关闭声音。

### 声音关闭

EZPlayer

```
/**
 * 关闭声音
 *
 * @return true 表示成功， false 表示失败
 */
public boolean closeSound();
```

示例代码：

```
mEZPlayer.closeSound();
```

### 声音开启

EZPlayer

```
/**
 * 开启声音
 *
 * @return true 表示成功， false 表示失败
 */
public boolean openSound();
```

示例代码：

```
mEZPlayer.openSound();
```

**注意**：取流成功后，画面声音默认是开启的；如需静音播放，请在接收到播放成功消息后关闭声音。

示例代码：

```
@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_REALPLAY_PLAY_SUCCESS:// 播放成功消息
            // do something
            if (mLocalInfo.isSoundOpen()) {
                mEZPlayer.openSound();
            } else {
                mEZPlayer.closeSound();
            }
            break;
    }
}
```