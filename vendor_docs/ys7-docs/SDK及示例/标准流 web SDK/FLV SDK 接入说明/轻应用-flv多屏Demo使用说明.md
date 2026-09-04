# 轻应用-flv多屏Demo使用说明

> 轻应用-flv多屏Demo使用说明

> 更新时间: 2026-05-25T16:44:37.000+08:00

> 文档ID: 5109 | 来源树: SDK及示例

---

# FLV 多屏Demo说明

一个灵活的分屏布局组件，支持多种分屏模式、自定义布局、主题切换和国际化。

![Download](https://img.shields.io/npm/dm/@ezuikit/multi-screen.svg) ![Version](https://img.shields.io/npm/v/@ezuikit/multi-screen.svg) ![License](https://img.shields.io/npm/l/@ezuikit/multi-screen.svg) ![Build Demos](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/workflows/build-demos/badge.svg)

## 特性

- ✅ 支持 1、2、4、6、9、16 分屏模式
- ✅ 支持自定义分屏布局
- ✅ 自适应父元素大小
- ✅ 单个屏幕选中功能
- ✅ 左上角序号显示
- ✅ 底部工具栏控制分屏切换
- ✅ 网页全屏和全局全屏支持
- ✅ 主题切换（亮色/暗色）
- ✅ 多语言支持（中文/英文）
- ✅ 事件回调系统

## 快速开始

### 安装依赖

```
npm install @ezuikit/multi-screen

# or
yarn add @ezuikit/multi-screen

# or
pnpm add @ezuikit/multi-screen
```

## 使用示例

### 构造函数

```
new MultiScreen(containerID, Player, options);
```

- containerID: string：容器元素 id（内部使用 document.getElementById(containerID)）
- Player: new (...args: any[]) => AbstractPlayer：播放器类构造器
- options: [MultiScreenOptions](https://github.com/Ezviz-OpenBiz/EZUIKit-MultiScreen/blob/main/API.md#%E6%9E%84%E9%80%A0%E5%87%BD%E6%95%B0%E9%80%89%E9%A1%B9)：初始化配置

### 基础用法

```
// 引入样式
import "@ezuikit/multi-screen/dist/style.css";
// 引入flv样式
import "ezuikit-flv/style.css";
import MultiScreen from "@ezuikit/multi-screen";
// 引入flv
import EzuikitFlv from "ezuikit-flv";

const screens = new MultiScreen("app", EzuikitFlv, {
    mode: 4, // 分屏模式
    theme: "dark",
    language: "zh",
    screens: [
       { url: "https://example.com/live1.flv" },
       { url: "https://example.com/live2.flv" },
     ],
});
```

完整的用例请参考[with-react-ts/src/App.tsx](https://github.com/Ezviz-OpenBiz/EZUIKit-MultiScreen/blob/main/examples/with-react-ts/src/App.tsx)

### 动态操作

```
// 切换模式
screens.setMode(9);

// 切换自定义布局
screens.setMode({ rows: 3, cols: 5 });

// 切换主题
screens.setTheme("light");

// 监听事件
screens.on("screen:click", (index, screen) => {
    console.log("屏幕被点击:", index);
});
```

## API 概览

### 初始化配置（MultiScreenOptions）

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| width | string | number | - | 容器宽度（类型定义支持；通常可通过 resize() 动态设置） |
| height | string | number | - | 容器高度（类型定义支持；通常可通过 resize() 动态设置） |
| mode | 1 | 2 | 4 | 6 | 9 | 16 | 'custom' | 4 | 分屏模式 |
| customLayout | { rows: number; cols: number } | null | 自定义网格（mode='custom' 时生效） |
| screens | ScreenItem[] | [] | 分屏数据；数量不足当前分屏数时自动补 null |
| theme | 'light' | 'dark' | 'dark' | 主题 |
| language | 'zh' | 'en' | 'zh' | 语言（非法值会回退 zh） |
| showToolbar | boolean | true | 是否显示工具栏 |
| scaleMode | 0 | 1 | 2 | 1 | 画面缩放模式 |
| audioMode | 'selected' | 'all' | 'muted' | 'muted' | 音频模式 |
| enableHardwareDecoding | boolean | true | 是否启用硬件解码（传入播放器参数 useMSE） |
| plugins | ControlConstructor[] | [] | 追加到左侧工具栏的自定义控件类 |
| placeholder | string | (() => string) | i18n: clickToSelect | 空分屏占位内容 |
| onScreenClick | (index, screen) => void | () => {} | 分屏点击回调（内部绑定到 screen:click） |
| onModeChange | (mode) => void | () => {} | 模式切换回调（内部绑定到 mode:change） |
| onFullscreenChange | (isFullscreen, type) => void | () => {} | 全屏变化回调（内部绑定到 fullscreen:change） |

### ToolbarPlugin 结构

```
interface ToolbarPlugin {
    name: string;
    content: string | ((layout: MultiScreen) => string);
    tooltip?: string | ((layout: MultiScreen) => string);
    disabledDefault?: boolean;
    wrapperClassName?: string;
    onClick: (layout: MultiScreen) => void;
}
```

### 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| mode | LayoutMode | 当前分屏模式 |
| players | (AbstractPlayer | null)[] | 当前播放器实例数组 |
| controls | Record<string, Control> | 当前工具栏控件实例映射 |
| scaleMode | 0 | 1 | 2 | 当前缩放模式 |
| audioMode | 'selected' | 'all' | 'muted' | 当前音频模式 |
| isWebFullscreen | boolean | 是否网页全屏 |
| isGlobalFullscreen | boolean | 是否浏览器全屏 |
| enableHardwareDecoding | boolean | 是否启用硬件解码 |
| language | string | 当前语言 |
| current | number | 当前选中窗口索引（从 1 开始） |

> current 是 getter/setter：赋值会触发选中逻辑并触发 screen:click。

### 方法

#### setMode(mode: LayoutMode | CustomLayout): void

设置分屏模式。

- 传入预设值（如 4/9）时直接切换。
- 传入 { rows, cols } 时会切到 custom。
- 触发事件：mode:change。

#### setScreen(screen: ScreenItem, index?: number): void

设置某个窗口的数据并重建该窗口播放器。

- index 从 1 开始，默认当前窗口。
- 越界时输出 console.warn('Invalid index')。

#### close(index?: number): void

关闭窗口并销毁对应播放器，删除该窗口数据（置 null）。

- index 从 1 开始，默认当前窗口。

#### setTheme(theme: 'light' | 'dark'): void

设置主题并触发 theme:change。

#### toggleWebFullscreen(): Promise

切换网页全屏（容器类名切换），触发 fullscreen:change（type='web'）。

#### toggleFullscreen(): Promise

切换浏览器全屏（screenfull），触发 fullscreen:change（type='global'）。

#### play(index?: number): void

播放指定窗口或全部窗口。

#### pause(index?: number): void

暂停指定窗口或全部窗口。

#### muted(muted = true, index?: number): void

设置指定窗口或全部窗口静音状态。

#### screenshot(filename?, format = 'png', quality = 0.92, type = 'download', index?): void

截图当前或指定窗口。

- format：'png' | 'jpeg' | 'webp'
- type：'download' | 'base64' | 'blob'
- 实际截图数据返回取决于底层播放器 player.screenshot(...) 实现。

#### setScaleMode(scaleMode: 0 | 1 | 2, index?: number): void

设置缩放模式并应用到指定窗口或全部窗口。

#### setAudioMode(audioMode: 'selected' | 'all' | 'muted'): void

设置音频模式：

- muted：全部静音
- all：全部有声
- selected：仅当前选中窗口有声

#### resize(width?: number | string, height?: number | string): void

修改容器尺寸；数字按 px 处理，字符串按 CSS 值处理。

#### destroy(): void

销毁组件，清理播放器、控件、事件监听、DOM 内容。

## 事件

MultiScreen 继承 EventEmitter ，支持 on / off / once / emit。

### 事件列表

| 事件名 | 回调签名 | 触发时机 |
| --- | --- | --- |
| screen:click | (index: number, screen: ScreenItem) => void | 窗口被选中时（包括设置 current、点击窗口） |
| mode:change | (mode: LayoutMode) => void | 调用 setMode() 切换后 |
| fullscreen:change | (isFullscreen: boolean, type: 'web' | 'global') => void | 调用网页全屏/浏览器全屏切换，或全屏状态变化时 |
| theme:change | (theme: 'light' | 'dark') => void | 调用 setTheme() 后 |

#### 初始化回调 vs 事件监听

初始化配置中的：

- onScreenClick
- onModeChange
- onFullscreenChange

本质是构造阶段自动调用 screens.on(...) 的快捷写法。你也可以在实例化后自行监听：

```
screens.on("screen:click", (index, screen) => {});
screens.on("mode:change", (mode) => {});
screens.on("fullscreen:change", (isFullscreen, type) => {});
screens.on("theme:change", (theme) => {});
```

## examples

### with-base

原生环境下使用umd demo [with-base/index.html](https://github.com/Ezviz-OpenBiz/EZUIKit-MultiScreen/blob/main/examples/with-base/index.html)

### with-react-ts

React + TypeScript demo [with-react-ts/src/App.tsx](https://github.com/Ezviz-OpenBiz/EZUIKit-MultiScreen/blob/main/examples/with-react-ts/src/App.tsx)

### with-vue-ts

Vue2.5 demo [with-vue2.5/src/components/index.vue](https://github.com/Ezviz-OpenBiz/EZUIKit-MultiScreen/blob/main/examples/with-vue2.5/src/components/index.vue)