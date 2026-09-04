# EZOpenSDK-harmony-SDK初始化.md

> EZOpenSDK-harmony-SDK初始化

> 更新时间: 2026-06-02T14:03:54.000+08:00

> 文档ID: 4191 | 来源树: SDK及示例

---

# SDK初始化及授权

SDK 初始化及认证流程如下  
![SDK初始化图片](http://img.ys7.com/group2/M00/49/A8/CmGCBVgAiauAMDzuAABAj-Uda3A972.jpg)

## 一、SDK初始化

如果是国内基线平台，不需要设置 **服务器域名(apiUrl)** 和 **认证地址(authUrl)**，SDK内部有初始值。示例代码如下：

```
await EZOpenSDK.initLibWithAppKey('Your AppKey')
```

如果是私有云平台，需要设置 **私有云服务器域名(apiUrl)**，示例代码如下：

```
await EZOpenSDK.initLibWithAppKey('Your AppKey', 'Your apiUrl', '')
```

## 二、SDK授权

SDK授权模式分为两种：**AccessToken授权模式** 和 **小权限TKToken授权模式**，两种模式只能二选一。

一般开发者使用AccessToken授权模式模式即可；小权限TKToken授权模式开发难度高，同时需要有后端服务参与开发，如您对应用安全性有更高的要求，可咨询技术支持。

### 1. AccessToken授权模式

授权登录流程代码如下

```
await EZOpenSDK.setAccessToken('Your accessToken')
```

设置的accessToken可能无效或者已过期，授权完成后，需要校验下accessToken的有效性，如果能获取到账号下设备数据，即说明accessToken有效。示例代码如下（具体参考MainPage.ets类实现）

```
EZOpenSDK.getDeviceList(0, 1, (deviceList, totalCount, error) => {
      if (error) {
        let errMsg: Resource
        switch (error.code) {
          case 400031:
            errMsg = $r('app.string.tip_of_bad_net')
            break
          default:
            errMsg = $r('app.string.login_expire')
            break
        }
        // accessToken无效
      } else {
        // accessToken有效
      }
    })
```

  

accessToken验证有效后，接下来您可以对账号下的设备进行预览、回放、对讲、控制等一系列操作了。

### 2. 小权限TKToken授权模式

此模式默认关闭，**如需使用，需要在initLibWithAppKey之前打开配置**

```
EZOpenSDK.enableSDKWithTKToken(true)
await EZOpenSDK.initLibWithAppKey('Your AppKey')
```

授权登录流程代码如下

```
await EZOpenSDK.setHttpToken('Your httpTKToken')
```

设置的httpToken同样需求验证有效性，同accessToken模式的验证方式。

**上述开关开启后，具体使用说明见api注释**

```
/**
 * SDK是否使用自己服务器生成的tkToken 代替 accessToken，默认NO；在`initLibWithAppKey`前调用
 * 此开关打开后，必须设置如下token，否则将影响各个功能的使用
 * `EZOpenSDK - setHttpToken:` 设置非设备类小权限token（入参不含设备序列号、通道号的接口会使用httpToken）
 * `EZOpenSDK - setDeviceTokenForDeviceSerial:deviceToken:` 设置设备类小权限token（入参含设备序列号、不包含通道号的接口会使用deviceToken）
 * `EZOpenSDK - setDeviceTokenForDeviceSerial:cameraNo:deviceGlobalToken:deviceVideoToken:` 设置设备类通道级小权限token（入参包含设备序列号、通道号的接口会使用deviceGlobalToken 和 deviceVideoToken）
 * `EZPlayer - setStreamToken:` 预览、对讲、回放设置取流小权限token
 * `EZDeviceRecordDownloadTask - setStreamToken:`下载设置取流小权限token
 *
 * 此开关打开后，以下接口不能使用
 * `EZOpenSDK - setAccessToken:`
 *
 * @param enable   是否使用自己服务器生成的tkToken
 */
static enableSDKWithTKToken(enable: boolean);
```

  

**小权限tkToken类型如下**

| token类型 | 释义 | 使用场景 |
| --- | --- | --- |
| httpToken | 非设备类小权限token | 入参不含设备序列号、通道号的api会使用此类型token，如getDeviceList获取账号下设备列表api |
| deviceToken | 设备类设备级小权限token | 入参含设备序列号、不包含通道号的api会使用deviceToken，如addDevice设备添加到账号api |
| deviceGlobalToken | 设备类通道级global小权限token | SDK内部封装的接口需要使用此类型小权限token，取流流程必须 |
| deviceVideoToken | 设备类通道级video小权限token | 入参包含设备序列号、通道号的api会使用此类型token，如setVideoLevel设置清晰度api |
| previewStreamToken | 预览小权限token | 用于预览取流，请在EZPlayer.startRealPlay之前设置 |
| playbackStreamToken | 回放小权限token | 用于SD卡回放取流，请在EZPlayer.startPlaybackFromDevice之前设置 用于SD卡录像下载，请在EZRecordDownloadTask.startRecordDownload之前设置 |
| talkStreamToken | 对讲小权限token | 用于对讲取流，请在EZPlayer.startVoiceTalk之前设置 |

**注意：**

- IPC设备对讲使用的是0通道，对讲streamToken生成请使用0通道。
- 双目设备(C7/C60P/Y5000FVX门锁等设备)取流使用的是交织流0通道，取流streamToken生成请使用0通道，deviceGlobalToken和deviceVideoToken保持不变使用1通道。

## 三、SDK账号切换

- 第一步：调用EZOpenSDK.logout((error) => {})退出前一个账号；
- 第二步：重新进行SDK初始化：await EZOpenSDK.setAccessToken('Your new accessToken');
- 第三步：重新进行授权：await EZOpenSDK.setAccessToken('Your new accessToken');

以上流程按顺序完成后，才可以对新账号下的设备进行预览、回放、对讲、控制等一系列操作了，否则会有异常现象。

## 四、SDK调试模式

**应用发布时，请务必关闭SDK调试模式，否则沙盒中会产生大量的码流文件，占用手机存储空间**。

开发时可选择是否打开SDK调试开关，打开后便于开发者排查问题。

EZOpenSDK.ets

```
/**
  * 设置是否打印debug日志,需在初始化sdk之前调用
  * @param enable 是否打印日志，默认关闭
  * return true/false
  */
static setDebugLogEnable(enable: boolean): boolean;

/**
  *  设置是否缓存sdk中的码流文件，用于码流调试；打开后，每次取流都会将码流保存到沙盒中
  *  在debug模式下设置开启，release下必须关闭或者删除，否则沙盒中会产生大量的码流文件，占用手机存储空间
  *  视频码流路径：/data/app/el2/100/base/应用包名/haps/entry/cache/EZSavedStreamData
  *  对讲码流路径：/data/app/el2/100/base/应用包名/haps/entry/cache/EZSavedIntercomData
  *  @param enable 是否打开，默认false
  *  @return true/false
  */
static setDebugStreamEnable(enable: boolean): boolean;
```