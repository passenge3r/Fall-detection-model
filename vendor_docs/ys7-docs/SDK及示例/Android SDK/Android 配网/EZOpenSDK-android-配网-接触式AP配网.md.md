# EZOpenSDK-android-配网-接触式AP配网.md

> EZOpenSDK-android-配网-接触式AP配网

> 更新时间: 2026-06-02T14:03:43.000+08:00

> 文档ID: 4175 | 来源树: SDK及示例

---

# 接触式AP配网

适用于防跌倒雷达设备、霍曼宠物喂食机等设备；该类设备无视频取流能力，设备标签上无二维码。

## 配网流程

### 1. 第一步获取配网token

EZOpenSDK

```
/**
 * 获取接触式AP配网token
 *
 * @param callback
 */
public void getNewApConfigToken(GetTokenCallback callback);
```

回调的DeviceTokenInfo对象如下

| 属性 | 含义 |
| --- | --- |
| userId | 用户id，暂未使用 |
| token | 接触式AP配网token，必要 |
| lbsDomain | 设备配网后注册平台，必要 |

### 2. 第二步连接设备热点（手动去设置里连接）

该类设备机身上无二维码，需要用户去设置-网络 页面连接上设备热点

### 3. 第三步获取设备信息

连接上设备热点后，回到应用，调用getAccessDeviceInfo获取设备信息

EZOpenSDK

```
/**
 * 获取设备信息（需连接设备热点）
 *
 * @param callback
 */
public void getAccessDeviceInfo(GetAccessDeviceInfoCallback callback);
```

可以拿到设备的序列号AccessDeviceInfo.devSubserial，后面查询设备配网结果用

### 4. 第四步配置设备网络

```
/**
 * 设备配网（向设备发送wifi信息）
 *
 * @param token 通过getNewApConfigToken接口获取的token
 * @param ssid wifi名称
 * @param password wifi密码
 * @param lbsDomain 通过requestConfigToken接口获取的注册地址
 * @param callback
 */
public void startNewApConfigWithToken(String token, String ssid, String password, String lbsDomain, StartNewApConfigCallback callback);
```

入参token 和 lbsDomain 传入第一步中获取到的值。

**示例代码**：

EZOpenSDK

```
EzvizApplication.getOpenSDK().startNewApConfigWithToken(configToken, wifiSsid
        , wifiPwd, tokenInfo.registerUrl, new StartNewApConfigCallback() {
    @Override
    public void onResponse(int statusCode, String statusDesc) {
        waitDialog.dismiss();
        runOnUiThread(() -> {
            logPrintTv.setText(TouchApApi.responseData);
            // 步骤5：开始轮询
            startSearchDeviceTimer();
        });
    }

    @Override
    public void onError(final EzConfigWifiException ezConfigWifiException) {
        // 将信息发送给设备后，设备关闭热点去连接网络，无回调给App，会回调onError，也需要去发起轮询
        runOnUiThread(() -> {
            // 步骤5
            startSearchDeviceTimer();
            Log.e(TAG, "请求失败，错误码 ： " + ezConfigWifiException.errorCode + " 错误信息: "
                    + ezConfigWifiException.message);
        });
        waitDialog.dismiss();
    }
});
```

### 5. 第五步轮询设备绑定状态

EZOpenSDK

```
/**
 * 查询设备绑定状态
 *
 * @param deviceSerial 设备序列号
 * @param callback
 */
public void queryPlatformBindStatus(String deviceSerial, QueryPlatformBindStatusCallback callback);
```

isBindSuccess == true时，说明设备绑定到账号成功了。

**详见Demo代码中的TouchApActivity.java类实现。**