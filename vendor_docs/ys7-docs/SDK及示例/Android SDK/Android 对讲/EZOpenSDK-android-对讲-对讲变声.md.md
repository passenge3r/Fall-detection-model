# EZOpenSDK-android-对讲-对讲变声.md

> EZOpenSDK-android-对讲-对讲变声

> 更新时间: 2026-06-02T14:03:41.000+08:00

> 文档ID: 4169 | 来源树: SDK及示例

---

# 对讲变声

在门铃、门禁等业务场景中，室内用户说话时，为了保护隐私等原因，不希望室外用户接收真实的声音，萤石音视频SDK提供变声功能，可以讲某一方对讲的声音变为其他声音，比如小丑、大叔等音色，让另外一方听不出来是谁。

EZPlayer

```
/**
 * 对讲变声，对讲成功后开启，需要设备开通变声服务后才生效（只支持国内，海外不支持）
 */
public void startVoiceChange(EZConstants.EZVoiceChangeType voiceChangeType, EZTalkback.TalkBackVoiceChangeCallback callback);
```

  

如果该设备已开通变声服务，**对讲过程中**可以调用如上api实现对讲变声。EZVoiceChangeType枚举值和对应的效果说明如下表

| 枚举 | 变声效果 |
| --- | --- |
| EZ\_VOICE\_CHANGE\_TYPE\_NORMAL | 原音 |
| EZ\_VOICE\_CHANGE\_TYPE\_MAN | 大叔音 |
| EZ\_VOICE\_CHANGE\_TYPE\_CLOWN | 小丑音 |