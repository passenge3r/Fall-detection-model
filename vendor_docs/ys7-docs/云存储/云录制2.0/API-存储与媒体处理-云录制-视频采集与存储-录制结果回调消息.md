# API-存储与媒体处理-云录制-视频采集与存储-录制结果回调消息

> API-存储与媒体处理-云录制-视频采集与存储-录制结果回调消息

> 更新时间: 2026-05-25T16:37:10.000+08:00

> 文档ID: 1384 | 来源树: 云存储

---

# 录制结果回调消息

前提条件: 在消息推送控制台开通消息推送服务，并勾选云录制消息，云录制消息类型：ys.open.cloud

[消息推送服务开通操作手册](https://open.ys7.com/help/566)

# 云录制2.0（加密录像录制）

## 计划消息

- ### **header说明**

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| **header** | **Object** | **设备信息** |
| type | String | 消息类型：ys.open.cloud表示云录制消息 |
| deviceId | String | 设备序列号 |
| channelNo | Integer | 设备通道号 |
| messageId | String | 消息唯一ID |
| messageTime | Long | 消息发送时间 |

- ### **body说明**

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| **body** | **Object** | **设备上传的消息** |
| messageType | String | 消息类型 ，计划信息（plan\_info\_result） |
| planId | Long | 计划id |
| planName | String | 计划名称 |
| planType | Integer | 计划类型 1-一次性计划,2-批量计划 |
| planStatus | Integer | 会发送消息的计划状态  1.创建中（设备任务创建） 2.创建失败（任务创建失败，错误信息） 3.未开始 （计划正式创建，未到达计划开始时间） 4.进行中 （计划已经执行） 5.已终止（计划停止） 6.终止中 （计划正在终止） 7.终止失败 （计划终止过程中发生异常，此场景一般不出现，除非服务异常） 8.删除中 （计划删除中） 9.删除失败 （计划删除过程中发生异常，此场景一般不出现，除非服务异常） 10.异常(录制过程中发生异常) 11.已完成 12.删除成功 |
| planStartTime | Date | 计划开始时间 |
| planEndTime | Date | 计划结束时间 |

## 计划中产生的任务消息

- ### **header说明**

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| **header** | **Object** | **设备信息** |
| type | String | 消息类型：ys.open.cloud表示云录制消息 |
| deviceId | String | 设备序列号 |
| channelNo | Integer | 设备通道号 |
| messageId | String | 消息唯一ID |
| messageTime | Long | 消息发送时间 |

- ### **body说明**

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| **body** | **Object** | **设备上传的消息** |
| messageType | String | 消息类型 ，计划中的任务消息（task\_remind\_pull\_storage） |
| planId | Long | 计划id |
| planType | Integer | 计划类型 1-一次性计划,2-批量计划 |
| taskType | Integer | 任务类型，1-预览，2-回放 |
| devId | String | 设备序列号 |
| channelNo | Integer | 通道号 |
| assignmentType | Integer | 任务类型，9：云录制 |
| createTime | Long | 任务创建时间 |
| updateTime | Long | 任务更新时间 |
| videosBeginTime | Long | 视频录制开始时间 |
| videosEndTime | Long | 视频录制结束时间 |
| assignmentStatus | Integer | 1. 任务开始 4. 任务结束 5. 任务取消 6. 任务异常 |
| planStartTime | Long | 计划开始时间 |
| planEndTime | Long | 计划结束时间 |
| errorCode | Integer | 错误码，参考文档：[云录制2.0错误码](https://open.ys7.com/help/4488) |

# 云点播

## 转封装任务消息

- ### **header说明**

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| type | String | 消息类型：ys.open.cloud表示云录制消息 |
| deviceId | String | 设备序列号 |
| channelNo | Integer | 设备通道号 |
| messageId | String | 消息唯一ID |
| messageTime | Long | 消息发送时间 |

- ### **body说明**

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| **body** | **Object** | **设备上传的消息** |
| messageType | String | 消息类型 ，云点播转封装任务（video\_transcode） |
| userId | String | 用户id |
| taskId | String | 任务id |
| errorCode | String | 错误码 |
| errrorMsg | String | 错误信息 |
| taskStatus | String | 任务状态 COMPLETE(0, "已完成"),PROCESSING(2, "进行中"), EXCEPTION\_FAILED(4, "异常结束"), NOT\_START(7,"未开始"); |

## 转封装子任务消息

- ### **header说明**

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| type | String | 消息类型：ys.open.cloud表示云录制消息 |
| deviceId | String | 设备序列号 |
| channelNo | Integer | 设备通道号 |
| messageId | String | 消息唯一ID |
| messageTime | Long | 消息发送时间 |

- ### **body说明**

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| **body** | **Object** | **设备上传的消息** |
| messageType | String | 消息类型 ，云点播转封装子任务（video\_transcode\_sub） |
| userId | String | 用户id |
| taskId | String | 任务id |
| errorCode | String | 错误码 |
| errrorMsg | String | 错误信息 |
| startTime | Long | 时间戳(毫秒)，转封装开始时间 |
| endTime | Long | 时间戳(毫秒)，转封装结束时间 |
| taskStatus | String | 任务状态 COMPLETE(0, "已完成"),PROCESSING(2, "进行中"), EXCEPTION\_FAILED(4, "异常结束"), NOT\_START(7,"未开始"); |

## 转封装子任务文件消息

- ### **header说明**

| **字段名** | **类型** | **描述** |
| --- | --- | --- |
| type | String | 消息类型：ys.open.cloud表示云录制消息 |
| deviceId | String | 设备序列号 |
| channelNo | Integer | 设备通道号 |
| messageId | String | 消息唯一ID |
| messageTime | Long | 消息发送时间 |

- ### **body说明**

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| **body** | **Object** | **设备上传的消息** |
| messageType | String | 消息类型 ，云点播转封装子任务文件消息（video\_transcode\_sub\_file） |
| taskId | String | 任务id |
| startTime | Long | 时间戳(毫秒)，转封装开始时间 |
| endTime | Long | 时间戳(毫秒)，转封装结束时间 |
| taskStatus | String | 任务状态 COMPLETE(0, "已完成"),PROCESSING(2, "进行中"), EXCEPTION\_FAILED(4, "异常结束"), NOT\_START(7,"未开始"); |
| tagId | String | 标签id， 如果是转封装任务，则为任务id； 如果是云录制2.0后处理模板，则为计划id； |
| fileNodeIds | String类型的List集合 | 转封装的云点播文件节点集合，示例如 ["MAcdrIrj"]， 可作为云点播其他接口的入参，  如调用 [获取文件播放地址（GET）](https://open.ys7.com/help/4402) 接口时，将其填入 fileNodeIds 参数;   调用其他云点播接口（如文件信息查询、删除等）时，将其填入 fileNodeId 或 folderNodes 参数。 |