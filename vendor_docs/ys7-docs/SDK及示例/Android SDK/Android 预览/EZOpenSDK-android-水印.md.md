# EZOpenSDK-android-水印.md

> EZOpenSDK-android-水印

> 更新时间: 2026-06-02T14:03:39.000+08:00

> 文档ID: 4181 | 来源树: SDK及示例

---

# 水印

在预览、回放画面中嵌入自定义水印信息，并支持水印截图、水印录制。目前仅支持单目设备，不支持多目设备。

## 水印设置

在预览、回放画面中嵌入自定义水印信息。

  

**提示：** EZPlayWaterMarkConfig水印配置类中，大部分属性都配置了默认值，设置fontArray水印数组属性后即可显示水印效果。如需其他效果，设置对应的属性值进行调整。

EZPlayWaterMarkConfig.java

```
public class EZPlayWaterMarkConfig {
    // 文本信息数组
    public String[] fontArray = new String[]{};
    // 字体宽度，限制：大于0（小于15的会默认为15）
    public int fontWidth = 35;
    // 字体高度，限制：大于0（小于15的会默认为15）
    public int fontHeight = 35;
    // 字体行间距，限制：无 建议取值范围[1~2]，表示字体高的倍数，1就是紧贴
    public float fontSpace = 1.2f;
    // 字体对齐方式，默认左对齐
    public EZWaterMarkTextAlignment fontAlignment = EZWaterMarkTextAlignment.EZWaterMarkTextAlignmentLeft;

    // 字体顺时针倾斜角度，限制[0, 360]
    public float fontRotateAngle = 0f;

    // 字体颜色是否自适应，默认关闭。开启后，自定义设置的color属性会失效。深色背景字体会显示白色，浅色背景字体会显示成黑色。
    public boolean fontColorAdapt = false;

    // region 字体颜色相关，默认黑色

    // 红，限制：[0, 255]
    public int red = 0;
    // 绿，限制：[0, 255]
    public int green = 0;
    // 蓝，限制：[0, 255]
    public int blue = 0;
    // 透明度，限制：[0, 100]  设置0会默认为100
    public int alpha = 100;

    // endregion

    // region 字体位置

    // x轴比例开始位置，限制[0, 1]
    public float startPosX = 0f;
    // y轴比例开始位置，限制[0, 1]
    public float startPosY = 0f;

    // endregion

    // region 窗口自适应

    // 水印自适应
    public EZWaterMarkWindowAdaptMode windowAdaptMode = EZWaterMarkWindowAdaptMode.EZWaterMarkWindowAdaptModeNone;

    /*
      设置自适应行列数行间距 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontRowColumn时用到。
      计算方式：rowSpace = 300，当前窗口大小 = 900，行数 = 900/300 = 3。 当窗口大小增大到1200时，行数自适应调整 = 1200/300 = 4。
      （当不足一行或一列时，最小为2行2列）（小于30，效果为30）
     */
    public int windowAdaptRowSpace = 100;
    /*
      设置自适应行列数列间距 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontRowColumn时用到。
      （当不足一行或一列时，最小为2行2列）
     */
    public int windowAdaptColumnSpace = 100;
    /*
      设置字体比例的基准窗口宽 限制：大于0 windowAdaptMode == EZWaterMarkWindowAdaptModeFontSize时用到。
      计算方式：输入fontWidth = 20，baseWindowWidth = 0.5625，字体大小 = 当前窗口宽 * 20 / 900 。
      如当前窗口宽为1200时，字体大小 = 1200 * 20 / 900 = 26
     */
    public int windowAdaptBaseWindowWidth;
    public int windowAdaptBaseWindowHeight;

    // endregion

    // region 全屏水印设置

    /*
      水印是否全屏，当windowAdaptMode = EZWaterMarkWindowAdaptModeNone或EZWaterMarkWindowAdaptModeFontSize时生效，默认关闭。
      开启后，需要用到rowNumber、columnNumber属性
     */
    public boolean fillFullScreen = false;
    // 行数
    public int rowNumber = 2;
    // 列数
    public int columnNumber = 2;

    // endregion

    ......
}
```

EZPlayer.java

```
/**
  * 设置渲染水印信息，新设置的waterMarkConfig会覆盖之前设置的waterMarkConfig，仅支持单目设备，不支持多目设备
  * 预览、回放取流成功后才能调用
  *
  * @param waterMarkConfig 水印信息配置
  * @return true 表示成功， false 表示失败
  */
public boolean setWaterMarkFont(EZPlayWaterMarkConfig waterMarkConfig);

/**
  * 清除渲染水印信息，仅支持单目设备，不支持多目设备
  */
public void clearWaterMarkFont();
```

  

