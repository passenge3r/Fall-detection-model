# EZOpenSDK-harmony-预览-门锁设备开门token.md

> EZOpenSDK-harmony-预览-门锁设备开门token

> 更新时间: 2026-06-02T14:03:56.000+08:00

> 文档ID: 4198 | 来源树: SDK及示例

---

# 门锁设备开门token

视频类门锁设备预览时，SDK会将码流私有数据中的门锁开门token回调给开发者；开发者可以使用该token+[平台接口](https://open.ys7.com/help/760)实现门锁设备远程开门。

### 开门token获取

播放器EZPlayer设置setPlayerAdditionalInfoCallback回调后，会回调开门token；

代码示例：

```
private playerAdditionalInfoCallback: EZPlayerAdditionalInfoCallback = {
  /*
    * 取流数据中获取开门token回调
    */
  playPrivateTokenInfo: (tokenInfo: EZPMPlayPrivateTokenInfo) => {
    EZLog.info(this.TAG, `token--->${tokenInfo.token}`)
  }
}
```

**注意：如果门锁设备没有回调开门token的话，请确认该设备的远程开锁开关是否打开。**

萤石云视频App入口：设备设置-开锁设置-远程开锁-开启远程开锁

如需集成远程开锁开关功能，请使用[此接口](https://open.ys7.com/help/759)