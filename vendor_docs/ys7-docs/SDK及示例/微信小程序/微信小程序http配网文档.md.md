# 微信小程序http配网文档.md

> 微信小程序http配网文档

> 更新时间: 2026-06-03T10:39:22.000+08:00

> 文档ID: 523 | 来源树: SDK及示例

---

# 微信小程序http配网

本配网方案支持 CS-CTQ6X-V101-1G2WF和CS-CTQ6N-V101-1G2WF 两种型号的设备配网。连接设备热点后，向设备发送目标网络（给设备配置的wifi）的SSID、BSSID和password信息，给设备连接目标网络。

## 1 前提条件

- 微信 App iOS 最低版本要求：8.0.10以上。
- 微信 App Android 最低版本要求：8.0.10以上。
- 小程序基础库最低版本要求：2.10.0。

## 2  跑通demo

### 2.1 小程序控制台配置域名

在【微信公众平台】>【开发】>【开发管理】>【开发设置】>【服务器域名】中设置"request合法域名"【https://open.ys7.com】

### 2.2 下载配网demo源码

[配网demov1.4\_20230721源码](https://resource.eziot.com/group1/M00/00/D9/CtwQE2S6K3GAGfBAAApIuRWx5LA870.zip)

[配网demo\_v1.5\_20260602源码](https://izhstatic.ys7.com/vasp-openweb/1780406666034_配网demo_v1.5_20260602源码.zip)

### 2.3 配置demo与运行

---

1. 打开微信开发者工具，选择小程序，单击新建图标，选择导入项目。
2. 填写您微信小程序的 AppID，单击确定。
3. 导入您下载的demo源码，找到pages/home/home.js文件，设置相关参数。

- `accessToken: '', // 开放平台访问令牌`

1. 单击预览，生成二维码，通过手机微信扫码二维码即可进入小程序。

## 3 开发指南

### 3.1 小程序控制台配置域名

已配置可忽略

在【微信公众平台】>【开发】>【开发管理】>【开发设置】>【服务器域名】中设置"request合法域名"【https://open.ys7.com】

### 3.2 整体流程

![整体流程](https://resource.eziot.com/group1/M00/00/9B/CtwQEmNOUHSAWUcoAAAzS0vmFfo357.png)

### 3.3 开发流程

#### 3.3.1 导入sdk

将demo中sdk代码（lib文件夹）放入您的目录下（demo中放置在根目录下）。

```
import {EConnectWifi} from '../../../lib/ez-wechat-connectwifi-sdk/index';

const eConnectWifi = EConnectWifi();
```

#### 3.3.2 查询设备信息

> 可参考/packageD/pages/queryDevice/index页面

```
eConnectWifi.searchDeviceInfo(accessToken, deviceSerial).then(res => {

}).catch(err => {

})
```

响应参数

| code | msg | data |
| --- | --- | --- |
| 200 | 设备处于可被添加的状态（在线无异常未被添加） | displayName：设备默认名称 status：设备在线状态：1-在线，0-不在线 model：设备型号 |
| 10001 | 参数错误 |  |
| 10004 | 用户不存在 |  |
| 10002 | accessToken过期或异常 |  |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20020 | 设备在线，已经被自己添加 |  |
| 20013 | 设备已被别人添加 |  |
| 20023 | 设备不在线，未被用户添加 |  |
| 20029 | 设备不在线，已经被自己添加 |  |
| 49999 | 获取设备信息异常 |  |

#### 3.3.3 连接目标网络

> 可参考/packageD/pages/initWifi/index页面

我们通过微信小程序提供的getConnectedWifi函数获取目标wifi的**BSSID, SSID**，[微信小程序获取已连接中的 Wi-Fi 信息API](https://developers.weixin.qq.com/miniprogram/dev/api/device/wifi/wx.getConnectedWifi.html)

```
wx.startWifi({

   success (res) {

   console.log(res.errMsg);

   wx.getConnectedWifi({ 

     success (res) {

     	console.log('当前连接的wifi：',res);

     	if (res && res.wifi) {

       		const {BSSID, SSID} = res.wifi;  

   	 		// 此处，您可以拿到当前连接的目标wifi的BSSID, SSID

      	}

     },

    fail(err) {

      
     console.log('获取连接的wifi', err);

     }

    })

   }

  });
```

**tips：**

- 目标wifi密码（**wifiPassword**），无法通过微信小程序提供的API获取，因此需要您已知。
- 建议您使用4G网络wifi，暂不支持5Gwifi配网

##### 如果您的手机尚未连接目标wifi,您可以通过[微信小程序连接 Wi-Fi API](https://developers.weixin.qq.com/miniprogram/dev/api/device/wifi/wx.connectWifi.html)先连接目标网络，获取到目标网络的BSSID, SSID。

```
wx.startWifi({

  success (res) {

   console.log(res.errMsg);

   wx.connectWifi({ 

    SSID: SSID,

    password: wifiPassword,

    success (res) {

     console.log('connectWifi success:', res);

     if (res.errCode == 0 || res.errMsg == 'connectWifi:ok') {}

     }

   })

  }

 })
```

#### 3.3.4 给设备配网

> 可参考/packageD/pages/connectWifi/index页面

**注意：因安全需要，我们无法校验您的设备验证码（validateCode）是否正确，但是希望您确保设备验证码正确性，否则无法连上设备网络，给设备配网**。

```
eConnectWifi.connectWifi(deviceSerial, validateCode, accessToken, BSSID, SSID, wifiPassword).then(() => {
    
}).catch(err => {
    
})
```

**tips:**

- 仅AP+STA同时支持的设备可准确响应。
- 给设备配网时，设备响应有延迟，因此开发者也可使用EConnectWifi.searchDeviceInfo （详见3.3.2 查询设备信息接口）设置定时器查询。
- 配网过程中，微信小程序会先连接设备wifi，该网络不可用于其他网络请求，只可用于我们给设备传递目标网络的信息，接收到目标网络信息后，设备wifi才会断开，小程序将连接可用的wifi。因此，在demo中设备名称设置页中【完成按钮】需要等小程序连上可用wifi后才可进行下一步。
- 若微信小程序官网联网API无法连接成功设备wifi，用户可以手动连接设备wifi，设备wifif名称为*SoftAP\_设备序列号*，设备密码为*SoftAP\_设备验证码*。
- **运行demo时需将官方示例替换为真实的accesstoken**。

**更新日志：**

- v1.3\_20230403  
    
  1、针对设备添加接口增加重试机制，降低因设备上下线状态延迟造成设备绑定失败率
- v1.4\_20230721  
    
  1、重新梳理了sdk中connectWifi方法，修复部分安卓机型在调用wx.connectWifi时会调用失败，改为弹出提示框跳转wifi列表  
    
  2、删除wx.onWifiConnected事件监听，部分机型连接设备wifi成功，但返回ssid为空字符串的情况  
    
  3、增加设备下发接口重试机制，调用失败或超时会进行重试，重试次数超过3次且任务总时长超过90秒会退出配网  
    
  4、新增错误广播"connectWifi:fail:connect cancel"，在wx.connectWifi失败后，点击弹出框的取消按钮触发，在eConnectWifi.connectWifi的catch函数中捕获
- v1.5\_20260602

       1、修复 taskConnectDeviceWifi 内 Promise.reject(new Error(res)) 写法导致外层 try/catch 捕获不到的问题，改为 throw。

       2、放宽入参 BSSID 校验，部分机型 getConnectedWifi 返回 BSSID 为空时不再被拦截。

       3、扫码二维码切分支持 \t、\n、\r、\r\n 多种分隔。

       4、SDK 内部不再直接调用 wx.showToast（除"手动连接"兜底 modal 外），所有错误统一以 reject(code) 抛出，UI 由调用方接管。

       5、新增 configStatusSetting() 方法用于发起配网前重置取消标志；新增 \_busy 互斥，连续调用 connectWifi 第二次直接 reject connectWifi:fail:busy。

       6、其他请详见demo中【帮助中心\_v1.5补充.md】