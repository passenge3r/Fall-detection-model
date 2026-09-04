# EZOpenSDK-iOS-水印.md

> EZOpenSDK-iOS-水印

> 更新时间: 2026-06-02T14:03:48.000+08:00

> 文档ID: 4107 | 来源树: SDK及示例

---

# 水印

在预览、回放画面中嵌入自定义水印信息，并支持水印截图、水印录制。目前仅支持单目设备，不支持多目设备。

## 水印设置

在预览、回放画面中嵌入自定义水印信息。

**提示：** EZPlayWaterMarkConfig水印配置类中，大部分属性都配置了默认值，配置fontArray水印数组后即可显示水印效果。如需其他效果，设置对应的属性值进行调整。

EZPlayWaterMarkConfig.h

```
@interface EZPlayWaterMarkConfig : NSObject

/// 文本信息数组
@property (nonatomic, strong) NSArray<NSString *> *fontArray;
/// 字体宽度，限制：大于0（小于15的会默认为15），默认值为35
@property (nonatomic, assign) int fontWidth;
/// 字体高度，限制：大于0（小于15的会默认为15），默认值为35
@property (nonatomic, assign) int fontHeight;
/// 字体行间距，限制：无 建议取值范围[1~2]，表示字体高的倍数，1就是紧贴，默认值为1.2
@property (nonatomic, assign) float fontSpace;
/// 字体对齐方式，默认左对齐
@property (nonatomic, assign) EZWaterMarkTextAlignment fontAlignment;

/// 字体顺时针倾斜角度，限制[0, 360]，默认值为0
@property (nonatomic, assign) float fontRotateAngle;

/// 字体颜色是否自适应，默认关闭。开启后，自定义设置的color属性会失效。深色背景字体会显示白色，浅色背景字体会显示成黑色。
@property (nonatomic, assign) BOOL fontColorAdapt;

/// 红，限制：[0, 255]，默认值为0
@property (nonatomic, assign) int red;
/// 绿，限制：[0, 255]，默认值为0
@property (nonatomic, assign) int green;
/// 蓝，限制：[0, 255]，默认值为0
@property (nonatomic, assign) int blue;
/// 透明度，限制：[0, 100]  设置0会默认为100，默认值为0
@property (nonatomic, assign) int alpha;


/// x轴比例开始位置，限制[0, 1]，默认值为0
@property (nonatomic, assign) float startPosX;
/// y轴比例开始位置，限制[0, 1]，默认值为0
@property (nonatomic, assign) float startPosY;


/// 窗口自适应，默认值为EZWaterMarkWindowAdaptModeNone
@property (nonatomic, assign) EZWaterMarkWindowAdaptMode windowAdaptMode;

/**
  设置自适应行列数行间距 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontRowColumn时用到。，默认值为100
  计算方式：rowSpace = 300，当前窗口大小 = 900，行数 = 900/300 = 3。 当窗口大小增大到1200时，行数自适应调整 = 1200/300 = 4。
  （当不足一行或一列时，最小为2行2列）（小于30，效果为30）
 */
@property (nonatomic, assign) int windowAdaptRowSpace;
/**
  设置自适应行列数列间距 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontRowColumn时用到。，默认值为100
  （当不足一行或一列时，最小为2行2列）
 */
@property (nonatomic, assign) int windowAdaptColumnSpace;
/**
  设置字体比例的基准窗口宽 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontSize时用到。
  计算方式：输入fontWidth = 20，baseWindowWidth = 0.5625，字体大小 = 当前窗口宽 * 20 / 900 。
  如当前窗口宽为1200时，字体大小 = 1200 * 20 / 900 = 26
 */
@property (nonatomic, assign) int windowAdaptBaseWindowWidth;
@property (nonatomic, assign) int windowAdaptBaseWindowHeight;

/**
  水印是否全屏，当windowAdaptMode = EZWaterMarkWindowAdaptModeNone或EZWaterMarkWindowAdaptModeFontSize时生效，默认关闭。
  开启后，需要用到rowNumber、columnNumber属性
 */
@property (nonatomic, assign) BOOL fillFullScreen;
/// 行数，默认值为2
@property (nonatomic, assign) int rowNumber;
/// 列数，默认值为2
@property (nonatomic, assign) int columnNumber;

@end
```

EZPlayer.h

