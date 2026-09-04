# ezuikit-js 视频巡检-自定义视频巡检.md

> 更新时间: 2026-05-25T16:44:32.000+08:00

> 文档ID: 4289 | 来源树: SDK及示例

---

# 自定义视频巡检

本文档演示如何基于EZUIKit自主实现一个像萤石开放平台控制台视频巡检一样的巡检业务，包括设备列表、屏幕实例管理，翻页轮询逻辑，以及页面布局搭建等。

**! 请确保EZUIKit版本不低于8.1.8 !**

#### 1、生成设备列表

根据业务、账号及设备关联关系，或者直接查询萤石云账号下的绑定/托管设备（[设备列表分页查询](https://open.ys7.com/help/673)），在前端维护一个设备列表deviceList。

设备列表为一个对象数组，由于每个对象都代表一个EZUIKit播放器实例，因此对象的属性与EZUIKit初始化所需的参数保持一致即可。

```
const deviceList = [
    {
        key: "XXX-1", // 使用【设备序列号-通道号】作为唯一标识
        width: 600,
        height: 400,
        accessToken: '',
        url: 'ezopen://open.ys7.com/XXX/1.rec',
        template: 'pcRec'
    },
    {
        key: "XXXX-1",
        width: 600,
        height: 400,
        accessToken: '',
        url: 'ezopen://open.ys7.com/XXXX/1.live',
        template: 'pcLive'
    }
];
```

#### 2、定义巡检参数/变量

为了实现巡检业务的播放、翻页、屏幕操作等功能，您需要定义一些变量用于页面状态，屏幕实例的管控（供参考，可根据需求调整变量）。

| 参数 | 类型 | 说明 | 建议默认值 |
| --- | --- | --- | --- |
| screenSize | number | 屏幕数量 | 4 |
| pageSize | number | 分页大小 | 4（与screenSize保持一致） |
| pageIndex | number | 页码 | 0 |
| delay | number | 轮询时间间隔ms | 10000 |
| selectScreen | number | 选中的屏幕下标 | 0 |
| screenList | array | 屏幕列表 | [] |
| audioOnly | boolean | 只播放选中画面声音，或同时播放所有画面声音 |  |

#### 3、定义巡检事件

实现巡检业务的播放、翻页、屏幕操作等功能。

- 上一页
- 下一页
- 跳转至指定页面
- 选中指定屏幕
- 初始化指定屏幕播放器
- 关闭指定屏幕
- 销毁指定屏幕
- 切换分屏数量
- 批量操作
- 全局全屏

**代码示例**

*以React项目为例，其他前端框架请根据特性调整语法逻辑*

```
// 引入EZUIKit库
import EZUIKit from 'ezuikit-js';
```

```
// 创建屏幕DOM节点、播放器容器DOM节点，并设置id
{Array.from({ length: screenSize }).map((_, index) => {
  return (
    <div id={`screen-${index + 1}`} >
      <div className="player" id={`screen-${index + 1}-player`}></div>
    </div>
  )
})}
```

```
// 选择设备在指定屏幕上初始化播放
onDeviceSelect = (selectKey) => {
    const { accessToken } = this.props;
    const { selectScreen, screenList, screenSize, pageIndex, selectDevices } = this.state;
    let tmpScreenList = [...screenList];
    let tmpSelectDevices = [...selectDevices];
    // 判断当前设备是否已经在播放中
    const deviceIndex = tmpSelectDevices.findIndex(i => !!i && i.key === selectKey);
    if (deviceIndex > -1) {
      message.destroy();
      message.warning(`当前设备已选择`);
      return;
    }
    // 判断目标屏幕是否有正在播放的设备
    if (tmpScreenList[selectScreen - 1] && tmpScreenList[selectScreen - 1].player) {
      tmpScreenList[selectScreen - 1].player.destroy();
      tmpSelectDevices = tmpSelectDevices.filter((item, i) => (!!item && item.key !== tmpScreenList[selectScreen - 1].key));
    }
    const option = {
      id: `screen-${selectScreen}-player`,
      url: `ezopen://open.ys7.com/${selectKey.split('-')[0]}/${selectKey.split('-')[1]}.live`,
      accessToken: accessToken,
      width: document.getElementById('screen-' + selectScreen).offsetWidth,
      height: document.getElementById('screen-' + selectScreen).offsetHeight,
      template: 'pcLive',
      mode: 'live'
    }
    const player = new EZUIKit.EZUIKitPlayer({
      ...option,
      handleFirstFrameDisplay: (res) => { } // 播放成功回调
    });
    // 更新屏幕列表参数
    tmpScreenList[selectScreen - 1] = {
      key: e.node.key,
      screenIndex: selectScreen,
      option: option,
      player: player
    }
    // 更新已选设备列表
    tmpSelectDevices.splice(screenSize * (pageIndex - 1) + selectScreen - 1, 0, {
      key: e.node.key,
      screenIndex: selectScreen,
      player: player,
      option: option
    });
    this.setState({
      screenList: tmpScreenList,
      selectDevices: tmpSelectDevices
    })
}

// 翻页
onPageChange = (page) => {
  const { accessToken } = this.props;
  const { selectDevices, screenSize, screenList, selectScreen } = this.state;
  let tmpScreenList = [...screenList];
  let destroyPromisList = [];
  // 销毁原页面的播放器
  if (tmpScreenList.length > 0) {
    tmpScreenList.map((screen, screenIndex) => {
      if (!!screen && !!screen.player) {
        destroyPromisList.push(screen.player.destroy());
      }
    })
    tmpScreenList = [];
  }
  // 销毁完成后初始化目标页的播放器
  Promise.all(destroyPromisList).finally(() => {
    selectDevices.map((item, index) => {
      if (index >= screenSize * (page - 1) && index < screenSize * page) {
        if (!!item && !!item.key) {
          const option = item.option ? item.option : {
            id: `screen-${item.screenIndex}-player`,
            url: `ezopen://open.ys7.com/${item.key.split('-')[0]}/${item.key.split('-')[1]}.live`,
            accessToken: accessToken,
            width: document.getElementById('screen-' + item.screenIndex).offsetWidth,
            height: document.getElementById('screen-' + item.screenIndex).offsetHeight,
            mode: 'live'
          }
          const player = new EZUIKit.EZUIKitPlayer({
            ...option,
            handleFirstFrameDisplay: (res) => { }
          });
          tmpScreenList[item.screenIndex - 1] = {
            key: item.key,
            screenIndex: item.screenIndex,
            option: option,
            player: player
          }
        }
      }
    })
    this.setState({
      screenList: tmpScreenList,
      pageIndex: page
    })
  })
}

// 选中屏幕
onScreenSelect = (selectIndex) => {
  this.setState({
    selectScreen: parseInt(selectIndex),
  }, () => {
    const { audioOnly, selectScreen, screenList, screenSize } = this.state;
    if (audioOnly) {
      // 仅播放选中画面的声音时，先关闭其他画面的声音
      for (let i = 0; i < screenSize; i++) {
        if (screenList[i] && screenList[i].player) {
          if (i !== selectScreen - 1) {
            screenList[i].player.closeSound();
          } else {
            screenList[i].player.openSound();
          }
        }
      }
    }
  })
}
```