# EZOpenSDK-iOS-告警消息-事件回放.md

> EZOpenSDK-iOS-告警消息-事件回放

> 更新时间: 2026-06-02T14:03:52.000+08:00

> 文档ID: 4096 | 来源树: SDK及示例

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
- (void)viewDidLoad {
    self.beginTime = [self.info.alarmStartTime dateByAddingTimeInterval:-(self.info.preTime)];
    self.endTime = [self.info.alarmStartTime dateByAddingTimeInterval:self.info.delayTime];
    __weak typeof (self) weakSelf = self;
    [EZOpenSDK searchRecordFileFromDevice:self.info.deviceSerial
                                 cameraNo:self.info.cameraNo
                                beginTime:self.beginTime
                                  endTime:self.endTime
                               completion:^(NSArray *deviceRecords, NSError *error) {
                                   [weakSelf.records removeAllObjects];
                                   if ([deviceRecords count] == 0) {// SD卡本地没有查询到录像片段，去云端查询
                                       [weakSelf doCloudSearch];
                                   } else {// 播放查询到的第一个录像片段
                                       weakSelf.isSelectedDevice = YES;
                                       [weakSelf.records addObjectsFromArray:deviceRecords];
                                       [weakSelf doPlayFirst];
                                   }
                               }];
}

- (void)doCloudSearch {
    __weak typeof(self) weakSelf = self;
    [EZOpenSDK searchRecordFileFromCloud:self.info.deviceSerial
                                cameraNo:self.info.cameraNo
                               beginTime:self.beginTime
                                 endTime:self.endTime
                              completion:^(NSArray *cloudRecords, NSError *error) {
                                  [weakSelf.records removeAllObjects];
                                  weakSelf.isSelectedDevice = NO;
                                  if (!cloudRecords || cloudRecords.count == 0) {
                                      [weakSelf.loadingView stopSquareClockwiseAnimation];
                                      [EZToast show:NSLocalizedString(@"message_file_search_fail", @"文件查询失败")];
                                  }
                                  [weakSelf.records addObjectsFromArray:cloudRecords];
                                  [weakSelf doPlayFirst];
                              }];
}
```

### 2. 第二步：录像片段播放

获取到SD卡录像片段 或 云存储录像片段后，对第一段录像片段进行播放即可。流程同[录像回放](https://open.ys7.com/help/4086)。

如果未查询到，则提示**文件查询失败**。