```
/**
 * 设置渲染水印信息，新设置的waterMarkConfig会覆盖之前设置的waterMarkConfig，仅支持单目设备，不支持多目设备
 * 预览、回放取流成功后才能调用
 *
 * @param waterMarkConfig 水印信息配置
 * @return YES/NO
 */
- (BOOL)setWaterMarkFont:(EZPlayWaterMarkConfig *)waterMarkConfig;

/**
 * 清除水印文字，仅支持单目设备，不支持多目设备
 * 该方法用于移除当前播放器上设置的所有水印文字
 */
- (void)clearWaterMarkFont;
```

  

示例代码：

```
// 取流成功后设置水印
[self.player setWaterMarkFont:self.waterMarkConfig];

- (EZPlayWaterMarkConfig *)waterMarkConfig {
    if (!_waterMarkConfig) {
        _waterMarkConfig = [[EZPlayWaterMarkConfig alloc] init];
        _waterMarkConfig.fontArray = @[@"水印信息：", @"杭州萤石网络有限公司", @"股票代码：688475"];
        _waterMarkConfig.fontAlignment = EZWaterMarkTextAlignmentCenter;
        _waterMarkConfig.fontRotateAngle = 45.f;
        _waterMarkConfig.fontColorAdapt = YES;
        _waterMarkConfig.windowAdaptMode = EZWaterMarkWindowAdaptModeFontRowColumn;
    }
    return _waterMarkConfig;
}
```

水印效果：

![水印效果](https://resource.eziot.com/group2/M00/01/0A/CtwQF2j4o7OAPFI4AAFxZX0chnU524.jpg)

## 水印截图

设置水印后，可以进行水印画面截图

EZPlayer.h

```
/**
 * 水印截图，仅支持单目设备，不支持多目设备
 * 耗时操作，需要在子线程中执行
 *
 * @param width 截图宽度
 * @param height 截图高度
 *
 * @return 抓取的图片
 */
- (UIImage *)captureRenderPictureWithWidth:(int)width height:(int)height;
```

示例代码：

```
CGFloat scale = [UIScreen mainScreen].scale;
CGFloat waterMarkWidth = self.playerView.width * scale;
CGFloat waterMarkHeight = self.playerView.height * scale;
// isWaterMarkShow：管理取流页面中的变量。设置水印后，设置为YES；清除水印后，设置为NO
// isMultiChannelDevice：管理取流页面中的变量。确认账号下没有多目设备可无视此变量。self.isMultiChannelDevice = [EZBusinessTool isSupportMultiChannel:self.deviceInfo cameraInfo:self.cameraInfo];
BOOL isWaterMarkCapture = self.isWaterMarkShow && !self.isMultiChannelDevice;
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    if (isWaterMarkCapture) { 
        UIImage *image = [_player captureRenderPictureWithWidth:waterMarkWidth height:waterMarkHeight];
    }
});
```

## 水印录制

设置水印后，可以进行水印画面录制

EZPlayer.h

```
/**
 * 开始渲染录制文件，仅支持单目设备，不支持多目设备
 * 该方法用于开始渲染指定的录制文件
 *
 * @param path 文件存储路径
 * @return YES 表示成功，NO 表示失败
 */
- (BOOL)startRenderRecordWithPath:(NSString *)path;

/**
 * 停止渲染录制，仅支持单目设备，不支持多目设备
 * 该方法用于停止当前的录制文件渲染
 */
- (void)stopRenderRecord:(void (^)(BOOL ret))complete;
```

  

**注意：** 预览或回放取流过程中才能进行水印录制。

开始水印录制 示例代码：

```
// 开始本地水印录像
// 创建文件
NSDate *date = [NSDate date];
_filePath = [NSString stringWithFormat:@"%@/%@.mp4", PATH_LocalRecord, [date formattedDateWithFormat:@"yyyyMMddHHmmss"]];
[FCFileManager createFileAtPath:_filePath overwrite:YES];
// 创建录制定时器
if (!_recordTimer) {
    _recordTimer = [NSTimer scheduledTimerWithTimeInterval:1.0 target:self selector:@selector(timerStart:) userInfo:nil repeats:YES];
}
if (self.isWaterMarkShow && !self.isMultiChannelDevice) {// 水印录制 && 非多目设备
    [_player startRenderRecordWithPath:_filePath];
} else {// 普通录制
    [_player startLocalRecordWithPathExt:_filePath];
}
```

结束水印录制 示例代码：

```
[_player stopRenderRecord:^(BOOL ret) {
    NSLog(@"%d", ret);
    // 销毁录制定时器
    [_recordTimer invalidate];
    _recordTimer = nil;
    // 可将录制的mp4文件转存到系统相册
    [self saveRecordToPhotosAlbum:_filePath];
    _filePath = nil;
}];
```