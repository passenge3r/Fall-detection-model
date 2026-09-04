# EZOpenSDK-android-预览-截图抓图.md

> EZOpenSDK-android-预览-截图抓图

> 更新时间: 2026-06-02T14:03:37.000+08:00

> 文档ID: 4154 | 来源树: SDK及示例

---

# 截图 & 抓图

## 截图

**取流过程中**，对当前画面进行截图，返回值为Bitmap对象。

应用场景：

- 预览页面直播时，停止播放前截图作为封面覆盖在播放窗口上
- 取流时，截图保存到相册

EZPlayer

```
/**
 * 开启截屏，需要先开启预览或回放
 * 耗时操作，需要在子线程中执行
 *
 * @return 图片数据
 */
public Bitmap capturePicture();
```

代码示例：

```
Thread thr = new Thread() {
    @Override
    public void run() {
        Bitmap bmp =  mEZPlayer.capturePicture();
    }
};
thr.start();
```

## 抓图

给在线设备下发信令，让设备上传当前图片到云端存储，**抓图将在服务器端保留2个小时**；返回值为图片的url地址。  
**不要求在取流过程中**

应用场景：

- 抓图作为设备封面

EZOpenSDK

```
/**
 * 获取摄像头实时图片的url接口，需要设备支持，萤石设备一般都能支持此协议。(该功能和萤石云视频app首页刷新封面的功能一致)
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @param cameraNo     通道号
 * @return 图片url
 * @throws BaseException replaced by getRealPicture and capturePicture
 */
 public String captureCamera(String deviceSerial, int cameraNo) throws BaseException;
```

代码示例：

```
new Thread(() -> {
    try {
        String string = getOpenSDK().captureCamera(mSingleDeviceSerial, 1);
    } catch (BaseException e) {
        e.printStackTrace();
    }
}).start();
```