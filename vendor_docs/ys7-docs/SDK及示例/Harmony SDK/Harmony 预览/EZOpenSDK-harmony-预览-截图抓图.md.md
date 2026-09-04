# EZOpenSDK-harmony-预览-截图抓图.md

> EZOpenSDK-harmony-预览-截图抓图

> 更新时间: 2026-06-02T14:03:55.000+08:00

> 文档ID: 4194 | 来源树: SDK及示例

---

# 截图 & 抓图

### 截图

**取流过程中**，对当前画面进行截图，返回值为截图本地缓存路径。

EZPlayer

```
/**
 * 直播画面抓图
 * 耗时操作
 * @param streamId 双目设备轨道
 * @returns 图片路径
 */
async capturePicture(streamId: number = 0): Promise<string>;
```

代码示例：

```
let picPath = await this.player?.capturePicture()
```

### 抓图

给在线设备下发信令，让设备上传当前图片到云端存储，**抓图将在服务器端保留2个小时**；返回值为图片的url地址。  
**不要求在取流过程中**

EZOpenSDK

```
/**
 * 获取抓取摄像头图片的url接口
 * 该接口比较耗时，不建议进行批量设备抓图，SDK内部只支持6个http请求并发，该接口会持续占用http请求资源，如果遇到http请求延时巨大问题，优先考虑抓图接口并发造成的问题,
 * 抓图将在服务器端保留2个小时
 * @param deviceSerial
 * @param cameraNo
 * @param callback
 * @param deviceSerial  设备序列号
 * @param cameraNo      通道号
 * @param callback      回调，正常时返回url地址信息，错误时返回错误码
 */
static captureCamera(deviceSerial: string, cameraNo: number, callback: (url: string, error: EZError) => void);
```

代码示例：

```
EZOpenSDK.captureCamera(this.mSingleDeviceSerial, 1, (url, error) => {
  this.captureCameraImagUrl = url
})
```