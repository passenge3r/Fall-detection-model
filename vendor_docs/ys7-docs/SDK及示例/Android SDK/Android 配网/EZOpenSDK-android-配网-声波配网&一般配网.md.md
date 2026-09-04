# EZOpenSDK-android-配网-声波配网&一般配网.md

> EZOpenSDK-android-配网-声波配网&一般配网

> 更新时间: 2026-06-02T14:03:43.000+08:00

> 文档ID: 4174 | 来源树: SDK及示例

---

# 声波配网 & 一般配网（Smart）

声波配网：设备通过发出特定频率的声波，用户使用手机等设备接收并解析声波，从而实现配网。

一般配网（Smart）：让设备能够快速、轻松地连接到网络，SDK会根据设备自动选择配网模式，自动配网。

声波配网 和 一般配网（Smart）的流程是一样的，只是入参区别。

## 配网流程

### 1. 第一步查询设备信息

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
        if (mEZProbeDeviceInfo != null){
            if (mEZProbeDeviceInfo.getBaseException() == null){
                // TODO: 2018/6/25 添加设备
                sendMessage(MSG_QUERY_CAMERA_SUCCESS);
            } else {
                switch (mEZProbeDeviceInfo.getBaseException().getErrorCode()){

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

### 2. 第二步配置设备网络

待设备提示配网时，调用startConfigWifi发起配网

EZOpenSDK

```
/**
 * 开始WiFi配置
 *
 * @param context      应用 activity context
 * @param deviceSerial 配置设备序列号
 * @param ssid         连接WiFi SSID
 * @param password     连接  WiFi 密码
 * @param mode         配网的方式，EZWiFiConfigMode中列举的模式进行任意组合,例如:EZWiFiConfigMode.EZWiFiConfigSmart|EZWiFiConfigMode.EZWiFiConfigWave
 * @param back         配置回调
 * @since 4.8.3
 */
public void startConfigWifi(Context context, String deviceSerial, String ssid, String password, int mode, EZOpenSDKListener.EZStartConfigWifiCallback back);
```

**示例代码**：

```
private void start() {
    // do something
    int mode = 0;
    mode |= support_Wifi?EZConstants.EZWiFiConfigMode.EZWiFiConfigSmart:0;
    mode |= support_sound_wave?EZConstants.EZWiFiConfigMode.EZWiFiConfigWave:0;
    getOpenSDK().startConfigWifi(AutoWifiConnectingActivity.this, serialNo, wifiSSID, wifiPassword,
                        EZConstants.EZWiFiConfigMode.EZWiFiConfigWave, mEZStartConfigWifiCallback);
}

EZOpenSDKListener.EZStartConfigWifiCallback mEZStartConfigWifiCallback =
    new EZOpenSDKListener.EZStartConfigWifiCallback() {
        @Override
        public void onStartConfigWifiCallback(String deviceSerial, final EZConstants.EZWifiConfigStatus status) {
            AutoWifiConnectingActivity.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (status == EZConstants.EZWifiConfigStatus.DEVICE_WIFI_CONNECTING) {

                    } else if (status == EZConstants.EZWifiConfigStatus.DEVICE_WIFI_CONNECTED) {
                        // do something
                    } else if (status == EZConstants.EZWifiConfigStatus.DEVICE_PLATFORM_REGISTED) {
                        // 开始绑定操作 do something
                    }
                }
            });
        }
    };
```

### 3. 第三步添加设备到当前账号下

调用addDevice接口进行设备添加。当状态为EZConstants.EZWifiConfigStatus.DEVICE\_PLATFORM\_REGISTED时方可添加成功。

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