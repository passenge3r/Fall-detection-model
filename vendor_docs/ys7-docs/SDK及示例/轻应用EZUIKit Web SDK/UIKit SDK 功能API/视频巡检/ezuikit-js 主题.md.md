# ezuikit-js 主题.md

> 更新时间: 2026-05-25T16:44:32.000+08:00

> 文档ID: 4290 | 来源树: SDK及示例

---

# 主题模板

## 官方主题

EZUIKit内置5个主题，可以在初始化阶段通过template字段指定。

| 主题id | 主题名称 |
| --- | --- |
| pcLive | WEB端预览主题 |
| pcRec | WEB端回放主题 |
| mobileLive | 移动端H5预览主题 |
| mobileRec | 移动端H5回放主题 |
| simple | 极简主题 |

## 主题配置

EZUIKit支持用户根据需求配置主题按钮是否展示。您可以通过themeData字段配置主题。

**字段说明**

| key | 含义 |
| --- | --- |
| autoFocus | 自动隐藏主题延时，为0时不自动隐藏 |
| header | 顶部区域 |
| footer | 底部按钮区域 |
| color | 默认文本颜色 |
| activeColor | 激活文本颜色 |
| backgroundColor | 背景颜色 |
| btnList | 按钮列表 |
| iconId | 按钮id |
| part | 按钮区域，left：置于左侧，right：置于右侧 |
| defaultActive | 默认是否激活按钮 |
| memo | 按钮提示文本 |
| isrender | 是否渲染按钮 |

**代码示例**

```
{
    "autoFocus": 5,
    "header": {
        "color": "#1890ff",
        "activeColor": "#FFFFFF",
        "backgroundColor": "#000000",
        "btnList": [
            {
                "iconId": "deviceID",
                "part": "left",
                "defaultActive": 0,
                "memo": "顶部设备名称",
                "isrender": 1
            },
            {
                "iconId": "deviceName",
                "part": "left",
                "defaultActive": 0,
                "memo": "顶部设备ID",
                "isrender": 1
            },
            {
                "iconId": "cloudRec",
                "part": "right",
                "defaultActive": 0,
                "memo": "头部云存储回放",
                "isrender": 0
            },
            {
                "iconId": "rec",
                "part": "right",
                "defaultActive": 0,
                "memo": "头部本地回放",
                "isrender": 0
            }
        ]
    },
    "footer": {
        "color": "#FFFFFF",
        "activeColor": "#1890FF",
        "backgroundColor": "#00000021",
        "btnList": [
            {
                "iconId": "play",
                "part": "left",
                "defaultActive": 1,
                "memo": "播放",
                "isrender": 1
            },
            {
                "iconId": "capturePicture",
                "part": "left",
                "defaultActive": 0,
                "memo": "截屏按钮",
                "isrender": 1
            },
            {
                "iconId": "sound",
                "part": "left",
                "defaultActive": 0,
                "memo": "声音按钮",
                "isrender": 1
            },
            {
                "iconId": "pantile",
                "part": "left",
                "defaultActive": 0,
                "memo": "云台控制按钮",
                "isrender": 1
            },
            {
                "iconId": "recordvideo",
                "part": "left",
                "defaultActive": 0,
                "memo": "录制按钮",
                "isrender": 1
            },
            {
                "iconId": "talk",
                "part": "left",
                "defaultActive": 0,
                "memo": "对讲按钮",
                "isrender": 1
            },
            {
                "iconId": "zoom",
                "part": "left",
                "defaultActive": 0,
                "memo": "电子放大",
                "isrender": 1
            },
            {
                "iconId": "hd",
                "part": "right",
                "defaultActive": 0,
                "memo": "清晰度切换按钮",
                "isrender": 1
            },
            {
                "iconId": "webExpend",
                "part": "right",
                "defaultActive": 0,
                "memo": "网页全屏按钮",
                "isrender": 1
            },
            {
                "iconId": "expend",
                "part": "right",
                "defaultActive": 0,
                "memo": "全局全屏按钮",
                "isrender": 1
            }
        ]
    }
}
```