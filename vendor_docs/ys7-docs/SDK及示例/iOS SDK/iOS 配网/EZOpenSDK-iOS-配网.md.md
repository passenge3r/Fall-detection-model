# EZOpenSDK-iOS-配网.md

> EZOpenSDK-iOS-配网

> 更新时间: 2026-06-02T14:03:52.000+08:00

> 文档ID: 4097 | 来源树: SDK及示例

---

# 配网简介

将萤石摄像头与家庭或企业的网络（通常是Wi-Fi网络）进行连接和配置，使其能够通过网络实现远程控制、数据传输等功能的过程。

## 配网方式

SDK提供以下几种配网方式

| 配网方式 | 说明 |
| --- | --- |
| AP配网 | AP（Access Point，无线接入点）配网是一种常见的摄像机或智能设备连接到Wi-Fi网络的方式。它通过创建一个临时的Wi-Fi热点（即AP模式），使设备能够更方便地获取Wi-Fi设置信息并连接到目标网络。 |
| 声波配网 | 设备通过发出特定频率的声波，用户使用手机等设备接收并解析声波，从而实现配网。 |
| 一般配网（Smart配网） | 让设备能够快速、轻松地连接到网络，SDK会根据设备自动选择配网模式，自动配网。如果Smart配网不生效，可以让用户选择其他指定的配网方式。 |
| 接触式AP配网 | 适用于防跌倒雷达设备、霍曼宠物喂食机等设备；该类设备无视频取流能力，设备标签上无二维码。 |
| 新协议AP配网 | 海外爱加三方设备专用。 |
| 网线配网 | 给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。 |

## 配网能力集

设备支持哪些配网方式依赖于设备的能力，可通过设备能力集进行判断。调用如下接口可获取到该设备的EZProbeDeviceInfo对象信息。

EZOpenSDK.h

```
/**
 *  查询设备信息（用于添加设备之前, 简单查询设备信息，如是否在线，是否添加等）
 *
 *  @param deviceSerial 设备序列号
 *  @param deviceType     设备型号，无法获取到设备型号则可传nil
 *  @param completion     回调block，正常时返回EZProbeDeviceInfo对象，错误码返回错误码
 *  @see 全新的设备是没有注册到平台的，所以会出现设备不存在的情况，设备wifi配置成功以后会上报数据到萤石云平台，以后每次查询就不会出现设备不存在的情况了。
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)probeDeviceInfo:(NSString *)deviceSerial
                               deviceType:(NSString *)deviceType
                               completion:(void (^)(EZProbeDeviceInfo *deviceInfo, NSError * __nullable error))completion;
```

  

EZProbeDeviceInfo对象部分属性说明如下

| 属性 | 值和含义 |
| --- | --- |
| supportAP | 是否支持AP配网，2-支持AP，其他值为不支持AP配网 |
| supportSoundWave | 是否支持声波配置，0-不支持，1-支持 |
| supportWifi | 是否支持wifi，0-不支持，1-支持，2-支持带userId的新的wifi配置方式，3-支持smartwifi |
| supportAPType | AP配网协议类型，1-HTTP 2-NETSDK |

**注意**：以上属性均为计算型属性，须调用后才能查看具体的值。未调用时，查看EZProbeDeviceInfo中的以上属性显示是0

## 接入配网方式选择

Question：SDK支持以上多种配网方式，那么开发者需要接入哪些配网方式？

Answer：

- AP配网：如果采购的设备支持AP配网（即EZProbeDeviceInfo.supportAP = 2），那么**只需要接入AP配网即可**，不用管是否支持其他配网方式；一般设备都支持AP配网；
- 声波配网：如果采购的设备不支持AP配网，EZProbeDeviceInfo.supportSoundWave = 1，则可接入该配网方式；
- 一般配网（Smart配网）：如果采购的设备不支持AP配网，EZProbeDeviceInfo.supportWifi = 3，则可接入该配网方式；
- 声波配网 & 一般配网：如果设备同时支持这两种配网方式，则可以使用混合模式进行配网，提高配网速度；详情参考demo，调用EZOpenSDK.startConfigWifi，其中入参mode传EZWiFiConfigSmart | EZWiFiConfigWave；
- 接触式AP配网：适用于防跌倒雷达设备、霍曼宠物喂食机等设备；该类设备无视频取流能力，设备标签上无二维码；
- 新协议AP配网：EZProbeDeviceInfo.supportAPType = 1，海外爱加三方设备专用；
- 网线配网：给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。

## SDK Demo配网流程图

![SDK Demo配网流程图](https://resource.eziot.com/group2/M00/01/07/CtwQF2iIOtKAcrJnAAJQJonnQpQ246.png)

注：建议通过鼠标右键将图片存储到本地进行查看，官网的图片查看有点问题。