# 流管理（RTMP）：生成推流地址

> 流管理（RTMP）：生成推流地址

> 更新时间: 2026-05-25T16:36:11.000+08:00

> 文档ID: 4360 | 来源树: 音视频

---

# 流管理（RTMP）：生成推流地址

流管理（RTMP），萤石流管理提供基于萤石域名的推流地址生成。通过阅读本文，您可以了解推流地址的生成规则及生成方式。

PS：若开发者遇到跨域等问题，可以联系小助手开放自定义域名配置功能。

# 使用说明

推流地址和播放地址默认已开启token鉴权，生成的推/播流地址需要附带鉴权串参数，才可以推流/播放。

鉴权参数中，是有有效期与token的更新机制。具体参考：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/19)

# 流创建

1、控制台入口
![](https://resource.eziot.com/group2/M00/01/04/CtwQFmhAAueAUPHxABQta95TZqI141.png)
1）控制台列表
![](https://resource.eziot.com/group2/M00/01/04/CtwQF2hAAuuAEUrCAAFceyW1rXE828.png)
2）点击新建流
![](https://resource.eziot.com/group2/M00/01/0D/CtwQF2lBFYyAPulHAAIBO2-8Gvg970.png)
2、生成推流地址

![](https://resource.eziot.com/group2/M00/01/04/CtwQF2hAAvGAPDsJAAFZ95-bsSw801.png)

1）接口获取

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmhABxOAQFC6AAFs3SK7zxM996.png)

2）控制台获取
![](https://resource.eziot.com/group2/M00/01/04/CtwQFmhAAvWASxmCAAFs0YTcFC8042.png)

# 地址规则说明

### 萤石推流地址的组成规则：

萤石推流域名＋AppID＋StreamName＋\*\*{鉴权串}\*\*。

以以下地址为例：

rtmp://cdnopen-push.ys7.com/c1cbc1d4e86d49a0981f54beea95280a/845740945980497920?auth\_key=1811043917-0-0-aea510e83a4a49ef712351a6b4aff60

| 内容 | 说明 | 备注 |
| --- | --- | --- |
| rtmp://cdnopen-push.ys7.com | 推流域名，默认萤石域名 |  |
| c1cbc1d4e86d49a0981f54beea95280 | 萤石账号APPID | 账号中心获取 |
| 845740945980497920 | 流ID |  |
| auth\_key=1811043917-0-0-aea510e83a4a49ef712351a6b4aff60 | 鉴权 | 该地址包含了时间有效期等信息 |

备注：

若开发者获取的有效期超过24小时，请注意保密。若泄露推流地址，可能造成其他用户拿到推流地址进行推流，开发者需自行承担所有费用