示例代码：

```
if (waterMarkConfig == null) {
    waterMarkConfig = new EZPlayWaterMarkConfig();
    waterMarkConfig.fontArray = new String[] {"水印信息：", "杭州萤石网络有限公司", "股票代码：688475"};
    waterMarkConfig.fontAlignment = EZPlayWaterMarkConfig.EZWaterMarkTextAlignment.EZWaterMarkTextAlignmentCenter;
    waterMarkConfig.fontRotateAngle = 45f;
    waterMarkConfig.fontColorAdapt = true;
    waterMarkConfig.windowAdaptMode= EZPlayWaterMarkConfig.EZWaterMarkWindowAdaptMode.EZWaterMarkWindowAdaptModeFontRowColumn;
}
// 取流成功后设置水印
mEZPlayer.setWaterMarkFont(waterMarkConfig);
```

水印效果：

![水印效果](https://resource.eziot.com/group2/M00/01/0A/CtwQFmj4o66AAabOAAJ8YmuJVdA207.jpg)

## 水印截图

设置水印后，可以进行水印画面截图

EZPlayer.java

```
/**
  * 开启水印截屏，需要先开启预览或回放；仅支持单目设备，不支持多目设备
  *
  * @param width 截图宽度
  * @param height 截图高度
  *
  * @return 图片数据
  */
public Bitmap captureRenderPicture(int width, int height);
```

示例代码：

```
// isWaterMarkShow：管理取流页面中的变量。设置水印后，设置为true；清除水印后，设置为false
// isMultiChannelDevice：管理取流页面中的变量。确认账号下没有多目设备可无视此变量。isMultiChannelDevice = EZBusinessTool.isSupportMultiChannel(mDeviceInfo, mCameraInfo);
// 水印开启 && 不是多目设备
if (isWaterMarkShow && !isMultiChannelDevice) {
    mEZPlayer.captureRenderPicture(mRealPlaySv.getWidth(), mRealPlaySv.getHeight());
}
```

## 水印录制

设置水印后，可以进行水印画面录制

EZPlayer.java

```
/**
  * 开始渲染画面录制，会重新编码，效率低，通过渲染进行录制，会携带电子放大、水印、滤镜等后处理信息，仅支持单目设备，不支持多目设备
  * 暂不支持多目设备
  *
  * @param recordFile 此路径必须指定为沙盒路径；不能指定为相册路径，新系统上有限制
  *
  * @return true 表示成功， false 表示失败
  */
public boolean startRenderRecordWithFile(String recordFile);

/**
  * 结束渲染画面录制，仅支持单目设备，不支持多目设备
  * @return true 表示成功， false 表示失败
  */
public boolean stopRenderRecord();
```

  

**注意：** 预览或回放取流过程中才能进行水印录制。

开始水印录制 示例代码：

```
// 开始本地水印录像
/**
 * 此路径必须指定为沙盒路径；不能指定为相册路径，新系统上有限制
 * This path must be specified as a sandbox path; Cannot be specified as album path, there are restrictions on the new system
 */
final String strRecordFile = DemoConfig.getRecordsFolder() + "/" + System.currentTimeMillis() + ".mp4";
LogUtil.i(TAG, "recorded video file path is " + strRecordFile);
// 设置录制回调
mEZPlayer.setStreamDownloadCallback(new EZOpenSDKListener.EZStreamDownloadCallback() {
    @Override
    public void onSuccess(String filepath) {
        LogUtil.i(TAG, "EZStreamDownloadCallback onSuccess " + filepath);
        dialog("Record result", "saved to " + mCurrentRecordPath);
        // TODO 将录制的视频保存到相册，需要申请动态权限WRITE_EXTERNAL_STORAGE，由开发者自行实现
        // EZUtils.saveVideo2Album(EZRealPlayActivity.this, new File(filepath));
    }

    @Override
    public void onError(EZOpenSDKListener.EZStreamDownloadError code) {
        LogUtil.e(TAG, "EZStreamDownloadCallback onError " + code.name());
    }
});
boolean result;
if (isWaterMarkShow && !isMultiChannelDevice) {// 水印录制
    result = mEZPlayer.startRenderRecordWithFile(strRecordFile);
} else {// 普通录制
    result = mEZPlayer.startLocalRecordWithFile(strRecordFile);
}
if (result) {
    // do something 开启录制定时器，刷新UI
} else {
    // do something
}
```

结束水印录制 示例代码：

```
mEZPlayer.stopRenderRecord();
```