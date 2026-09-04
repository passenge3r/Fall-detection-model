# API-设备云组件仓-门禁-基础功能-消息示例与消息类别

> API-设备云组件仓-门禁-基础功能-消息示例与消息类别

> 更新时间: 2026-05-25T16:42:04.000+08:00

> 文档ID: 1131 | 来源树: OPEN_API

---

## 消息示例与消息类别

- 发起呼叫的消息示例

```
{
    "header": {
        "messageTime": 1664518380246,
        "channelNo": 0,
        "messageId": "633688ec94dd3627fb450cfa",
        "type": "ys.open.isapi",
        "deviceId": ""
    },
    "body": {
    "payload": {
	"ipAddress":  "172.6.64.7",	
	/*ro, req, string, 报警设备IPv4地址*/
	"ipv6Address":  "1080:0:0:0:8:800:200C:417A",	
	/*ro, opt, string, 报警设备IPv6地址*/
	"portNo":  80,	
	/*ro, opt, int, 报警设备端口号*/
	"protocol":  "HTTP",	
	/*ro, opt, enum, 传输通信协议类型, subType:string, [HTTP#HTTP,HTTPS#HTTPS,EHome#EHome], desc:传输通信协议HTTP/HTTPS/EHome（萤石透传ISAPI 的时候赋值HTTP；ISUP透传ISAPI 的时候赋值 EHome）protocolType作为历史遗留由平台兼容*/
	"macAddress":  "01:17:24:45:D9:F4",	
	/*ro, opt, string, MAC地址*/
	"channelID":  1,	
	/*ro, opt, int, 触发报警的设备通道号, desc:触发的视频通道号（1、    在SDK透传ISAPI协议的时候，上传的是 私有协议对应的视频通道号；（2、    在萤石透传ISAPI协议的时候，上传的是 萤石协议对应的视频通道号；（3、    在ISUP透传ISAPI协议的时候，上传的是 ISUP协议对应的视频通道号；*/
	"dateTime":  "2004-05-03T17:30:08+08:00",	
	/*ro, req, datetime, 报警触发时间*/
	"activePostCount":  1,	
	/*ro, opt, int, 同一个报警已经上传的次数, desc:事件触发频次脉冲事件 定义：事件持续触发（按照设备的检测频率），例如：移动侦测。瞬时事件 定义：区分目标，一个目标触发一次，例如：人脸识别activePostCount  在脉冲事件 类型触发的时候，用于区分是否是同一触发源触发的事件。例如：移动侦测，按照设备检测频率会一直上传；如果触发源发生了变化，这个时候计数就可以重新开始了。这个可以作为事件触发频次的方式来集成；*/
	"eventType":  "voiceTalkEvent",	
	/*ro, req, string, 事件类型, desc:voiceTalkEvent-对讲交互事件*/
	"eventState":  "active",	
	/*ro, req, enum, 事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
	"eventDescription":  "Voice Talk Interactive Event",	
	/*ro, req, string, 事件描述, desc:voiceTalkEvent-对讲交互事件*/
	"deviceID":  "test0123",	
	/*ro, opt, string, 即PUID, desc:在ehome协议接入透传ISAPI事件信息中必须返回,与/ISAPI/System/Network/Ehome的deviceID一致*/
	"VoiceTalkEvent": {	
	/*ro, opt, object, 通话信令事件*/
		"deviceName":  "test",	
		/*ro, opt, string, 设备名称*/
		"netUser":  "test",	
		/*ro, opt, string, 网络操作的用户名*/
		"deviceNo":  1,	
		/*ro, opt, int, 设备编号*/
		"deviceId":  "test",	
		/*ro, opt, string, 设备编号字符串（如：10000000101）, range:[1,32]*/
		"remoteHostAddr":  "test",	
		/*ro, opt, string, 远程主机地址*/
		"talkType":  0,	
		/*ro, opt, enum, 对讲模式, subType:int, [0#单呼,1#组呼], desc:矿灯摄像机在添加到平台的时候，平台会对设备进行分组，对讲有组呼和单呼模式，设备需要上报平台对应的对讲模式；如果是组呼，平台会将该设备的对讲信息转发给组内的其它设备。如果是单呼，就是设备与平台之间进行语音对讲。*/
		"cmdType":  "request",	
		/*ro, req, enum, 操作类型, subType:string, [request#请求呼叫,cancel#取消本次呼叫,answer#接听本次呼叫,reject#拒绝来电呼叫,bellTimeout#被叫响铃超时,hangUp#结束本次通话,deviceOnCall#设备正在通话中,callFailed#呼叫失败,callTimeout#通话超时,startInterrupt#开始插话,endInterrupt#结束插话,callInfo#呼叫信息传递(仅管理机HEOP用到)], 
		desc:1、callTimeout-通话超时（超时后自动挂断，超时时间通过/ISAPI/VideoIntercom/operationTime中talkTime字段配置）。
		2、startInterrupt-开始插话（探视分机A和探视分机B进行对讲时，护士站主机进行插话操作）。
		3、endInterrupt-结束插话（探视分机A和探视分机B进行对讲时，护士站主机插话结束）*/
		"src": {	
		/*ro, opt, object, 源信息*/
			"periodNumber":  1,	
			/*ro, opt, int, 期号*/
			"buildingNumber":  1,	
			/*ro, opt, int, 楼号*/
			"unitNumber":  1,	
			/*ro, opt, int, 单元号*/
			"floorNumber":  1,	
			/*ro, opt, int, 层号*/
			"roomNumber":  1,	
			/*ro, opt, int, 房间号*/
			"devIndex":  1,	
			/*ro, opt, int, 设备序号*/
			"communityNumber":  "test",	
			/*ro, opt, string, 小区编号*/
			"unitType":  "indoor",	
			/*ro, opt, enum, 类型, subType:string, [indoor#室内机,villa#别墅门口机,confirm#二次确认机,outdoor#门口机,fence#围墙机,doorbell#门铃机,manage#管理机,acs#门禁设备,windowCounterIntercom#柜台窗口IP对讲设备,pagingMicrophone#寻呼话筒]*/
			"personUUID":  "test",	
			/*ro, opt, string, 人员UUID, range:[1,64]*/
			"personType":  "student",	
			/*ro, opt, enum, 人员类型, subType:string, [student#学生,parent#家长], desc:默认家长*/
			"callType":  "voice",	
			/*ro, opt, enum, 通话类型, subType:string, [voice#语音,video#视频]*/
			"model":  "DS-KD9403-A",	
			/*ro, opt, string, 设备型号, range:[1,64]*/
			"deviceName":  "test",	
			/*ro, opt, string, 设备名称, range:[1,32]*/
			"serialNumber":  "test"	
			/*ro, opt, string, 设备序列号*/
		},
		"target": {	
		/*ro, opt, object, 目标信息*/
			"periodNumber":  1,	
			/*ro, opt, int, 期号*/
			"buildingNumber":  1,	
			/*ro, opt, int, 楼号*/
			"unitNumber":  1,	
			/*ro, opt, int, 单元号*/
			"floorNumber":  1,	
			/*ro, opt, int, 层号*/
			"roomNumber":  1,	
			/*ro, opt, int, 房间号*/
			"devIndex":  1,	
			/*ro, opt, int, 设备序号*/
			"communityNumber":  "test",	
			/*ro, opt, string, 小区编号*/
			"unitType":  "indoor",	
			/*ro, opt, enum, 类型, subType:string, [indoor#室内机,villa#别墅门口机,confirm#二次确认机,outdoor#门口机,fence#围墙机,doorbell#门铃机,manage#管理机,acs#门禁设备,interactive#终端,center#中心,ezviz#萤石云,windowCounterIntercom#柜台窗口IP对讲设备,pagingMicrophone#寻呼话筒]*/
			"personUUID":  "test",	
			/*ro, opt, string, 人员UUID, range:[1,64]*/
			"personType":  "student",	
			/*ro, opt, enum, 人员类型, subType:string, [student#学生,parent#家长], desc:默认家长*/
			"callType":  "voice",	
			/*ro, opt, enum, 通话类型, subType:string, [voice#语音,video#视频]*/
			"serialNumber":  "test",	
			/*ro, opt, string, 设备序列号*/
			"assemblyAgreementNum":  "sip"	
			/*ro, opt, enum, 号码组装协议, subType:string, [sip#sip协议,ezviz#萤石协议,ISUP#ISUP协议], desc:对讲设备呼叫时，不同协议类型接入的被叫设备号码组装规则不同。无此节点时默认SIP接入*/
		},
		"serialNo":  1,	
		/*ro, opt, int, 事件流水号*/
		"currentEvent":  true,	
		/*ro, opt, bool, 是否为实时事件*/
		"frontSerialNo":  1,	
		/*ro, opt, int, 上一条事件流水号, desc:（若设备没返回该字段，平台根据serialNo判断是否丢失事件；若设备返回该字段，平台根据该字段和serialNo字段共同判断是否丢失事件）（主要用于解决报警订阅后导致serialNo不连续的情况）*/
		"pictureURL":  "test",	
		/*ro, opt, string, 图片URL*/
		"picturesNumber":  1,	
		/*ro, opt, int, 图片数量, desc:后面所带的图片数目，没图片时，也包括使用URL的方式时，该字段为0或不返回*/
		"messageID":  "test",	
		/*ro, opt, string, 消息id, range:[1,64], desc:用于标识和配置通话信令交互：/ISAPI/VideoIntercom/callSignal?format=json的对应关系*/
		"exceptionInfo":  "test"	
		/*ro, opt, string, 异常信息, range:[1,128]*/
	}
}    }
}
```

