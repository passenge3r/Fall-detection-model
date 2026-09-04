# 海康Ehome协议接入

> 海康Ehome协议接入

> 更新时间: 2025-03-20T02:17:20.000+08:00

> 文档ID: 3872 | 来源树: 云接入

---

# · 接入流程概览：

![](https://resource.eziot.com/group1/M00/01/5A/CtwQE2cyywuAaPDFAAEoauifITU334.png)

# · 完整接入流程：

## 一. 绑定设备，获取接入参数（共2步）

### 1. 进入“[Ehome控制台](https://open.ys7.com/console/ehome.html)”页，支持**绑定设备/批量绑定设备**申请Ehome设备所需的设备信息。

（以下操作以“绑定设备”为例展示，不进行批量绑定的操作展示。）

\*注意：绑定设备后，即开始进行计费。

| 填写项 | 说明 |
| --- | --- |
| 设备名称 | 可支持自定义，用于标注设备的具体名字。 |
| 设备密码 | 设备的密码，4-20位，可包含大小写字母、数字（大小写字母敏感）。 |
| 通道数 | 通道数数量，可输入0-999的整数 |

![](https://resource.eziot.com/group1/M00/01/5A/CtwQEmcyv5qAc-GrAAHQFsrIgp4507.png)

### 2. 完成后，您可以在“[Ehome控制台](https://open.ys7.com/console/ehome.html)”中查看到申请的设备信息。在配置过程中，所需的设备信息，可以通过 **“设备详情”** 按钮进行查看。

![](https://resource.eziot.com/group1/M00/01/5A/CtwQE2cyv52AdVDTAAGWRT0HMPs337.png)

## 二. 获取设备IP，准备进行设备注册（共2步）

### 1. 局域网内搜索设备

将设备与PC接在同一个局域网内，下载SADP工具，打开SADP，点击刷新按钮搜索局域网设备。

![](https://resource.eziot.com/group1/M00/01/5A/CtwQEmcy8zyAPMvJAADFx5Lnvdw903.png)

### 2. 选择需要注册的设备，获取其IP地址

\*可双击ip地址，进入设备web客户端界面。

![](https://resource.eziot.com/group1/M00/01/5A/CtwQE2cy8z6ACIwrAAIY8qM4iGk594.png)

## 三. 注册设备（共3步）

### 1. 进入设备web客户端界面。（激活密码需要咨询设备所属者）

![](https://resource.eziot.com/group1/M00/01/5A/CtwQE2cy-1SAUtAvAAgQstgiZPU597.png)

### 2. 进入Ehome接入配置入口

【控制台配置指南】

![](https://resource.eziot.com/group1/M00/01/5A/CtwQEmcy-1aAVf2HAAGyZ7Zbp4M348.png)
![](https://resource.eziot.com/group1/M00/01/64/CtwQEmdSakeAP0bgAADY_smbLg8511.png)

\*注：如果设备保存时提示参数错误，可能是设备序列号的校验格式问题，虽然ehome协议本身不禁止“:”字符，但是部分设备可能把“:”当做特殊字符来处理了。

请把“:”使用其他字符替换，比如“a”，服务端做了兼容，支持使用其他字符代替“:”。

### 3. 配置相关信息

| 所需配置信息名称 | 获取方式 | 备注 |
| --- | --- | --- |
| 平台接入方式 | ISUP |  |
| 白名单 | 若因为设备所连网络为内网，或网络有防火墙相关限制，导致设备无法在控制台正常上线，则建议将萤石云ip配置至该白名单 | 电信：115.238.23.87；联通：101.71.31.87 ；移动：112.17.34.17；端口：7660 |
| 启用 | √ | 重新注册操作为：将勾选去除，点击确认。刷新界面后，重新勾选并点击确认 |
| 协议版本 | Ehome2.0 | 现平台支持Ehome2.0版本 |
| 服务器地址 | 可以选择填写域名或注册。 域名：ehome.ys7.com IP：电脑连接在设备所在网络环境下，“Win+R”-“输入cmd”-输入“ping ehome.ys7.com” 会拿到当前网络对应运营商的服务注册IP地址。域名允许ping 4次 | 电信：115.238.23.87 联通：101.71.31.87 移动：112.17.34.17 注册端口：7660 |
| 端口 | 对应服务器端口。 |  |
| 设备ID | 对应设备ID。 |  |
| 注册状态 |  | 配置完成后，刷新配置页面，等到注册状态为“在线”后，表示设备注册成功，设备端已上线。 |

## 四. 测试设备（共1步）

### 1.您可在“Ehome控制台”页面，核对“设备状态”是否为在线（一般完成配置后，在线状态更新为8s-60s。），并点击“播放地址”等按钮测试设备是否能否正常播放。

![](https://resource.eziot.com/group1/M00/01/5A/CtwQEmczBu2AZdlOAAG8RDYbsnU990.png)