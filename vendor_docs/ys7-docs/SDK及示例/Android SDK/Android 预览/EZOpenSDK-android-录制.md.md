# EZOpenSDK-android-录制.md

> EZOpenSDK-android-录制

> 更新时间: 2026-07-09T15:28:09.000+08:00

> 文档ID: 4160 | 来源树: SDK及示例

---

# 录制

提供录像能力，集成后可以对当前`预览或回放`画面进行录像，一般是某一段时长录像，并提供保存。

## 开始录制

EZPlayer.java

```
/**
  * 预览/回放时开始本地录像录制功能
  * 注意：录制的MP4视频时长 和 应用层录制时长 对比是没有意义的。因为应用层计时器一直在走，但是网络异常导致画面卡住 或 设备码流异常（比如帧丢失、跳帧等情况）都会影响录制的时长
  * 验证标准如下：
  * 1、录制的MP4视频播放开始画面中的时间戳 与 实际开始录制时画面中的时间戳是否相近。
  * 2、录制的MP4视频播放结束画面中的时间戳 与 实际结束录制时画面中的时间戳是否相近。
  *
  * @param recordFile 此路径必须指定为沙盒路径；不能指定为相册路径，部分机型、新系统上有限制
  *
  * @return true 表示成功， false 表示失败
  */
public boolean startLocalRecordWithFile(String recordFile);

/**
  * 预览/回放时开始本地录像录制功能（保存为ps文件，ps文件为码流源文件，未经过转码转封装，三方开发者不使用）
  *
  * @return true 表示成功， false 表示失败
  */
public boolean startLocalRecordWithFileEx(String recordFile);
```

**注意**：预览或回放取流过程中才能开始录制功能。

示例代码：

```
/**
 * 此路径必须指定为沙盒路径；不能指定为相册路径，部分机型、新系统上有限制
 * This path must be specified as a sandbox path; Cannot be specified as album path, some models and new systems have restrictions
 */
final String strRecordFile = DemoConfig.getRecordsFolder() + "/" + System.currentTimeMillis() + ".mp4";
LogUtil.i(TAG, "recorded video file path is " + strRecordFile);
// 设置录制回调
mEZPlayer.setStreamDownloadCallback(new EZOpenSDKListener.EZStreamDownloadCallback() {
    @Override
    public void onSuccess(String filepath) {
        LogUtil.i(TAG, "EZStreamDownloadCallback onSuccess " + filepath);
        dialog("Record result", "saved to " + mCurrentRecordPath);
        // TODO 将录制的视频保存到相册，需要申请动态权限WRITE_EXTERNAL_STORAGE，由开发者自行实现
        // EZUtils.saveVideo2Album(EZRealPlayActivity.this, new File(filepath));
    }

    @Override
    public void onError(EZOpenSDKListener.EZStreamDownloadError code) {
        LogUtil.e(TAG, "EZStreamDownloadCallback onError " + code.name());
    }
});
boolean result = mEZPlayer.startLocalRecordWithFile(strRecordFile);
if (result) {
    // do something 开启录制定时器，刷新UI
} else {
    // do something
}
```

## 结束录制

EZPlayer.java

```
/**
 * 结束预览/回放录像录制（保存为mp4文件，与startLocalRecordWithFile配对使用）
 * @return true 表示成功， false 表示失败
 */
public boolean stopLocalRecord();

/**
  * 结束预览/回放录像录制（保存为ps文件，与startLocalRecordWithFileEx配对使用，三方开发者不使用）
  *
  * @return true 表示成功， false 表示失败
  */
public boolean stopLocalRecordEx();
```

示例代码：

```
mEZPlayer.stopLocalRecord();
```

**注意**：如果用户没有主动调用停止录制，页面退出的时候，开发者需要在onStop函数中停止录制。