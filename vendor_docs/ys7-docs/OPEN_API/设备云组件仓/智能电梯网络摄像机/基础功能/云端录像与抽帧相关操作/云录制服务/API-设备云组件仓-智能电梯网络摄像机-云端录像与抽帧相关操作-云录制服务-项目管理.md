# API-设备云组件仓-智能电梯网络摄像机-云端录像与抽帧相关操作-云录制服务-项目管理

> API-设备云组件仓-智能电梯网络摄像机-云端录像与抽帧相关操作-云录制服务-项目管理

> 更新时间: 2026-05-25T16:39:06.000+08:00

> 文档ID: 1602 | 来源树: OPEN_API

---

# 项目管理

> 云录制服务介绍：您可以在云端远程录制、抽取实时的视频以及图片，也可以对本地已经存储的录像进行云端转录以及图片抽帧，将重点信息记录在云端，并且支持对内容进行下载及分析。应用场景：电梯应急救援视频存储在云端。

- 请确保您的账号当前处于企业版状态。云录制服务仅支持企业版用户使用。测试过程您可以申请体验金哦！

---

## 创建云录制项目

- 接口URL

https://open.ys7.com/api/open/cloud/v1/project/{projectId}

- 接口描述

开发者通过创建云录制项目。（后期存储的图片、视频会存储于该项目内，可以设置项目中文件过期时间、下载流量保护等信息。）

- 详细说明

<https://open.ys7.com/help/366#project_created-api1>

## 单条查询云录制项目

- 接口URL

https://open.ys7.com/api/open/cloud/v1/project/{projectId}

- 接口描述

单条查询云录制项目详细内容。（后期存储的图片、视频会存储于该项目内，可以设置项目中文件过期时间、下载流量保护等信息。）

- 详细说明

<https://open.ys7.com/help/366#project_created-api2>

## 分页查询云录制项目

- 接口URL

https://open.ys7.com/api/open/cloud/v1/projects

- 接口描述

分页查询云录制项目。

- 详细说明

<https://open.ys7.com/help/366#project_created-api3>