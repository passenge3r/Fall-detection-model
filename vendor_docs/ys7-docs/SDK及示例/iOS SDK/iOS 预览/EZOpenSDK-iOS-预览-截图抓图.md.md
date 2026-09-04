# EZOpenSDK-iOS-预览-截图抓图.md

> EZOpenSDK-iOS-预览-截图抓图

> 更新时间: 2026-06-02T14:03:47.000+08:00

> 文档ID: 4080 | 来源树: SDK及示例

---

# 截图 & 抓图

### 截图

**取流过程中**，对当前画面进行截图，返回值为UIImage对象。

EZPlayer.h

```
/**
 *  直播画面抓图
 *  耗时操作，需要在子线程中执行
 *
 *  @param quality 抓图质量（0～100）,数值越大图片质量越好，图片大小越大
 *
 *  @return image
 */
- (UIImage *)capturePicture:(NSInteger)quality;
```

代码示例：

```
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    UIImage *image = [_player capturePicture:100];
});
```

### 抓图

给在线设备下发信令，让设备上传当前图片到云端存储，**抓图将在服务器端保留2个小时**；返回值为图片的url地址。  
**不要求在取流过程中**

EZOpenSDK.h

```
/**
 *  获取抓取摄像头图片的url接口
 *
 *  @param deviceSerial 设备序列号
 *  @param cameraNo     通道号
 *  @param completion   回调block，正常时返回url地址信息，错误时返回错误码
 *  @see 该接口比较耗时，不建议进行批量设备抓图，SDK内部只支持6个http请求并发，该接口会持续占用http请求资源，如果遇到http请求延时巨大问题，优先考虑抓图接口并发造成的问题,
 *  抓图将在服务器端保留2个小时
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)captureCamera:(NSString *)deviceSerial
                               cameraNo:(NSInteger)cameraNo
                             completion:(void (^)(NSString *url, NSError * __nullable error))completion;
```

代码示例：

```
[EZOpenSDK captureCamera:_cameraInfo.deviceSerial cameraNo:_cameraInfo.cameraNo completion:^(NSString *url, NSError *error) {
    NSLog(@"[%@] capture cameraNo is [%d] url is %@, error is %@", _cameraInfo.deviceSerial, (int)_cameraInfo.cameraNo, url, error);
}];
```