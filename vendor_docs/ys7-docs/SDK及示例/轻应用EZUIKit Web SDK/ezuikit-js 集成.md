# ezuikit-js 集成

> ezuikit-js 集成

> 更新时间: 2026-06-25T14:55:14.000+08:00

> 文档ID: 4294 | 来源树: SDK及示例

---

# 轻应用UIKIT 接入说明

轻应用公UIKIT是萤石开放平台针对web/H5页面的视频接入：

ezopen JS SDK：基于萤石ezopen私有协议，对视频流进行加密，确保设备出流安全的JavaScript SDK，支持H264/H265视频解码, 支持 AAC / G711 / G722 音频解码

# UIKit 介绍

## 产品介绍

产品介绍，详见：<https://open.ys7.com/help/4424>

# 开发接入：

## 一、安装

**1、npm引入**

```
npm install ezuikit-js
```

or

```
yarn add ezuikit-js
```

or

```
pnpm add ezuikit-js
```

**2、本地引入**

### 请勿使用 CDN 引入方案

- 萤石官方**未提供公共 CDN 地址**
- 任何 `open.ys7.com` 域名下的 JS 文件直链
- 任何 `unpkg.com` 等三方公共CDN服务提供的萤石SDK包

以上情况可能出现资源加载失败、资源跨域等导致取流播放失败的情况。

① 访问我们的github或者gitee项目地址：

```
** github**
https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm

**gitee**
https://gitee.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm
```

② Clone或下载ZIP包到本地，并将 `ezuikit.js` 文件及 `ezuikit_static` 文件夹放在项目中合适的位置

③ 在项目中引入ezuikit依赖库

```
import EZUIKit from "ezuikit-js";
```

or

```
// 推荐（>= v8.1.2 ）
//  ESM引入
import { EZUIKitPlayer } from "ezuikit-js";
```

or

```
// UMD引入（原生HTML）
<script src="./ezuikit.js"></script>
```

若您对如何在项目本地引入UIKit仍然存在疑惑，我们在[demos](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos)文件夹中提供了原生[html](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos/base-demo)、[React](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos/with-react-vite)、[Vue2.5](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos/with-vue2.5), [Vue3](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos/vue3-demo), [Uniapp Web](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos/with-uniapp-vue3)框架的接入示例

*注意：[demos](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/demos)中的框架仅提供接入方式的参考，可能不是最新的UIKit版本*

## 二、使用

**1、在页面中提供一个空的div标签用于生成轻应用播放器元素**

```
<div id="ezuikit-player"></div>
```

EZUIKitPlayer 的 `width` / `height` 参数要求及注意事项说明：

- 自适应、动态宽高：需确保初始化之前容器已创建完成，在容器内容为空或 DOM 未完成渲染时，`clientHeight` 极易返回 0 或极小值，导致播放器高度异常。
- 固定宽高（建议）：初始化时传入固定的宽高值。

```
// 正确做法：先算好尺寸，再创建播放器
const formRect = formCardEl.getBoundingClientRect();
const width = window.innerWidth - padding * 2;
const height = window.innerHeight - formRect.height - padding * 2 - gap;

// 先把尺寸写到容器上
wrapper.style.width = `${width}px`;
wrapper.style.height = `${height}px`;

// 再用同样的值初始化播放器
const player = new EZUIKitPlayer({
  id: 'video-container',
  accessToken,
  url,
  width,
  height,
});
```

```
// 错误做法：依赖 flex 布局后读 clientHeight
// wrapper 通过 CSS flex:1 撑高，但 clientHeight 可能为 0
const height = wrapper.clientHeight;
const player = new EZUIKitPlayer({ ..., height });
```

**2、初始化UIKit实例**  
注意：不同的引入方式需要使用不同的初始化方法

```
// UMD 引入方式初始化
const player = new EZUIKit.EZUIKitPlayer({
  id: "ezuikit-player",
  accessToken: "at.xxxxx",
  url: "ezopen://open.ys7.com/设备序列号/通道号.live",
  template: "pcLive",
  width: 600,
  height: 400,
  handleError: (err) => {
    console.error("播放异常:", err);
  }
});

// ESM、CommonJS 引入方式初始化
const player = new EZUIKitPlayer({
  id: "ezuikit-player",
  accessToken: "at.xxxxx",
  url: "ezopen://open.ys7.com/设备序列号/通道号.live",
  template: "pcLive",
  width: 600,
  height: 400,
  handleError: (err) => {
    console.error("播放异常:", err);
  }
});
```