- 门禁事件的消息示例

```
{
    "header": {
        "messageTime": 1664525552809,
        "channelNo": 0,
        "messageId": "6336a4f033fee71ff3ed8058",
        "type": "ys.open.isapi",
        "deviceId": "J49882687"
    },
    "body": {
        "payload": {
            "ipAddress": "10.10.10.10",
				/*报警设备IPv4地址*/
            "macAddress": " 1080:0:0:0:8:800:200C:417A ",
				/*报警设备IPv6地址*/
            "channelID":1,
				/*触发报警的设备通道号*/
            "dateTime": "2022-09-30T16:12:00+08:00",
				/*报警触发时间*/
            "activePostCount": 1,
				/*事件触发频次脉冲事件*/
            "eventType": "AccessControllerEvent",
				/*事件类型, desc:AccessControllerEvent-门禁事件上传报警*/
            "eventState": "active",
				/*事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
            "eventDescription": "Access Controller Event",
				/*事件描述, desc:AccessControllerEvent-门禁事件上传报警*/
            "AccessControllerEvent": {
                "deviceName": "Access Controller",
					/*设备名称*/
                "majorEventType": 5,
					/*报警主类型*/
                "subEventType": 75,
					/*报警次类型*/
                "name": "Lin",
					/*人员姓名*/
                "cardReaderKind": 1,
					/*读卡器属于哪一类, subType:int, [1#IC读卡器,2#身份证读卡器,3#二维码读卡器,4#指纹头] */
                "cardReaderNo": 1,
					/*读卡器编号*/
                "verifyNo": 170,
					/*多重卡认证序号*/
                "employeeNoString": "458ac8d98a8948371",
					/*人员ID*/
                "serialNo": 914,
					/*事件流水号, range:[1,100000], desc:从1开始,递增加1,达到设备支持的最大值后循环覆盖*/
                "userType": "normal",
					/*人员类型, subType:string, [normal#普通人（主人）,visitor#来宾（访客）,blackList#黑名单人,administrators#管理员,operator#操作员] */
                "currentVerifyMode": "face",
					/*读卡器当前验证方式*/
                "currentEvent": true,
					/*是否为实时事件*/
                "fronSerialNo": 913,
					/*上一条事件流水号*/
                "attendanceStatus": "checkIn",
					/*考勤状态, subType:string, [checkIn#上班,checkOut#下班,breakOut#开始休息,breakIn#结束休息,overtimeIn#开始加班,overtimeOut#结束加班] */
                "label": "上班",
					/*自定义考勤名称*/
                "statusValue": 0,
					/*状态值*/
                "mask": "no",
					/*是否戴口罩, subType:string, [unknown#未知,yes#戴口罩,no#不戴口罩] */
                "helmet": "unknown",
					/*是否戴安全帽, subType:string, [unknown#未知,yes#戴安全帽,no#不戴安全帽] */
                "purePwdVerifyEnable": true
					/*是否支持纯密码开门*/
            }
        }
    }
}
```