# 小程序与S10设备VOIP视频通话服务端接入文档

> 小程序与S10设备VOIP视频通话服务端接入文档

> 更新时间: 2026-05-25T16:36:48.000+08:00

> 文档ID: 4987 | 来源树: 音视频

---

# 小程序与S10设备VOIP视频通话服务端接入文档

> 本文档为 《s10设备呼叫微信小程序》 及 《微信小程序呼叫s10设备》 服务端接入demo

## ⼀. 设备呼叫小程序开发者服务端接入demo

设备呼叫小程序整体流程如下：
![](https://resource.eziot.com/group2/M00/01/0E/CtwQFmlCR1mAdU68AAFX-qjGICg140.png)

1.开发者收到萤石云开放平台**设备请求呼叫**webhook后，主动调用微信接口触发微信呼叫

- webhook消息类型：ys.open.rtc.call，参考：[实时音视频webhook消息](https://open.ys7.com/help/4913)

```
代码示例如下：
//设备呼叫微信小程序请求模板 CALL_REQUEST_TEMP 
String CALL_REQUEST_TEMP = "{\"model_id\":\"%s\",\"sn\":\"%s\",\"openid\":\"%s\",\"room_type\":\"video\",\"listener_name\":\"%s\",\"version_type\":%d,\"query\":\"ratio=%s&callId=%s&encodeVideoFixedLength=320&encodeVideoRotation=1&encodeVideoRatio=75\",\"caller_camera_status\":0,\"listener_camera_status\":%d,\"payload\":\"%s\"}";
//解析webhook消息体内容，拿到呼叫action
String action = callBody.getAction();
if (action.equals(CallActionEnum.REQUEST.getCmdType())) {
    //设备上行链路---设备主动呼叫小程序
    //developerRelation：开发者维护的deviceSerial，account，openId，applicationId关联信息表。
    DeveloperRelation queryAccount = developerRelationDao.query(null, null, callBody.getAccount(), deviceSerial);
    if (Objects.nonNull(queryAccount) && queryAccount.getPlatform().equals("小程序")) {
        String openId = queryAccount.getOpenId();
        String callId = callBody.getCallId();
        String strRoomId = callBody.getStrRoomId();
        String appId = callBody.getAppId();
        //获取ertc token
        Map<String, String> ertcToken = getErtcToken(appId, strRoomId, openId, deviceSerial, accessToken);
        String deviceToken = ertcToken.get("deviceToken");
        String wxToken = ertcToken.get("wxToken");
        //developerRoomRecord：开发者维护的callId,ertcToken,serverToken,wxRoomId,wxAppId,sessionKey,strRoomId等房间信息表。
        developerRoomRecordDao.insert(callId, deviceToken, wxToken, deviceSerial, null, openId, wxAppId, null, null, strRoomId);
        // 携带自定义payload，呼叫小程序
        try {
            String payload = callId + "@" + DEVICE_TO_WX_TYPE;
            log.info("生成的payload:{}", payload);
            // 微信视频编码定制参数可参考 https://developers.weixin.qq.com/miniprogram/dev/framework/device/voip/voip-video.html 2.4部分
            String requestJson = String.format(CALL_REQUEST_TEMP, MODEL_ID, deviceSerial, openId, "测试设备", wxType, "16:9", callId,
                       encodeVideoFixedLength, encodeVideoRotation, encodeVideoRatio, 0, payload);
            String token = getToken();
            // 呼叫微信接口：https://api.weixin.qq.com/wxa/business/iot/voip/call
            OkHttpCaller.HttpResponseEntity<WechatSchema> response = OkHttpCaller.postJsonParams(String.format(callUrl, token),
                    requestJson, null, WechatSchema.class);
            if (response.getData().isUnBound()) {
                log.info("用户微信未绑定，触发修改绑定状态{}-{}", openId, deviceSerial);
                throw exception;
            }
            if (response.isSuccess() && response.getData().isSuccess()) {
                log.info("触发微信呼叫成功：{}-{}", openId, deviceSerial);
            } else {
                log.error("触发微信呼叫失败：{}-{}-{}", openId, deviceSerial, response);
                throw exception;
            }
        } catch (Exception e) {
            log.error("触发微信呼叫出错：{}-{}", openId, deviceSerial, e);
            throw exception;
        }
    }
}
//最后响应webhook回调成功
```

  
  
  

2.开发者触发微信呼叫后，在微信回调地址中调用萤石云开放平台微信voip操作接口

- [微信公众平台](https://mp.weixin.qq.com/)(小程序配置)
- [微信消息推送文档](https://developers.weixin.qq.com/miniprogram/dev/framework/server-ability/message-push.html)(参考消息加解密模式为“安全模式”的方法，下载里面的代码示例)

```
代码示例如下：
//解密微信回调密文...，拿到设备触发微信呼叫时的自定义payload
String payload = callbackBody.getPayload();
String[] split = payload.split("@");
String callId = split[0];
String callType = split[1];
//获取accessToken
String accessToken = getAccessToken();
Map<String, String> headers = new HashMap<>();
headers.put("accessToken", accessToken);

DeveloperRoomRecord developerRoomRecord = developerRoomRecordDao.queryByCallId(callId);
//设备呼叫小程序微信回调处理
if (callType.equals(DEVICE_TO_WX_TYPE)) {
    if (Objects.nonNull(developerRoomRecord)) {
        developerRoomRecordDao.updateWxInformation(callId, callbackBody.getRoomId(), wxAppId, callbackBody.getSessionKey(), callbackBody.getServerToken());
        String saveOpenId = developerRoomRecord.getOpenId();
        String deviceSerial = developerRoomRecord.getDeviceSerial();
        DeveloperRelation queryAccount = developerRelationDao.query(saveOpenId, null, null, deviceSerial);
        Map<String, String> joinParam = getVoipJoinParam(developerRoomRecord, queryAccount, callbackBody, "0");
        // 调用开放平台微信voip操作接口 https://open.ys7.com/api/service/rtc/voip/trigger
        OkHttpCaller.HttpResponseEntity<MetaBody> voipJoinResp = OkHttpCaller.postForm(domain + VOIP_JOIN_URL, joinParam, headers, MetaBody.class);
        if (voipJoinResp.isSuccess() && Objects.nonNull(voipJoinResp.getData()) && voipJoinResp.getData().isSuccess()) {
            log.info("【微信房间信息转发VOIP成功】，CallId:{}，Action:{}，deviceSerial:{}", callId, "设备呼叫小程序，微信回调", deviceSerial);
        }
    }
}
//最后响应微信回调成功
```

  
  
  

3.微信小程序接听/拒接/挂断后，萤石云开放平台会将消息推送至开发者服务，开发者调用接听/拒接/挂断接口同步至萤石云开放平台

- webhook消息类型：ys.open.rtc，参考：[通话状态消息通知](https://open.ys7.com/help/4299)

```
代码示例如下：
//解析webhook消息体内容，拿到result
VoipOperationResult bodyResult = callBody.getResult();
String statusRequest = null;
if (VoipStatus.TALKING.getCode() == bodyResult.getStatus() || VoipStatus.REJECTED.getCode() == bodyResult.getStatus() ||
        VoipStatus.HANGUP_BY_CALLEE.getCode() == bodyResult.getStatus() || VoipStatus.BUSY.getCode() == bodyResult.getStatus()) {
    if (VoipStatus.TALKING.getCode() == bodyResult.getStatus()) {
        statusRequest = "answer";
    }
    if (VoipStatus.REJECTED.getCode() == bodyResult.getStatus()) {
        statusRequest = "reject";
    }
    if (VoipStatus.HANGUP_BY_CALLEE.getCode() == bodyResult.getStatus()) {
        statusRequest = "hangUp";
    }
    if (VoipStatus.BUSY.getCode() == bodyResult.getStatus()) {
        statusRequest = "busy";
    }
    DeveloperRoomRecord developerRoomRecord = developerRoomRecordDao.queryByCallId(callBody.getRoomId());
    //VOIP通话状态回调
    if (Objects.nonNull(developerRoomRecord)) {
        String saveOpenId = developerRoomRecord.getOpenId();
        String deviceId = developerRoomRecord.getDeviceSerial();
        String strRoomId = developerRoomRecord.getStrRoomId();
        String dtkToken = developerRoomRecord.getDtkToken();
        DeveloperRelation queryAccount = developerRelationDao.query(saveOpenId, null, null, deviceId);
        String appId = queryAccount.getApplicationId();
        String account = queryAccount.getAccount();
        //状态同步至设备
        String json = null;
        Map<String, String> headers = new HashMap<>();
        String accessToken = getAccessToken();
        headers.put("accessToken", accessToken);
        headers.put("deviceSerial", deviceId);
        OkHttpCaller.HttpResponseEntity<MetaBody> AccessTokenResult = OkHttpCaller.postJsonParams(domain + String.format(CALL_ACTION, statusRequest, strRoomId, appId, account, dtkToken, callBody.getRoomId()),
                json, headers, MetaBody.class);
        if (AccessTokenResult.isSuccess() && Objects.nonNull(AccessTokenResult.getBody())) {
            String responseBody = AccessTokenResult.getBody();
            JSONObject jsonObject = JSON.parseObject(responseBody);
            JSONObject meta = jsonObject.getJSONObject("meta");
            if (meta != null) {
                String code = meta.getString("code");
                if ("200".equals(code)) {
                    log.info("【VOIP回调触发小程序响应状态同步至设备成功】，CallId:{}，Action:{}，deviceSerial:{}", callBody.getRoomId(), bodyResult.getMsg(), deviceId);
                }
            }
        }
    }
}

//最后响应webhook回调成功
```

  
  
  

4. 设备取消呼叫小程序，webhook中调用萤石云开放平台微信voip操作接口

- webhook消息类型：ys.open.rtc.call，参考：[实时音视频webhook消息](https://open.ys7.com/help/4913)
- [开放平台微信voip操作接口](https://open.ys7.com/help/4298)

## 二. 小程序呼叫设备服务端接入demo

小程序呼叫设备整体流程如下：
![](https://resource.eziot.com/group2/M00/01/0E/CtwQFmlCUcOAZjTiAAEnLPbpaRw175.png)

1.开发者可保存萤石云开放平台通话Token并生成callId

- 小程序客户端可根据开发者服务端生成的callId，标记唯一通话，来执行呼叫（步骤2），取消呼叫（步骤4）

```
//代码示例如下
Map<String, String> openIdParams = new HashMap<>();
openIdParams.put("grant_type", "authorization_code");
openIdParams.put("appid", wxAppId);
openIdParams.put("secret", appSecret);
openIdParams.put("js_code", jsCode);

String openid = null;

try {
    //获取openId微信接口：https://api.weixin.qq.com/sns/jscode2session
    OkHttpCaller.HttpResponseEntity<OpenIdResult> openResponse = OkHttpCaller.get(OPENID_URL, openIdParams, null, OpenIdResult.class);
    if (openResponse.isSuccess()) {
        OpenIdResult openResponseData = openResponse.getData();
        log.info("请求微信获取OpenId接口返回响应：{}", JSON.toJSONString(openResponseData));
        openid = openResponseData.getOpenid();
        if (!StringUtils.hasText(openid)) {
            throw exception;
        }
    }
} catch (Exception e) {
    log.error("调用微信获取OpenId失败", e);
    ItemManager.getInstance().accumulate("LOCK_HOUSEKEEPER_WECHAT_OPENID_FAIL");
    throw exception;
}
//developerRelation：开发者维护的deviceSerial，account，openId，applicationId关联信息。
DeveloperRelation developerRelation = developerRelationDao.query(openid, null, null, deviceSerial);
//生成唯一callId
String callId = UUID.randomUUID().toString().replace("-", "");
String strRoomId = callId;
String appId = developerRelation.getApplicationId();

Map<String, String> ertcToken = null;
//调用开放平台生成通话token接口  https://open.ys7.com/api/service/media/token/rtc
ertcToken = getErtcToken(appId, strRoomId, openid, deviceSerial, accessToken);
//deviceToken中customId为设备序列号
String deviceToken = ertcToken.get("deviceToken");
//wxToken中customId为openId
String wxToken = ertcToken.get("wxToken");
//保存ertc房间信息  
//developerRoomRecord：开发者维护的callId,ertcToken,serverToken,wxRoomId,wxAppId,sessionKey,strRoomId等房间信息。
developerRoomRecordDao.insert(callId, deviceToken, wxToken, deviceSerial, null, openid, wxAppId, null, null, strRoomId);
//返回callId给小程序端
return callId;
```

  
  
  

2.开发者收到**小程序呼叫设备**的微信回调消息后，主动调用萤石云开放平台呼叫设备接口

- [微信公众平台](https://mp.weixin.qq.com/)(小程序配置)
- [微信消息推送文档](https://developers.weixin.qq.com/miniprogram/dev/framework/server-ability/message-push.html)(参考消息加解密模式为“安全模式”的方法，下载里面的代码示例)

```
代码示例如下：
//解密微信回调密文...，拿到微信呼叫设备时的自定义payload
String payload = callbackBody.getPayload();
String[] split = payload.split("@");
String callId = split[0];
String callType = split[1];
if (callType.equals(WX_TO_DEVICE_TYPE)) {
    //小程序呼叫设备微信回调
    if (Objects.nonNull(developerRoomRecord)) {
        developerRoomRecordDao.updateWxInformation(callId, callbackBody.getRoomId(), wxAppId, callbackBody.getSessionKey(), callbackBody.getServerToken());
        String saveOpenId = developerRoomRecord.getOpenId();
        String deviceSerial = developerRoomRecord.getDeviceSerial();
        String strRoomId = developerRoomRecord.getStrRoomId();
        String dtkToken = developerRoomRecord.getDtkToken();
        DeveloperRelation queryAccount = developerRelationDao.query(saveOpenId, null, null, deviceSerial);
        String appId = queryAccount.getApplicationId();
        String account = queryAccount.getAccount();
        //呼叫设备  
        String json = null;
        headers.put("deviceSerial", deviceSerial);
       //调用开放平台呼叫设备接口：https://open.ys7.com/api/service/rtc/call/request
        OkHttpCaller.HttpResponseEntity<MetaBody> AccessTokenResult = OkHttpCaller.postJsonParams(domain + String.format(CALL_ACTION, "request", strRoomId, appId, account, dtkToken, callId),
                json, headers, MetaBody.class);
        if (AccessTokenResult.isSuccess() && Objects.nonNull(AccessTokenResult.getBody())) {
            String responseBody = AccessTokenResult.getBody();
            JSONObject jsonObject = JSON.parseObject(responseBody);
            JSONObject meta = jsonObject.getJSONObject("meta");
            if (meta != null) {
                String code = meta.getString("code");
                if ("200".equals(code)) {
                    log.info("【微信回调触发呼叫设备成功】，CallId:{}，Action:{}，deviceSerial:{}", callId, "小程序呼叫设备，微信回调", deviceSerial);
                }
            }
        }
    }
}
//最后响应微信回调成功
```

  
  
  

3.开发者收到设备**接听/拒接/挂断**的webhook后，调用萤石云开放平台微信voip操作接口

- webhook消息类型：ys.open.rtc.call，参考：[实时音视频webhook消息](https://open.ys7.com/help/4913)

```
代码示例如下：
//解析webhook消息体内容，拿到设备响应action
String action = callBody.getAction();
//获取accessToken
Map<String, String> headers = new HashMap<>();
String accessToken = getAccessToken();
headers.put("accessToken", accessToken);
if (action.equals(CallActionEnum.ANSWER.getCmdType()) || action.equals(CallActionEnum.REJECT.getCmdType())
        || action.equals(CallActionEnum.HANG_UP.getCmdType()) || action.equals(CallActionEnum.CANCEL.getCmdType())
        || action.equals(CallActionEnum.BUSY.getCmdType()) || action.equals(CallActionEnum.WAIT_TIMEOUT.getCmdType())) {
    DeveloperRoomRecord developerRoomRecord = developerRoomRecordDao.queryByCallId(callBody.getCallId());
    if (Objects.nonNull(developerRoomRecord)) {
        DeveloperRelation queryAccount = developerRelationDao.query(developerRoomRecord.getOpenId(), null, null, deviceSerial);
        //设备上行链路---小程序主动呼叫设备
        if (Objects.nonNull(queryAccount) && queryAccount.getPlatform().equals("小程序")) {
            Map<String, String> joinParam;

            String cmdType;
            if (action.equals(CallActionEnum.ANSWER.getCmdType())) {
                cmdType = "0";
            }
            if (action.equals(CallActionEnum.CANCEL.getCmdType()) || action.equals(CallActionEnum.HANG_UP.getCmdType())) {
                cmdType = "1";
            }
            if (action.equals(CallActionEnum.REJECT.getCmdType()) || action.equals(CallActionEnum.BUSY.getCmdType())
                    || action.equals(CallActionEnum.WAIT_TIMEOUT.getCmdType())) {
                cmdType = "2";
            }
            // 转发小程序进入/退出房间/拒接
            if (cmdType.equals("0") || cmdType.equals("1")) {
                joinParam = getVoipJoinParam(developerRoomRecord, queryAccount, null, cmdType);
            } else {
                joinParam = getVoipRejectParam(developerRoomRecord, queryAccount, cmdType, action);
            }
             // 调用开放平台微信voip操作接口 https://open.ys7.com/api/service/rtc/voip/trigger
            OkHttpCaller.HttpResponseEntity<MetaBody> voipJoinResp = OkHttpCaller.postForm(domain + VOIP_JOIN_URL, joinParam, headers, MetaBody.class);
            if (voipJoinResp.isSuccess() && Objects.nonNull(voipJoinResp.getData()) && voipJoinResp.getData().isSuccess()) {
                log.info("【设备上行-微信房间信息转发VOIP成功】，CallId:{}，Action:{}，deviceSerial:{}", callBody.getCallId(), action, deviceSerial);
            }
        }
    }
}
//最后响应webhook回调成功
```

  
  
  

4.开发者收到小程序取消呼叫，调用萤石云开放平台取消呼叫接口(通过callId保持唯一通话)

- [客户端取消呼叫](https://open.ys7.com/help/4343)