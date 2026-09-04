# ezuikit-js 视频巡检-视频巡检组件.md

> 更新时间: 2026-05-25T16:44:32.000+08:00

> 文档ID: 4288 | 来源树: SDK及示例

---

# 视频巡检组件

将设备列表托管给EZUIKit内置的视频巡检组件EZUIKitInspectionUI，通过参数配置及API调用快速实现视频巡检业务。

**! 请确保EZUIKit版本不低于8.1.8 !**

#### 1、生成设备列表

根据业务、账号及设备关联关系，或者直接查询萤石云账号下的绑定/托管设备（[设备列表分页查询](https://open.ys7.com/help/673)），在前端维护一个设备列表deviceList。

设备列表为一个对象数组，巡检组件内部会将每个对象分配给一个EZUIKit播放器实例，因此对象的属性与EZUIKit初始化所需的参数保持一致即可。

```
const deviceList = [
    {
        width: 600,
        height: 400,
        accessToken: '',
        url: 'ezopen://open.ys7.com/XXX/1.rec',
        template: 'pcRec'
    },
    {
        width: 600,
        height: 400,
        accessToken: '',
        url: 'ezopen://open.ys7.com/XXX/1.live',
        template: 'pcLive'
    }
];
```

#### 2、初始化巡检组件

- 在页面中创建一个放置巡检组件的div容器
- 初始化巡检组件，并传入容器DOM节点及设备列表

```
<div id="player"></div>
```

```
const inspection = new EZUIKit.EZUIKitInspectionUI(document.getElementById('player'), { list: deviceList })
```

## 3、定义巡检参数/变量

您可以定义一些变量用于配合EZUIKitInspectionUI实现业务层页面展示状态的管控（供参考，可根据需求调整变量）。

| 参数 | 类型 | 说明 | 建议默认值 |
| --- | --- | --- | --- |
| screenSize | number | 屏幕数量 | 4 |
| pageSize | number | 分页大小 | 4（与screenSize保持一致） |
| pageIndex | number | 页码 | 0 |
| delay | number | 轮询时间间隔ms | 10000 |
| selectScreen | number | 选中的屏幕下标 | 0 |

## 4、功能调用

EZUIKitInspectionUI提供翻页、修改分页大小、批量操作实例、获取实例等API，可通过inspection实例调用触发。

#### 5、销毁实例

退出页面或关闭巡检模块前，调用销毁API，销毁所有EZUIKit播放器实例，释放资源，并按需重置页面DOM。

```
inspection.destroy();
```

#### 6、参数说明

EZUIKitInspectionUI初始化参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| container | HTMLElement | EZUIKitInspectionUI目标挂载节点 |
| options | EZUIKitInspectionUIOptions | EZUIKitInspectionUI初始化配置项 |

EZUIKitInspectionUIOptions巡检组件配置参数

| 参数 | 类型 | 说明 | 默认 |
| --- | --- | --- | --- |
| list | EZUIKitInspectionPlayerOptions[] | 设备列表 | [] |
| id | string | EZUIKitInspectionUI实例id，不传则会默认指定一个 | ezuikit-inspection-player |
| defaultSelect | number | 默认选中的屏幕下标 | 0 |
| selectStyle | string | 选中屏幕样式 | ".screen-select::before { content: '';position: absolute;top: 0;left: 0;right: 0;bottom: 0;border: 2px solid red;box-sizing: border-box;z-index: 9999; pointer-events: none; }" |
| pageSize | number | 分页大小 | 4 |
| pageIndex | number | 页码 | 0 |
| autoPlay | boolean | 初始化完成后是否自动播放 | true |
| autoTurn | boolean | 默认自动开始轮询 | false |
| delay | number | 轮询时间间隔ms | 10000 |
| screenStyle | string | 屏幕样式 | / |
| selectScreen | number | 选中的屏幕下标 | 0 |
| text | string | 未播放区域占位文本 | '请选择播放设备' |
| textStyle | string | 占位文本样式 | / |
| imgUrl | string | 未播放区域占位背景图片 | / |
| onScreenSelect | Function | 选中画面时的回调 | () => {} |
| onPageChange | Function | 页码、分页大小改变时的回调 | () => {} |

EZUIKitInspectionPlayerOptions巡检播放器配置参数

*该配置项继承至EZUIKitPlayerParams*

*其他属性可以参考EZUIKit初始化参数*

| 参数 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| url | string | ezopen协议播放地址 | / |
| accessToken | string | accessToken | / |
| width | number | 播放屏幕宽度 | 600 |
| height | number | 播放屏幕高度 | 400 |
| container | HTMLElement | 自定义挂载播放屏幕的DOM，若不传则SDK会创播放屏幕 | / |

#### 7、API列表

| API名称 | API功能 | 入参[参数类型]：参数说明 | 返回结果 | 说明 |
| --- | --- | --- | --- | --- |
| initPlayer | 初始化指定屏幕播放器 | initIndex[number]：要初始化的元素下标 screenIndex[number]：屏幕下标 options[EZUIKitPlayerParams]: 初始化播放器参数 | player实例 | 传入options时，根据options初始化播放器到指定screenIndex 不传options时，按initIndex初始化list内对应的播放器 |
| lastPage | 上一页 | / | / |  |
| nextPage | 下一页 | / | / |  |
| startTurn | 开始轮询 | / | / |  |
| stopTurn | 停止轮询 | / | / |  |
| setDelay | 设置轮询时间间隔 | delay[number]: 目标时间间隔 | / |  |
| changePageSize | 修改分页大小 | size[number]: 目标页面大小 | / |  |
| pageTo | 跳转至指定页 | target[number]: 目标页面下标 | / |  |
| screenSelect | 选中屏幕 | index[number]: 目标选中屏幕下标 | object: 屏幕参数 | 若目标屏幕正在播放器中，则会一起返回播放器实例 |
| setText | 设置未播放区域占位文本 | text[string]: 目标文本 | / |  |
| setBackground | 设置未播放区域占位背景图片 | url[string]: 目标背景图片地址 | / |  |
| destroy | 销毁实例 | destroyAll[boolean]: 是否保留占位DOM | / |  |
| getScreen | 获取屏幕实例 | index[number]: 目标获取屏幕下标，不传则返回当前选中的屏幕 | object: 屏幕参数 | 若目标屏幕正在播放器中，则会一起返回播放器实例 |
| getScreenList | 获取当页屏幕列表 | / | object[] |  |
| destroyScreen | 销毁指定屏幕 | index[number]: 目标销毁屏幕下标 destroyAll[boolean]: 是否保留占位DOM | / |  |
| getDeviceList | 获取设备列表 | / | list |  |
| setList | 更新设备列表 | list | / |  |
| stopAll | 停止播放所有屏幕 | / | / |  |
| playAll | 开始播放所有屏幕 | / | / |  |
| muteAll | 静音所有屏幕 | / | / |  |
| unmuteAll | 取消静音所有屏幕 | / | / |  |

**代码示例**

*以HTML+JavaScripy为例，其他前端框架请根据特性调整语法逻辑*

```
// 引入EZUIKit库
import EZUIKit from 'ezuikit-js';
```

```
<!-- 创建巡检组件容器DOM节点 -->
<div class="player-list" id="player"></div>
```

```
// 初始化巡检组件实例
const inspect = new EZUIKit.EZUIKitInspectionUI(document.getElementById('player'), {
    pageSize: 4,
    autoPlay: true,
    list: deviceList,
    autoTurn: autoTurn,
    delay: 5000,
    imgUrl: "https://...",
    onScreenSelect: (index, item) => {
        console.log("选中屏幕：", index, item);
    },
    onPageChange: (res) => {
        if (res.code > -1) {
            pageIndex = res.data.pageIndex;
            pageSize = res.data.pageSize;
        } else {
            console.log(res)
        }
    }
})

// 上一页
inspect.lastPage();

// 下一页
inspect.nextPage();

// 开始翻页轮询
inspect.startTurn();

// 停止翻页轮询
inspect.stopTurn();

// 设置轮询间隔为30s
inspect.setDelay(30000);

// 销毁巡检组件
inspect.destroy();
inspect = null;

// 更多API及参数见上方API列表
```