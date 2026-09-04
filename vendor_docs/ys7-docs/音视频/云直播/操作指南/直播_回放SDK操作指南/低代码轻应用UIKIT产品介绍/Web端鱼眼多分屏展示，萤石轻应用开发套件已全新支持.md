#  Web端鱼眼多分屏展示，萤石轻应用开发套件已全新支持

> Web端鱼眼多分屏展示，萤石轻应用开发套件已全新支持

> 更新时间: 2026-05-25T16:36:11.000+08:00

> 文档ID: 4368 | 来源树: 音视频

---

# Web端鱼眼多分屏展示，萤石轻应用UIKit已全新支持

> 本文主要介绍鱼眼摄像头如何在开放平台进行预览取流的使用说明

# 鱼眼介绍

一镜360°全景，鱼眼摄像机为店铺、会议室等场景提供了更广阔的监控视野，受到了众多使用者的青睐。其广泛适用性，成为各种场景下智能化方案的“C位”角色，为进一步满足行业便捷应用需求，萤石开放平台上线了轻应用UIKIT最新版本V7.7.0，增加了支持在浏览器Web端实现鱼眼相机视频多分屏的能力，持续提升使用体验。

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmhBZKeAXhTVAAd6tKOjzoQ869.png)

备注：萤石鱼眼摄像机购买请咨询萤石销售或前往萤石官网购买，海康鱼眼摄像机请咨询海康销售或经销商。

# 1 具体接入方法

### 接入ezopen SDK

初始化参数时，选择鱼眼矫正示例（可参考demo）。

开发指南可参考文档：<https://open.ys7.com/help/4274>

### 配置参数

新版轻应用开发套件产品能力及相关接入参数：

支持在Web/H5页面进行鱼眼画面多分屏，各个参数代表内容如下：

- ① {1, 0} 壁装鱼眼 不矫正
- ② {1, 1} 壁装360°全景
- ③ {1, 2} 壁装4分屏
- ④ {1, 4} 壁装广角
- ⑤ {3, 0} 顶装鱼眼 不矫正
- ⑥ {3, 1} 顶装360°全景
- ⑦ {3, 4} 顶装4分屏
- ⑧ {3, 5} 顶装柱状

### 使用示例可以参考demo：

如果使用原生js，可参考demos => base-demo
如果使用react，可参考demos => react-demo
如果使用vue，可参考demos => vue-demo

# 2 鱼眼相机应用场景介绍

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2hBZUuAYqaGAAQAhtEwM-w223.png)

1、支持海康、萤石多款鱼眼相机，如萤石E4p全景相机等。

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmhBZZiAVZjwAAx8VS4MhPY124.png)

2、小商铺、便利店、餐饮店等场景

全景覆盖，一台设备实现原来多设备监控效果

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2hBZeOAazX-AAdRb7WSZ1g733.png)

3、会议室等

与会人员环形分布，会议模式下可覆盖所有人群

![](https://resource.eziot.com/group1/M00/01/8D/CtwQEmhBZf6AT9HLAAOL9dyHx8I841.png)

4、前台等

面积大、人员流动多，全景记录大范围区域情况

![](https://resource.eziot.com/group1/M00/01/8D/CtwQE2hBZiOAe-iAAAlST7CjVeg645.png)

5、教室等

全景覆盖，保障学生安全，记录教学过程