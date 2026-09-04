# EZOpenSDK-android-告警消息-事件回放.md

> EZOpenSDK-android-告警消息-事件回放

> 更新时间: 2026-06-02T14:03:42.000+08:00

> 文档ID: 4171 | 来源树: SDK及示例

---

# 事件回放

对告警消息事件进行回放。

### 1. 第一步：获取录像片段

告警消息对象EZAlarmInfo中有如下几个属性

| 字段 | 释义 |
| --- | --- |
| alarmStartTime | 告警开始时间 |
| preTime | 告警录像开始时间提前偏移量，通过alarmStartTime减去提前偏移量获得告警录像的具体开始时间 |
| delayTime | 告警录像结束时间延后偏移量，通过alarmStartTime加上延后偏移量获得告警录像的具体结束时间 |
| ... | 其他属性 |

  

- 开始时间beginTime = alarmStartTime - preTime
- 结束时间endTime = alarmStartTime + delayTime

通过计算出来的beginTime 和 endTime 去SD卡本地或云端查询录像。当然，开发者也可根据自己业务需求使用自定义的preTime和delayTime值，比如都为5秒。

**示例代码如下**：

```
private Calendar mAlarmStartTime = null;
private Calendar mBeginTime = null;
private Calendar mEndTime = null;

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    new Thread() {
            @Override
            public void run() {
                try {
                    mEZAlarmInfo = intent.getParcelableExtra(IntentConsts.EXTRA_ALARM_INFO);
                    mAlarmStartTime = Utils.parseTimeToCalendar(mEZAlarmInfo.getAlarmStartTime());

                    mBeginTime = (Calendar) mAlarmStartTime.clone();
                    mBeginTime.add(Calendar.SECOND, -mEZAlarmInfo.preTime);
                    mEndTime = (Calendar) mAlarmStartTime.clone();
                    mEndTime.add(Calendar.SECOND, mEZAlarmInfo.delayTime);

                    LogUtil.i(TAG, "searchEZAlarmFile seletedTime:" + mAlarmStartTime.getTime());
                    mEZDeviceFileList = EzvizApplication.getOpenSDK().searchRecordFileFromDevice(mEZAlarmInfo.getDeviceSerial(),mEZAlarmInfo.getCameraNo(), mBeginTime, mEndTime);
                    if (mEZDeviceFileList != null && mEZDeviceFileList.size() > 0) {// SD卡本地查询到录像片段
                      doPlayFirst();// 播放查询到的第一个录像片段
                    } else {// SD卡本地没有查询到录像片段，去云端查询
                      LogUtil.d(TAG, "no matching device record file for alarm");
                      mEZCloudFileList = EzvizApplication.getOpenSDK().searchRecordFileFromCloud(mEZAlarmInfo.getDeviceSerial(),mEZAlarmInfo.getCameraNo(), mBeginTime, mEndTime);
                      if (mEZCloudFileList != null && mEZCloudFileList.size() > 0) {
                          doPlayFirst();// 播放查询到的第一个录像片段
                      } else {
                        LogUtil.d(TAG, "no matching cloud record file for alarm");
                      }
                    }   
                } catch (BaseException e) {
                    e.printStackTrace();

                    ErrorInfo errorInfo = (ErrorInfo) e.getObject();
                    LogUtil.d(TAG, "search file list failed. error " + errorInfo.toString());
                }
            }
        }.start();
    
}
```

### 2. 第二步：录像片段播放

获取到SD卡录像片段 或 云存储录像片段后，对第一段录像片段进行播放即可。流程同[录像回放](https://open.ys7.com/help/4161)。

如果未查询到，则提示**文件查询失败**。