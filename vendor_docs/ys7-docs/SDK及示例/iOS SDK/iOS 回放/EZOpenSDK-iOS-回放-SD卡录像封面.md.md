# EZOpenSDK-iOS-回放-SD卡录像封面.md

> EZOpenSDK-iOS-回放-SD卡录像封面

> 更新时间: 2026-06-02T14:03:50.000+08:00

> 文档ID: 4092 | 来源树: SDK及示例

---

# SD卡录像封面

自动抽取画面中的某一帧作为录像的封面图，需要设备能力集支持。

### 1. 第一步SD卡录像封面管理器初始化

传入设备序列号、通道号，初始化SD卡录像封面管理器；设备代理并实现代理方法，示例代码如下：

```
#import "EZRecordCoverFetcherManager.h"

@interface EZPlaybackViewController ()<..., RecordCoverFetcherDelegate> {
}

- (void)viewDidLoad {
    [super viewDidLoad];
    ...
    // SD卡本地录像获取初始化
    // 国内支持SD卡录像封面获取，海外不支持
    // 与设备建立链接，获取SD卡录像封面（页面退出的时候必须断开链接，释放资源，见-dealloc方法）
    [[EZRecordCoverFetcherManager sharedInstance] initFetcherWithDeviceSerial:_cameraInfo.deviceSerial cameraNo:_cameraInfo.cameraNo];
    [EZRecordCoverFetcherManager sharedInstance].fetcherDelegate = self;
    ...
}

#pragma mark - RecordCoverFetcherDelegate SD卡录像封面获取回调

/** SD卡录像封面提取封面成功回调 */
- (void)onGetCoverSuccess:(int)seq data:(NSData *_Nonnull)data {
    // 代码实现见第二步中示例代码
}

/** SD卡录像封面提取封面失败回调 */
- (void)onGetCoverFailed:(int)errorCode {
    
}
```

### 2. 第二步请求录像封面

获取到SD卡录像列表后请求录像封面，示例代码如下：

```
- (void)requestDeviceRecordCover {
    for (int i = 0; i < self.records.count; i ++) {
        EZDeviceRecordFile *recordFile = self.records[i];
        recordFile.seq = i;// 设置索引，封面回调的时候知道对应哪一个录像
    }
    // 去获取SD卡视频封面
    BOOL isSupportSdCover = [EZBusinessTool isSupportSdCover:self.deviceInfo cameraInfo:self.cameraInfo];
    if (isSupportSdCover) {
        [[EZRecordCoverFetcherManager sharedInstance] requestRecordCover:self.records];
    }
}
```

封面获取成功后会回调代理方法

```
#pragma mark - RecordCoverFetcherDelegate SD卡录像封面获取回调

/** SD卡录像封面提取封面成功回调 */
- (void)onGetCoverSuccess:(int)seq data:(NSData *_Nonnull)data {
    // 注意：图片是设备一张一张传回来的，接收到一张就需要局部刷新UI。
    // 本demo将data转换为UIImage直接加载。开发者也可自行将data转为文件，进行缓存管理。
    
    // 以下情况做拦截，否则会将SD卡录像封面显示在云存储录像上或者数组越界崩溃
    if (_recordCategory != EZRecordCategoryDevice || kArrayIsEmpty(self.records) || seq > self.records.count-1) {
        return;
    }
    EZDeviceRecordFile *recordFile = self.records[seq];
    if (![recordFile isKindOfClass:[EZDeviceRecordFile class]]) {
        return;
    }
    recordFile.imageData = data;
    
    [self.playbackList reloadItemsAtIndexPaths:@[[NSIndexPath indexPathForRow:seq inSection:0]]];
}

/** SD卡录像封面提取封面失败回调 */
- (void)onGetCoverFailed:(int)errorCode {
    NSLog(@"onGetCoverFailed");
}
```

### 3. 页面退出时录像封面管理器释放资源

```
- (void)dealloc {
    ...
    [[EZRecordCoverFetcherManager sharedInstance] stopFetcher];// 断开与设备的链接
}
```