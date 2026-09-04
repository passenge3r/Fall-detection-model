# EZOpenSDK-android-回放-时间戳.md

> EZOpenSDK-android-回放-时间戳

> 更新时间: 2026-06-02T14:03:40.000+08:00

> 文档ID: 4166 | 来源树: SDK及示例

---

# 回放时间戳

录像片段回放时，提供当前播放帧时间戳。api如下

EZPlayer

```
/**
 * 获取当前播放时间戳
 *
 * @return true 表示成功， false 表示失败
 */
public Calendar getOSDTime();
```

获取到当前播放时间戳 - 录像片段的开始时间 = 当前已经播放的秒数，再刷新已回放秒数TextView组件 和 回放进度SeekBar组件

**示例代码**：

```
Calendar osd = mPlaybackPlayer.getOSDTime();
if (osd != null) {
    long osd = osdTime.getTimeInMillis();
    long begin = currentClickItemFile.getBeginTime();
    long end = currentClickItemFile.getEndTime();
    double x = ((osd - begin) * RemoteListContant.PROGRESS_MAX_VALUE) / (double) (end - begin);
    int progress = (int) x;
    progressSeekbar.setProgress(progress);

    SimpleDateFormat format = Utils.getEZDateFormat("yyyy-MM-dd HH:mm:ss");
    LogUtil.i(TAG, "handlePlayProgress, begin time:" + format.format(new Date(begin)) +
            " endtime:" + format.format(new Date(end)) + " osdTime:" + format.format(new Date(osd)) +
            " progress:" + progress + " maxProgress:" + RemoteListContant.PROGRESS_MAX_VALUE);

    if (osd >= begin && osd <= end) {
        int beginTimeClock = (int) ((osd - begin) / 1000);
        String convToUIDuration = RemoteListUtil.convToUIDuration(beginTimeClock);
        beginTimeTV.setText(convToUIDuration);
    }
}
```

**注意**：v5.17起支持国标设备回放返回时间戳。如您的国标设备回放无法获取回放时间戳，请检查SDK版本号。