*注意：*

① 初始化实例时传入的id需要与第1步div的id保持一致

② url和accessToken为取流播放的必要参数，获取方式及参数说明请参考：

**url获取方式说明文档地址** <https://open.ys7.com/help/1414>

**accessToken获取方式说明文档地址** <https://open.ys7.com/help/81>

③ 请在实例化时创建一个变量（UIKitDEMO）用于保存UIKit实例，用于后续的API调用

④ 确保id在页面中的唯一性，请勿重复初始化同一个id的UIKit实例，否则可能导致播放失败

⑤ 初始化成功后，默认会自动开始播放视频，请勿额外调用其他播放接口，否则可能导致多次取流或无法播放的问题。若不希望默认自动播放，可在初始化时通过参数配置，详见下方初始化参数说明

#### 3、UiKit API

UIKit实例提供的API请参考：

**API说明文档地址** <https://open.ys7.com/help/1771>

#### 4、初始化参数说明（标准版、Pro版初始化参数一致）

| 字段 | 类型 | 含义 | 是否必填 | 备注 |
| --- | --- | --- | --- | --- |
| id | string | 用于挂载轻应用播放的DOM节点的id | 是 |  |
| url | string | ezopen协议播放地址 | 是 |  |
| accessToken | string | 取流播放token，从开放平台控制台获取 | 是 |  |
| muted | boolean | 初始化播放时是否静音 | 否 | 8.2.0及之后版本支持，默认false，即初始化播放后自动播放声音 |
| width | number | 初始化播放器宽度 | 是 | 8.2.2及之后的版本支持css支持单位 , 比如 "50%", "10em" |
| height | number | 初始化播放器高度 | 是 | 8.2.2及之后的版本支持css支持单位 ，比如 "50%", "10em" |
| talkChannelNo | number | 对讲通道号 | 否 | 默认为0，与设备本身对讲 NVR设备需指定对讲通道为设备的取流通道号 小权限token对讲时，需指定对讲通道为IPC：1，NVR：取流通道 |
| handleError | function | 播放失败回调方法 | 否 | 返回值为错误描述 |
| handleSuccess | function | 播放成功回调方法 | 否 |  |
| handleCapturePicture | function | 截图回调方法 | 否 | 返回值为图片数据 |
| handleFirstFrameDisplay | function | 首帧回调方法 | 否 | 取流成功并出现第一帧画面时触发 |
| dpr | number | 锯齿消除 | 否 | 8.0.5及之后的版本支持，消除监控画面清晰度超过当前终端的显示分辨率时产生的锯齿，默认为1（dpr以牺牲出流速度的方式消除画面锯齿，数值设置的越高，画面锯齿消除的效果越好，出流耗时的增加也会越高） |
| env | object | 请求服务地址 | 否 | 默认值为{domain:'https://open.ys7.com'} |
| autoplay | boolean | 初始化成功后是否立即开始播放 | 否 | 默认值为true，初始化成功后直接开始播放视频 |
| download | boolean | 截图是否下载到本地 | 否 | 默认值为true |
| decoderType | string | 解码模式，v1：兼容性优先模式，v3：性能优先模式 | 否 | 默认值为v3，若当前环境不支持v3会自动切换至v1 |
| 使用v1模式可以在端侧关闭设备移动监测功能 |  |  |  |  |
| quality | string / number | 初始化默认清晰度 | 否 | 8.1.5及之后的版本支持，不传则默认从设备侧查询当前的清晰度并展示 |
| 0: 流畅； 1: 标清; 2: 高清; 3: 超清; 4: 极清; 5: 3K; 6:4K ; "pp"： "性能优先 (Performance Priority)"; "qp": "画质优先(Quality Priority)" |  |  |  |  |
| downloadRecord | boolean | 录制文件是否下载到本地 | 否 | 8.1.6版本后支持，默认值为true |
| stopSaveCallBack | function | 结束录制回调方法 | 否 | 8.1.6版本后支持， stopSave结束录制后触发，返回录制文件数据及文件的blob地址; 8.2.x 开始不再支持， 请使用 监听 `stopSave` 事件 |
| showStreamInfo | boolean | 是否展示码流检测信息 | 否 | 8.1.16版本后支持 |
| isCloudRecord | boolean | 开启云录制 | 否 | 适用 8.1.x 云录制，8.2.x 已移除并默认支持云录制 ， 不再推荐 |
| [videoLevelList](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/blob/master/videoLevelList.md) | Object | 自定义清晰度列表 | 否 | 自定义清晰度列表，默认null, 如果有值 sdk 内部不在进行获取, 为 null 使用接口获取的清晰度列表, videoLevelList.length === 0 不展示清晰度控件 sdk 内部不在进行获取, videoLevelList.length > 0 展示控件 sdk 内部不在进行获取 (v8.1.10版本及以上支持); 8.1.17 开始 当 level 的值小于 0时， 不在向设备发送指令，仅根据 streamTypeIn 切换码流 （请保证 streamTypeIn 对应的码流存在） |
| scaleMode | 0 | 1 | 2 | 设置画面填充模式 |
| spaceId | number | 云录制空间 ID | 否 | 云录制空间 ID (仅云录制生效) @sine 8.2.0 |
| timeLineOptions | Object | 回放时间轴配置 | 否 | timeLineOptions.showCoverFold 是否展示卡片(仅移动端)， 默认true @sine 8.2.1 |
| speedOptions | Object | 自定义倍速列表 | 否 | {list: Array<{label: string, value: 0.5 |
| dblClickFullscreen | boolean | 是否支持双击全屏 | 否 | 默认 true @sine 8.2.0 |

## 三、模式切换

UIKit提供单线程、多线程两种模式，默认情况下启用单线程模式。多线程模式在相同环境下有更好的性能表现，切换至多线程模式需依赖浏览器开启跨域安全隔离

UIKit 提供单线程、软解、硬解三种模式，默认情况下启用单线程模式。其中，软解模式依赖浏览器跨域安全隔离。各模式启用方式如下：

① 单线程模式：初始化UIKit实例时decoderType传入v1，并关闭浏览器跨域安全隔离。

② 软解模式：初始化UIKit实例时decoderType传入v3，并开启浏览器跨域安全隔离。画面出流成功后，浏览器console控制台输出以下提示说明软解模式开启成功。

```
The final decodeEngine is 0 (0 is soft,1 is hard)
```

*注意：软解模式向前兼容标准版的多线程模式*

③ 硬解模式：初始化UIKit实例时decoderType传入v3，并关闭浏览器跨域安全隔离。画面出流成功后，浏览器console控制台输出以下提示说明硬解模式开启成功。

```
The final decodeEngine is 1 (0 is soft,1 is hard)
```

*注意：手机端访问集成了UIKit的H5页面暂不支持开启多线程模式*

您可以通过两种方式切换至多线程模式：

#### 1、配置浏览器（仅支持Chrome浏览器）

该方式需要手动配置访问UIKit播放器页面的浏览器，更换其他PC需重新配置，建议开发者在本地调试时使用

```
右键点击浏览器快捷方式 --> 属性 --> 目标栏添加【（空格）--enable-features=SharedArrayBuffer】 --> 应用 --> 重启浏览器
```

#### 2、配置前端服务

该方式只需在前端页面服务中配置一次即可，所有访问该页面的浏览器会自动开启跨域安全隔离，无需手动配置

① nodejs服务

```
response.setHeader("Cross-Origin-Opener-Policy", "same-origin");
response.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
```

② nginx服务

```
add_header Cross-Origin-Opener-Policy "same-origin"; 
add_header Cross-Origin-Embedder-Policy "require-corp";
```

---

# 说明

##### 1、请勿修改UIKit源码中的逻辑，否则可能引起播放失败或功能失效

##### 2、单个页面内初始化多个UIKit实例时的播放性能表现取决于PC硬件配置

##### 3、集成过程中遇到任何问题欢迎在[github](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm)中提交[issues](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/issues)

##### 4、UIKit可能会收集实例化耗时、浏览器类型等非敏感信息，用于帮助我们不断优化UIKit功能体验，详见萤石SDK隐私政策