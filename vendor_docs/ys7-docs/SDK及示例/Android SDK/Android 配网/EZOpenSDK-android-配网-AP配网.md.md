# EZOpenSDK-android-配网-AP配网.md

> EZOpenSDK-android-配网-AP配网

> 更新时间: 2026-06-02T14:03:42.000+08:00

> 文档ID: 4173 | 来源树: SDK及示例

---

# AP配网

AP（Access Point，无线接入点）配网是一种常见的摄像机或智能设备连接到Wi-Fi网络的方式。它通过创建一个临时的Wi-Fi热点（即AP模式），使设备能够更方便地获取Wi-Fi设置信息并连接到目标网络。

## AP配网流程图

![AP配网流程图](https://resource.eziot.com/group2/M00/01/07/CtwQF2iIZe6AbGC8AAEQrS5GLmU285.png)

## AP配网集成开发流程

### 1. 第一步权限配置

需申请【本地网络权限 & 定位权限】，请参考[【android-权限设置】](https://open.ys7.com/help/4150)中的配网所需权限。

### 2. 第二步查询设备信息

查询设备信息probeDeviceInfo接口所获得对象是EZProbeDeviceInfo，正常查询到设备信息对象说明查询成功。

EZOpenSDK

```
/**
 * 尝试查询设备信息（用于添加设备之前, 简单查询设备信息，如是否在线，是否添加等）
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 需要查询的设备序列号
 * @param deviceType   设备型号 (设备型号和设备序列号不能均为空,优先按照设备序列号查询)
 * @return 返回 EZProbeDeviceInfo 对象，包含设备简单信息，用于添加目的
 */
public EZProbeDeviceInfoResult probeDeviceInfo(String deviceSerial, String deviceType);
```

  

**示例代码**：

```
new Thread() {
    public void run() {

        mEZProbeDeviceInfo = getOpenSDK().probeDeviceInfo(serialNo, mDeviceType);
        if (mEZProbeDeviceInfo != null) {
            if (mEZProbeDeviceInfo.getBaseException() == null) {
                // TODO: 2018/6/25 添加设备
                sendMessage(MSG_QUERY_CAMERA_SUCCESS);
                // 记录该设备热点前缀
                Config.DeviceHotspotPrefix = EZBusinessTool.getWiFiConfigPrefix(mEZProbeDeviceInfo.getEZProbeDeviceInfo().getDeviceHotSpot());
            } else {
                switch (mEZProbeDeviceInfo.getBaseException().getErrorCode()) {

                    case 120023:
                        // TODO: 2018/6/25  设备不在线，未被用户添加 （这里需要网络配置）
                    case 120002:
                        // TODO: 2018/6/25  设备不存在，未被用户添加 （这里需要网络配置）
                    case 120029:
                        // TODO: 2018/6/25  设备不在线，已经被自己添加 (这里需要网络配置)
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                LogUtil.i(TAG, "probeDeviceInfo fail :" + mEZProbeDeviceInfo.getBaseException().getErrorCode());
                                sendMessage(MSG_QUERY_CAMERA_FAIL, mEZProbeDeviceInfo.getBaseException().getErrorCode());
                            }
                        });
                        break;

                    case 120020:
                        // TODO: 2018/6/25 设备在线，已经被自己添加 (给出提示)
                        sendMessage(MSG_QUERY_CAMERA_FAIL, mEZProbeDeviceInfo.getBaseException().getErrorCode());
                        break;

                    case 120022:
                        // TODO: 2018/6/25  设备在线，已经被别的用户添加 (给出提示)
                    case 120024:
                        // TODO: 2018/6/25  设备不在线，已经被别的用户添加 (给出提示)
                        sendMessage(MSG_QUERY_CAMERA_FAIL, mEZProbeDeviceInfo.getBaseException().getErrorCode());
                        break;

                    default:
                        // TODO: 2018/6/25 请求异常
                        showToast("Request failed = " + mEZProbeDeviceInfo.getBaseException().getErrorCode());
                        break;
                }
            }
        } else {
            // 查询失败，do something
        }
    }
}.start();
```

**注意事项：**

萤石基线设备生成的热点前缀都是EZVIZ，定制设备生成的热点前缀可能是SoftAP或者其他，需要通过deviceInfo.deviceHotSpot属性来设置热点前缀。

代码示例：

EZBusinessTool.java

```
/**
  * 获取设备热点前缀
  * @param deviceHotSpot 0-EZVIZ，1-SoftAP，2-CAMGO
  */
public static String getWiFiConfigPrefix(int deviceHotSpot) {
    String WiFiConfigPrefix = "EZVIZ";
    switch (deviceHotSpot) {
        case 1:
            WiFiConfigPrefix = "SoftAP";
            break;
        case 2:
            WiFiConfigPrefix = "CAMGO";
            break;
        default:
            break;
    }
    return WiFiConfigPrefix;
}
```

### 3. 第三步配置设备网络

待设备提示配网时，调用startAPConfigWifiWithSsid发起AP配网

EZOpenSDK

```
/**
 * AP配网接口，如果你的设备热点是EZVIZ_开头的，deviceHotspotName和deviceHotspotPwd可传空；如果不是，这两个参数一定要传入对应的设备热点名和设备热点密码，否则配网失败
 * 封装了设备状态轮询步骤，轮询20次，5秒一次，一共100秒等待时间；如果感觉等待时间过长，可以使用以下方案：
 * 使用此api的同时，创建一个定时器，设置自己期望的一个超时时间。超时后调用stopAPConfigWifiWithSsid，视为配网失败
 *
 * @param wifiSsid                   WiFi的ssid
 * @param wifiPwd                    WiFi的密码
 * @param deviceSerial               设备序列号
 * @param deviceVerifyCode           设备验证码
 * @param deviceHotspotName          设备热点名称，可传空，默认为"EZVIZ_"+设备序列号
 * @param deviceHotspotPwd           设备热点密码,可传空，默认为"EZVIZ_"+设备验证码
 * @param autoConnectToDeviceHotSpot 是否自动连接设备热点,需要获取可扫描wifi的权限
 * @param callback                   结果回调
 */
public void startAPConfigWifiWithSsid(final String wifiSsid, final String wifiPwd, String deviceSerial,
                                      final String deviceVerifyCode, final String deviceHotspotName,
                                      final String deviceHotspotPwd, boolean autoConnectToDeviceHotSpot,
                                      final APWifiConfig.APConfigCallback callback);
```

**示例代码**：(详见ApConfigWifiPresenterForFullSdk.java类实现)

```
private void startConfigWifi(Application app, final Intent configParam) {
    // do something
    // 开始配网
    EzvizApplication.getOpenSDK().startAPConfigWifiWithSsid(wifiSSID, wifiPwd,
        deviceSerial, deviceVerifyCode,
        deviceHotspotSSID, deviceHotspotPwd,
        autoConnect, mConfigCallback);
}

private APWifiConfig.APConfigCallback mConfigCallback = new APWifiConfig.APConfigCallback() {
    @Override
    public void onSuccess() {// SDK将WiFi信息发送给设备后回调此方法（WiFi密码可能错误，设备不一定联网成功）
        if (mCallback == null) {
            return;
        }
        mCallback.onConnectedToWifi();
    }

    @Override
    public void onInfo(int code, String message) {
        if (mCallback == null) {
            return;
        }
        // SDK将WiFi信息发送给设备后，SDK内部会开启轮询设备是否联网成功并注册到平台，如果注册到平台了会回调此code
        if (code == EZConfigWifiInfoEnum.CONNECTED_TO_PLATFORM.code) {
            mCallback.onConnectedToPlatform();
        }
    }

    @Override
    public void OnError(int code) {// AP配网过程中的错误回调
        if (mCallback == null) {
            return;
        }
        LogUtil.e(TAG, "OnError: " + code);
        boolean solved = false;
        if (code == EZConfigWifiErrorEnum.CONFIG_TIMEOUT.code) {
            solved = true;
            mCallback.onTimeout();
        } else if (code == EZConfigWifiErrorEnum.PHONE_NOT_CONNECTED_TO_TARGET_WIFI.code) {
            // TODO: 摄像机要连接的WiFi和手机当前连接的WiFi不一致，SDK内部检测会回调此消息，不用处理
        } else if (code == EZConfigWifiErrorEnum.USER_REFUSED_CONNECTION_REQUEST.code) {
            // TODO: 在Android10及以上系统，使用NetworkSpecifier尝试自动连接到设备热点时，被用户主动拒绝。
        } else if (code == WiFiConnecter.PARAM_ERROR) {
            // TODO: 参数错误
        } else if (code == WiFiConnecter.PASSWORD_ERROR) {
            // TODO: 设备ap热点密码错误
        } else if (code == WiFiConnecter.CONNECT_ERROR) {
            // TODO: 连接ap热点异常
        } else if (code == WiFiConnecter.SCAN_ERROR) {
            // TODO: 搜索WiFi热点错误
        } else if (code == WiFiConnecter.COUNTOUT_ERROR) {
            // TODO: WiFi热点连接错误
        } else {
            // TODO: 其他错误码请查看 EZConfigWifiErrorEnum类
        }

        if (!solved) {
            mCallback.onConfigError(code, null);
        }
    }
};
```

### 4. 第四步添加设备到当前账号下

调用addDevice接口进行设备添加。当状态为EZConfigWifiInfoEnum.CONNECTED\_TO\_PLATFORM时方可添加成功。

EZOpenSDK

```
/**
 * 添加设备
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @param verifyCode   设备验证码，验证码位于设备机身上，6位大写字母
 * @return true 表示成功， false 表示失败
 * @throws BaseException
 */
public boolean addDevice(String deviceSerial, String verifyCode) throws BaseException;
```

**特别说明**： 账户下删除设备重新进行wifi配置并且添加时，请在重置设备等待2分钟以后再调用wifi配置的相关接口可以提高wifi配置的成功率，否则会降低成功率，因为重置设备以后我们平台将在2分钟内得到设备下线的状态，只有平台认为下线了，wifi配置成功率才会高。