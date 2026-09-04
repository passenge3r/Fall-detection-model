# EZOpenSDK-harmony-预览-声音开关.md

> EZOpenSDK-harmony-预览-声音开关

> 更新时间: 2026-06-02T14:03:56.000+08:00

> 文档ID: 4195 | 来源树: SDK及示例

---

# 声音开关

画面预览时，可以开启或者关闭声音。

### 声音关闭

EZPlayer

```
/**
 * 关闭声音
 * @returns true/false
 */
async closeSound(): Promise<boolean>;
```

示例代码：

```
await this.player?.closeSound()
```

### 声音开启

EZPlayer

```
/**
 * 开启声音
 * @returns true/false
 */
async openSound(): Promise<boolean>;
```

示例代码：

```
await this.player?.openSound()
```

**注意**：取流成功后，画面声音默认是开启的；如需静音播放，请在接收到播放成功消息后关闭声音。

示例代码：

```
// ------------------------ 播放器回调函数 player callback ------------------------

private playerCallback: EZPlayerCallback = {
  /*
    * 播放器播放成功消息回调
    */
  didReceivedMessage: async (messageCode: number) => {
    EZLog.debug(this.TAG, `player didReceivedMessage messageCode: ${messageCode}`)
    if (messageCode == EZMessageCode.PLAYER_REALPLAY_START) {
      // do something
      // 声音设置
      if (!this.isOpenSound) {
        await this.player?.closeSound()
      }
    }
  },
  /*
    * 播放器播放失败消息回调
    */
  didPlayFailed: async (error: EZError) => {
    
  }
}
```