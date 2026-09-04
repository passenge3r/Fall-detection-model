# EZOpenSDK-android-回放-SD卡录像封面.md

> EZOpenSDK-android-回放-SD卡录像封面

> 更新时间: 2026-06-02T14:03:40.000+08:00

> 文档ID: 4167 | 来源树: SDK及示例

---

# SD卡录像封面

自动抽取画面中的某一帧作为录像的封面图，需要设备能力集支持。

### 1. 第一步SD卡录像封面管理器初始化

传入设备序列号、通道号，初始化SD卡录像封面管理器；设备代理并实现代理方法，示例代码如下：

```
import com.videogo.remoteplayback.RecordCoverFetcherManager;

public class EZPlayBackListActivity extends RootActivity implements ... {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // do something
        // 国内支持SD卡录像封面获取，海外不支持
        if (!EzvizAPI.getInstance().isUsingGlobalSDK()) {
            // 与设备建立链接，获取SD卡录像封面（页面退出的时候必须断开链接，释放资源，见onDestroy方法）
            RecordCoverFetcherManager.getInstance().initFetcher(this, mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(),
                    new RecordCoverFetcherManager.RecordCoverFetcherInitCallBack() {
                        @Override
                        public void onFetcherInitSuccess() {

                        }

                        @Override
                        public void onFetcherInitFailed() {

                        }
            });
        }

    }
}
```

### 2. 第二步请求录像封面

获取到SD卡录像列表后请求录像封面，示例代码如下：

```
if (!EzvizAPI.getInstance().isUsingGlobalSDK() && EZBusinessTool.isSupportSdCover(mDeviceInfo, mCameraInfo)) {// 国内 & 支持SD卡录像封面
    // 去获取SD卡视频封面
    List<EZDeviceRecordFile> recordFiles = new ArrayList<>();
    for (int i = 0; i < cloudPartInfoFile.size(); i ++) {
        CloudPartInfoFile file = cloudPartInfoFile.get(i);
        EZDeviceRecordFile recordFile = new EZDeviceRecordFile();
        recordFile.setBegin(file.getBegin());
        recordFile.setEnd(file.getEnd());
        recordFile.setSeq(i);// 设置索引，封面回调的时候知道对应哪一个录像
        recordFiles.add(recordFile);
    }
    RecordCoverFetcherManager.getInstance().requestRecordCover(recordFiles, new RecordCoverFetcherManager.RecordCoverFetcherCallBack() {
        @Override
        public void onGetCoverSuccess(int seq, byte[] bytes) {
            /**
             * 注意：图片是设备一张一张传回来的，接收到一张就需要局部刷新UI。
             */

            // 以下情况做拦截，否则会将SD卡录像封面显示在云存储录像上或者数组越界崩溃
            if (mCheckBtnCloud.isChecked() || seq > cloudPartInfoFile.size()-1) {
                return;
            }

            // 此处将bytes转为bitmap。开发者也可自行将bytes转为文件，进行缓存管理。
            Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
            // TODO 局部刷新UI

            // 将获取到的图片赋值给列表中的对象
            CloudPartInfoFile cloudFile = cloudPartInfoFile.get(seq);
            cloudFile.setBitmap(bitmap);
            // do something
        }

        @Override
        public void onGetCoverFailed(int errorCode) {
            LogUtil.e(TAG, "onGetCoverFailed");
        }
    });
```

### 3. 页面退出时录像封面管理器释放资源

```
@Override
protected void onDestroy() {
    super.onDestroy();
    // do something
    if (!EzvizAPI.getInstance().isUsingGlobalSDK()) {
        RecordCoverFetcherManager.getInstance().stopFetcher();// 断开与设备的链接
    }
}
```