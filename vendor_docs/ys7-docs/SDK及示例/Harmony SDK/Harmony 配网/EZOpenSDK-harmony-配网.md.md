# EZOpenSDK-harmony-配网.md

> EZOpenSDK-harmony-配网

> 更新时间: 2026-06-02T14:04:00.000+08:00

> 文档ID: 4212 | 来源树: SDK及示例

---

# 配网简介

将萤石摄像头与家庭或企业的网络（通常是Wi-Fi网络）进行连接和配置，使其能够通过网络实现远程控制、数据传输等功能的过程。

## 配网方式

SDK提供以下几种配网方式

| 配网方式 | 说明 |
| --- | --- |
| AP配网 | AP（Access Point，无线接入点）配网是一种常见的摄像机或智能设备连接到Wi-Fi网络的方式。它通过创建一个临时的Wi-Fi热点（即AP模式），使设备能够更方便地获取Wi-Fi设置信息并连接到目标网络。 |
| 网线配网 | 给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。 |

## 配网能力集

设备支持哪些配网方式依赖于设备的能力，可通过设备能力集进行判断。调用如下接口可获取到该设备的EZProbeDeviceInfo对象信息。

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

  

EZProbeDeviceInfo对象方法说明如下

| 方法 | 值和含义 |
| --- | --- |
| getSupportAP | 是否支持AP配网，2-支持AP，其他值为不支持AP配网 |

## 接入配网方式选择

Question：SDK支持以上多种配网方式，那么开发者需要接入哪些配网方式？

Answer：

- AP配网：如果采购的设备支持AP配网（即EZProbeDeviceInfo.supportAP = 2），那么**只需要接入AP配网即可**，不用管是否支持其他配网方式；一般设备都支持AP配网；