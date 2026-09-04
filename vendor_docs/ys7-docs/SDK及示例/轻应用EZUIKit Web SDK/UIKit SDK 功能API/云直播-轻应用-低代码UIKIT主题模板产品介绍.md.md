# 云直播-轻应用-低代码UIKIT主题模板产品介绍.md

> 更新时间: 2026-05-25T16:44:29.000+08:00

> 文档ID: 1759 | 来源树: SDK及示例

---

# 低代码UIKIT主题模板产品介绍

# 轻应用UIKIT产品说明：

轻应用是是基于萤石开放平台JS SDK封装的UI组件，使用过程中不必学习专业的业务概念，更不用调用繁琐的接口，能够以极简的嵌入方式，快速在您的应用中集成视频功能。

# 使用说明：

在集成UIKIT JS SDK后，如果您需要快速集成UI，而不想自己开发时，可以使用我们的UIKIT主题模板

UIKIT JS SDK集成说明：[前往查看](/help/31)

## 参数说明

在初始化参数时，传参 template 可以设置对应uikit的主题模板，官网有提供以下主题模板，也可以在官网上进行主动配置

## 接入方法1：使用官方标准模板

| 模板值 | 描述 | 示例 |
| --- | --- | --- |
| simple | 极简版 \*固定模板 仅包含视频播放窗口，创建实例后通过方法集控制视频播 放相关功能 |  |
| security | 安防版(预览回放); *固定模板 包含视频窗口，叠加了录制，全屏控件， 标清/高清切换，预览录制切换控件* |  |
| voice | 语音版; *固定模板 包含视频窗口，叠加了录制，全屏控件，语音播报，语音 对讲控件* |  |
| pcLive | *固定模板 按钮列表，颜色，底部头部背景色固定，可用于pc端预览，如需 修改按钮配置，头部底部背景色，可参考 {{自定义themeId}}，或者使用 themeData本地配置* |  |
| pcRec | *固定模板 按钮列表，颜色，底部头部背景色固定， 可用于pc端回放，如需 修改按钮配置，头部底部背景色，可参考 {{自定义themeId}}，或者使用themeData 本地配置* |  |
| mobileLive | *固定模板 按钮列表，颜色，底部头部背景色固定，可用于移动端预 览，如需修改按钮配置，头部底部背景色，可参考 {{自定义themeId}}，或者使用themeData 本地配置* |  |
| mobileRec | *固定模板 按钮列表，颜色，底部头部背景色固定， 可用于移动端回放， 如需修改按钮配置，头部底部背景色，可参考 {{自定义themeId}}，或者使用themeData 本地配置* |  |
| 自定义themeId | 自定义主题，[前往开放平台控制台配置页面获取](https://open.ys7.com/console/ezuikit/template.html) （v0.6.2版本及以上支持，建议使用 自定义themeId，或者使用themeData本地 配置）; |  |

## 接入方法2：控制台配置自定义主题模板

#### 创建模板

前往官网：<https://open.ys7.com/console/ezuikit/template.html>，进入控制台，选择云直播-轻应用，即可查看所有模板及进行自定义模板配置。

![](https://resource.eziot.com/group2/M00/00/A8/CtwQFmTU5FmASU9GAAH7ZVIoJKc573.png)

创建模板

![](https://resource.eziot.com/group2/M00/00/A7/CtwQF2TU5FuAfNLJAAC2u7kZsAA659.png)

进入主题模板配置页面

![](https://resource.eziot.com/group2/M00/00/A8/CtwQFmTU5F2ADI2oAAIGhLJIsIs901.png)

配置相关功能后，即可直接复制右侧代码，嵌入自己前端代码中，即可集成