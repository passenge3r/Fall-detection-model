# EZUIKit常见问题Q&A.md

> EZUIKit常见问题Q&A

> 更新时间: 2026-05-25T16:44:35.000+08:00

> 文档ID: 4292 | 来源树: SDK及示例

---

# EZUIKit常见问题原因及解决方式

## 一、集成

#### 1、VUE项目集成ezuikit-js后，启动/编译阶段报node\_moduules/loader错误

解决方案：

1、使用最新版本的vite进行项目构建。

2、参考以下配置，修改项目工程的vue.config.js配置文件，忽略对ezuikit.js的二次打包，并重试。

```
// vue.config.js
module.exports = {
  publicPath: "./",
  chainWebpack: (config) => {
    config.module
      .rule("babel")
      .test(/\.js$/)
      .exclude.add(
        (file) =>
          /node_modules/.test(file) && !/\.vue\.js|ezuikit\.js/.test(file)
      )
      .end()
      .use("babel-loader")
      .loader("babel-loader")
      .options({
        presets: ["@babel/preset-env"],
      });
    config.module
      .rule("vue")
      .test(/\.vue$/)
      .use("vue-loader")
      .loader("vue-loader");
  },
};
```

或：vue2.5版本之前的框架，将vue-cli-service升级至最新版本，或使用vite进行项目构建。

#### 2、react项目集成后，编译/启动失败，webpack报错

解决方案：在webpack.config.js中，配置忽略对ezuikit.js的二次打包。

```
// 执行命令，暴露webpack配置文件
react-scripts eject

// webpack.config.js
module.exports = {
    //... 
    externals: {
        'ezuikit': 'ezuikit'
    }
}
```

或：访问我们的[github](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/blob/master/ezuikit.js%EF%BC%89%EF%BC%8C%E5%B0%86ezuikit.js%E6%96%87%E4%BB%B6%E4%BF%9D%E5%AD%98%E8%87%B3%E7%9B%AE%E6%A0%87%E9%9B%86%E6%88%90%E9%A1%B5%E9%9D%A2%E7%9A%84%E5%90%8C%E7%BA%A7%E7%9B%AE%E5%BD%95%EF%BC%8C%E5%B9%B6%E9%80%9A%E8%BF%87import%E5%AF%BC%E5%85%A5%E3%80%82)，将ezuikit.js文件保存至目标集成页面的同级目录，并通过import导入。

```
import EZUIKit from "./ezuikit.js";
```

## 二、初始化

#### 1、提示初始化成功，但是没有播放，控制台报Decoder.js文件加载失败，或CORS资源跨域错误

