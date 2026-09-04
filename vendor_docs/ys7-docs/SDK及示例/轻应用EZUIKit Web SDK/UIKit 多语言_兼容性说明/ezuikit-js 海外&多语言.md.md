# ezuikit-js 海外&多语言.md

> 更新时间: 2026-05-25T16:44:33.000+08:00

> 文档ID: 4277 | 来源树: SDK及示例

---

# EZUIKit 海外&多语言

**请确保EZUIKit版本不低于8.0.8**

EZUIKit已支持对接入海外区域萤石云平台的设备取流播放，并支持初始化及使用过程中切换播放器的提示、文案等信息的语言。

当前EZUIKit内置了中文、英文两种语言，您也可以通过EZUIKit的多语言模块自定义其他国家的语言或提示语文案内容。

## 海外设备播放

#### 1、确定设备所在区域

根据设备绑定账号的所属区域确定设备所在的区域env。

| 区域 | env |
| --- | --- |
| 中国 | <https://open.ys7.com> |
| 欧洲 | <https://ieuopen.ezvizlife.com> |
| 北美 | <https://iusopen.ezvizlife.com> |
| 南美 | <https://isaopen.ezvizlife.com> |
| 新加坡 | <https://isgpopen.ezvizlife.com> |
| 印度 | <https://iindiaopen.ezvizlife.com> |
| 俄罗斯 | <https://irusopen.ezvizlife.com> |

#### 2、初始化EZUIKit时配置

*以欧洲区域设备取流播放为例*

```
const player = new EZUIKit.EZUIKitPlayer({
  id: "player",
  template: "pcLive",
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken: "at.xxx",
  host: "open.ezviz.com", // host为url（即ezopen协议地址）的域名，海外固定为【open.ezviz.com】，国内固定为【open.ys7.com】
  url: `ezopen://open.ezviz.com/${设备序列号}/${通道号}.live`,
  env: {
    domain: "https://ieuopen.ezvizlife.com",
  }
});
```

## 多语言

EZUIKit内置中文、英文两种语言，可以在初始化阶段通过language参数配置，或在播放过程中通过实例切换语言。

```
// 方法一：初始化阶段通过language参数配置
const player = new EZUIKit.EZUIKitPlayer({
  id: "player",
  template: "pcLive",
  language: "en", // zh：中文，en：英文
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken: "at.xxx",
  host: "open.ezviz.com",
  url: `ezopen://open.ezviz.com/${设备序列号}/${通道号}.live`,
  env: {
    domain: "https://ieuopen.ezvizlife.com",
  }
});

// 方法二：播放过程中通过实例切换语言
player.i18n.switchTranslation('en');
```

## 自定义语言/提示文案

若您有使用其他国家语言的需求，或是想修改某些错误码、UI模块的提示文本内容，可通过EZUIKit的语言文案管理模块进行自定义。

当前仅支持初始化成功后通过实例API切换文案。

1、定义提示文案

```
const lang_zh ={
  "396701":"没有新的回放片段了",
  "399048":"请联系客服",
  'LOADING': 'loading...',
  'INIT SUCCESS':'初始化播放器成功'
}

const lang_en ={
  "396701": "Playback ends",
  "399048": "please contact customer service",
  'LOADING': 'loading...',
  'INIT SUCCESS': 'Initialize the player successfully'
}


const diy_zh = {
  'LOADING': '加载中',
  'INIT SUCCESS':'初始化完成'
}
```

2、初始化SDK成功回调里使用自定义文案覆盖默认文案

```
//初始化轻应用
const player =new EZUIKit.EZUIKitPlayer({
  id: "player",
  template: "pcLive",
  talkChannelNo: 1,
  width: 600,
  height: 400,
  accessToken: "at.xxx",
  handleSuccess: () => {
    // 导入想要覆盖的中/英文文案内容或自定义的语言
    player.is8n.appendTranslations({
    zh: lang_zh,
    en: lang_en,
    diy_zh: diy_zh
    })

    // 切换自定义语言
    player.i18n.switchTranslation('diy_zh');
  }
})
```