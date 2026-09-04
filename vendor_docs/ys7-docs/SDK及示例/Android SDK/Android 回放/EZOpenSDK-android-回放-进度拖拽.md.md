# EZOpenSDK-android-回放-进度拖拽.md

> EZOpenSDK-android-回放-进度拖拽

> 更新时间: 2026-06-02T14:03:40.000+08:00

> 文档ID: 4165 | 来源树: SDK及示例

---

# 进度拖拽

回放时，支持拖拽进度条，跳转到指定的时间点进行查看。api如下

EZPlayer

```
/**
 * 根据偏移时间播放，播放过程中才能调用
 * 拖动进度条时调用此接口，调用前需判断下录像是否在播放中。如果录像不在播放中，需要return，不要调用此接口。
 *
 * @param offsetTime 录像偏移时间
 * @return true 表示成功， false 表示失败
 */
public boolean seekPlayback(Calendar offsetTime);
```

### 1. 第一步绘制SeekBar组件

开发者需在设备回放页面创建一个SeekBar组件，并设置setOnSeekBarChangeListener监听

### 2. 第二步计算拖拽后的时间并进行seek

SeekBar组件拖拽后，当前SeekBar的value值 \* 该录像片段总秒数 + 该录像片段开始时间，即为seek的时间点

**示例代码**：

```
progressSeekbar.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
    /**
     * 拖动条停止拖动的时候调用
     */
    @Override
    public void onStopTrackingTouch(SeekBar arg0) {
        int progress = arg0.getProgress();
        if (progress == RemoteListContant.PROGRESS_MAX_VALUE) {
            // 拖动到seekBar末尾，结束回放
            // do something
            return;
        }
        if (currentClickItemFile != null) {
            long beginTime = currentClickItemFile.getBeginTime();
            long endTime = currentClickItemFile.getEndTime();
            long avg = (endTime - beginTime) / RemoteListContant.PROGRESS_MAX_VALUE;
            long trackTime = beginTime + (progress * avg);

            // do something

            LogUtil.i(TAG,
                    "onSeekBarStopTracking, begin time:" + beginTime + " endtime:" + endTime + " avg:" + avg + " MAX" +
              ":" + RemoteListContant.PROGRESS_MAX_VALUE + " tracktime:" + trackTime);
            if (mPlaybackPlayer != null) {
                Calendar seekTime = Calendar.getInstance();
                seekTime.setTime(new Date(trackTime));
                mPlaybackPlayer.seekPlayback(seekTime);
            }
        }
    }

    /**
     * 拖动条开始拖动的时候调用
     */
    @Override
    public void onStartTrackingTouch(SeekBar arg0) {
    }

    /**
     * 拖动条进度改变的时候调用
     */
    @Override
    public void onProgressChanged(SeekBar arg0, int arg1, boolean arg2) {
        // do something
    }
});
```