解决方案：访问我们的[github](https://github.com/Ezviz-OpenBiz/EZUIKit-JavaScript-npm/tree/master/ezuikit_static)，将ezuikit\_static文件夹保存至项目的public路径下，确保项目启动后，可以通过url访问到项目工程中的Decoder.js文件，并在ezuikit初始化时添加以下配置项（具体路径根据项目public文件路径调整）。

```
staticPath: "/public/ezuikit_static"
```

#### 2、提示初始化成功，但是没有播放，且控制台没有报错

解决方案：使用[Ezuikit排障工具](https://openstatic.ys7.com/ezuikit_troubleshoots/index.html)，右上角选择与自己集成的SDK一致的版本，并填写播放地址、token等参数后初始化播放。导出日志，并提供给我们的技术支持

### 3、初始化时，提示找不到parentNode/DOM节点

解决方案：检查执行初始化时，ezuikit的目标挂载节点是否已经创建。部分历史版本存在dom节点处理缺陷，升级ezuikit版本之后重试。

## 三、播放

#### 1、播放器展示红色的信息，初始化失败

解决方案：打开浏览器控制台，获取errorCode，参考[错误码列表](https://open.ys7.com/help/377)，确定播放失败原因。

#### 2、按钮UI已经处于播放状态，但是画面黑屏

解决方案：检查设备是否处于加密状态，在初始化阶段的url中拼接[设备验证码](https://open.ys7.com/help/1751) 。打开浏览器控制台-> Network -> WS标签，重新初始化，点击websocket取流通道，观察设备是否正常推流，若推流卡顿或者没有推流，建议重启设备或检查设备网络后重试。

#### 3、切换至其他设备进行播放，或切换预览/回放模式

解决方案：使用ezuikit提供的changePlayUrl接口进行设备/播放模式的切换，无需重新初始化ezuikit实例，避免额外的资源开销（参考：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/1771?h=changePlayUrl)）。

#### 4、回放模式下拖动时间轴至目标时间，播放失败

解决方案：检查初始化时的token类型，ra token为单次有效token，拖动时间轴后，用该token重新发起取流会直接失败，建议使用seek模式，或使用其他类型的token。

#### 5、seek回放无效

seek功能可以在回放过程中，不断开当前取流链路的前提下，进行回放时间的跳转。

解决方案：联系设备销售或技术支持，确认当前设备是否支持seek，且报备了support\_seek\_playback能力集。初始化时配置【useSeek: true】。

#### 6、清晰度较高时，画面出现锯齿状

由画面分辨率超过客户端的渲染分辨率，canvas渲染时部分像素被丢失导致。

解决方案：升级ezuikit至8.0.5及以上版本，并在初始化时配置【dpr: 2】（dpr用于消除画面锯齿，可以是任何大于等于1的数值，dpr越大，对性能消耗就越大，建议根据实际应用场景，调整dpr的值，以平衡画面质量与性能消耗）。

## 四、销毁

#### 1、删除播放器节点后，取流没有断开

解决方案：先调用ezuikit提供的stop接口，该接口返回一个Promise，在then中销毁播放器DOM节点即可。

#### 2、destroy接口调用失败/无效

解决方案：该接口不存在时（老版本），请调用stop接口停止取流后，自行销毁DOM结构即可。

#### 3、 初始化新的实例后，旧实例销毁

解决方案：如果是为了切换播放设备，使用changePlayUrl接口切换即可，无需销毁再重新创建。参考问题1，旧节点删除和新实例的初始化都需要在旧实例stop的回调中执行。

## 五、对讲

#### 1、发起对讲失败，控制台报错talk err getUserMedia not available

uikit未获取到浏览器的WebRTC全局对象，可能是浏览器不支持，或者当前页面没有获取到麦克风权限，或者当前是用ip地址访问，导致触发浏览器安全限制，不允许调用webrtc。

解决方案：[检查当前浏览器是否支持WebRTC](https://caniuse.com/?search=WebRTC)，并已经授权使用麦克风。若项目通过ip地址访问，需要使用https协议。

#### 2、对讲发起成功，浏览器激活麦克风，但是对讲双方都听不到声音

解决方案：确认对讲通道，IPC为0，NVR需要根据设备所在的通道，在初始化ezuikit时配置对应的对讲通道（参考：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/1772?h=talkChannelNo))。

#### 3、对讲发起成功，但是有其中一方听不到对方声音。

解决方案：若设备听不到客户端的声音，检查客户端麦克风是否正常。若客户端听不到设备的声音，联系设备销售或技术支持确认设备是否支持全双工对讲。部分ezuikit历史版本存在对讲功能缺陷，升级ezuikit版本后重试。

## 六、问题反馈

请先查阅[萤石开放平台SDK错误码文档](https://open.ys7.com/help/37) 和 以上常见问题能否解决您的问题。

如果未解决，请先在排障工具中尝试复现，确保工具内也存在同样的问题。

- 如不能复现，请升级至对应的SDK版本再尝试；
- 如果能复现，请[创建工单](https://open.ys7.com/console/work.html)，并提供以下信息（或直接导出排障工具的日志提供给我们）：

```
1.SDK版本
2.使用的浏览器类型、版本
3.问题复现条件、场景及复现概率
4.问题详细描述（需要告知哪个功能模块出现的问题，具体怎么操作，出现异常的现象是什么；最好提供问题复现录屏）
5.浏览器控制台日志，在浏览器控制台中右键 -> save as 保存浏览器日志
6.demo（不是您的项目）启动至问题复现的完整日志
```