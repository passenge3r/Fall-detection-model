# ezOtaSDK接入手册（android版）

> ezOtaSDK接入手册（android版）

> 更新时间: 2026-05-25T16:44:41.000+08:00

> 文档ID: 1867 | 来源树: SDK及示例

---

# 1. 概述

ezOtaSDK 是设备接入萤石云平台的一个重要的工具套件，该套件提供以下能力：

| 功能点 | 描述 |
| --- | --- |
| 设备认证、安全 |  |
| 设备查包 |  |
| 可升级固件包下载 |  |
| 下载/升级进度上报 |  |

# 2. 名词解释

| 名词 | 含义/作用 | 获取方式 |
| --- | --- | --- |
| productKey | 产品ID，萤石开放平台中产品的唯一标识。在业务中用于唯一标识产品信息。在SDK集成等中均需应用。 | 开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 |
| deviceLicense | 产品密钥，确认产品使用权限，在SDK集成等中均需应用。 | 开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 |
| deviceName | 设备序列号，设备实际的序列号。由您定义。需要保证产品下唯一，不可重复。 | 由您定义，可提前导入萤石OTA控制台，便于管理。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理 |
| deviceId | 设备ID，设备注册并激活后平台颁发的唯一ID。萤石开放平台中设备唯一标识。 | SDK在第一次注册激活成功或向平台获取并回调给设备保存，设备拿到后必须固话保证不丢失。后续可在萤石开放平台OTA控制台-设备列表中获取。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理 |
| dasHttpPort | 升级接入服务端口号，默认https为443端口 |  |
| dasHttpHost | 升级接入服务域名 | http:dev.ys7.com |
| deviceMac | 设备网卡的MAC地址 |  |

# 3. OTA产品接入流程

1. 在OTA控制台中创建产品信息，并获取productKey与deviceLicense（即产品ID与产品密钥）——详见[《使用指南》](https://open.ys7.com/help/1715)3.1.1创建产品（产品线）
2. 在控制台中创建产品模块。——详见[《使用指南》](https://open.ys7.com/help/1715)3.4.1添加模块
3. 在控制台中导入设备信息。——详见[《使用指南》](https://open.ys7.com/help/1715)3.3.1导入设备
4. ezOtaSDK设备接入。——详见本文档
5. 上传升级包、下发升级任务。激活设备后升级——详见[《使用指南》](https://open.ys7.com/help/1715)3.5、3.6内容

## 3.1ezOtaSDK设备接入流程

![](http://resource.eziot.com/group2/M00/00/B7/CtwQF2UmVFWARcW6AAEZ3X9apaQ736.png)

# 4. 使用指南

## 4.1导入OtaSDK的aar文件

ota.aar

## 4.2 添加依赖

api 'com.squareup.retrofit2:converter-gson:2.4.0'

## 4.3 SDK的使用

### 4.3.1 初始化SDK

```
	OtaManager.init(MyApplication.sApplication, {initInfo}, {debug}, new OtaManager.Callback<String>() {
	    @Override
	    public void onSuccess(String deviceId) {
	         //初始化成功后，保存deviceId到本地，下次使用时要传入	 
	    }	 
	    @Override
	    public void onFail(int errorCode, String errorMessage) {  
	    }
	});
```

参数说明：

```
/**
* sdk初始化
*
* @param application
* @param initInfo,初始化信息信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_init_info_t
*  {
*    "byfile":0,     ///< 必须，0-configInfo是json字符串
*    "deviceId":"RkaPdVlwmWpMTOrsOWvwJbKhRG1pyLCY",
*    "configInfo":{    ///< 必须,可以是文件路径也可以是json字符串
*       "dasHttpPort":443,  ///< 必须
*       "dasHttpHost":"test12-devapi.ys7.com",  ///< 必须
*       "deviceMac":"3C:05:82:12:34:56",    ///< 必须
*       "devVersion":"v1.0.0 build 220915",    ///< 必须
*       "productLicense":{
*          "productKey":"TEST_OTA_OPEN",///< 必须
*          "deviceName":"test1-deviceName",///< 必须
*          "deviceLicense":"FM2G692TtBhT4byQy3zmD3"///< 必须
*       }
*    }
* }
* @param isDebug 是否开启调试模式
* Return: 0-初始化成功
* Return: other-初始化失败
* @param isDebug
*/
public static int init(Application application, String initInfo, boolean isDebug, Callback<String> callback)
```

### 4.3.2 查询固件包

```
	OtaManager.queryPackage({modules}, new OtaManager.Callback<List<QueryResponse.PackageInfo>>() {
	 
	    @Override
	    public void onSuccess(List<QueryResponse.PackageInfo> packageList) {	          	 
	    }	 
	    @Override
	    public void onFail(int errorCode, String errorMessage) {         
	    }
	});
```

参数说明：

```
/**
* 查询固件包
*
*
* @param modules 产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_modules_t
*  {
*    "num":1,            ///< 必须，模块数量
*    "modules":[
*       {
*          "supportDiff":0,///< 必须
*          "mod_name":"ZJW_TEST_SWITCH",///< 必须
*          "fw_ver":"V1.0.0 build 211115"///< 必须
*       }
*    ]
* }
* @param callback 回调 onSuccess onFail
* Return:packageList,产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_firmwarePackageList_t
*  {
*    "errCode":0,      ///< 错误码信息，如果查不到包，此处为对应错误码
*    "num":1,         ///< 查到的可升级模块数量
*    "packageList":[
*       {
*          "fileType":1,   ///< 固件类型，0：整包，1：差分包
*          "mod_name":"ZJW_TEST_SWITCH",   ///< 模块名称
*          "filesize":15412,       ///< 升级包文件大小
*          "fw_ver":"V1.1.0 build 220531",      ///< 模块最新的固件版本号, 格式为:V1.1.0 build 220427格式
*          "fw_ver_dst":"V1.0.0 build 211115",      ///< 差分升级的目标版本, 如果为差分包，该参数为当前固件版本
*          "digest":"12162bbff30bf22b7ada1e744a3a04af",    ///< 升级包摘要,MD5小写摘要
*          "filepath":"/file/12162bbff30bf22b7ada1e744a3a04af", ///< 升级包文件保存路径
*          "dsc":"升级包描述",
*          "conditions":{
*             "silent_upgrade":1,   ///< 升级方式：0-触发升级,1-静默升级
*             "battery_limit":90,   ///< 升级时和下载固件包时最低电量要求：限制百分比:0-100,0表示不限制
*             "network_limit":0,       ///< 固件包下载网络要求 0-不限制,1-非流量模式可以下载（非4G/5G模式可下载）
*             "startTime":"20:00", ///< 允许/建议下载和升级的开始时间00:00（小时：分钟）
*             "endTime":"08:00"  ///< 允许/建议下载和升级的结束时间 00:00（小时：分钟）
*          }
*       }
*    ]
* }
*/
public static void queryPackage(String modules, Callback<List<QueryResponse.PackageInfo>> callback)
```

### 4.3.3 下载固件包

```
	OtaManager.downloadPackage({byfile},{fileType},{supportDiff},{mod_name},{fw_ver},{fw_ver_dst},{dirPath},new OtaManager.DownloadCallback() {
	    @Override
	    public void onProgress(int percentage) {
	    }
	    @Override
	    public void onComplete(File targetFile) {
	        Toast.makeText(MainActivity.this, "下载成功，文件路径:" + targetFile, Toast.LENGTH_LONG).show();
	    }
	    @Override
	    public void onFail(int code, String errorMsg) {
	        Toast.makeText(MainActivity.this, "下载失败:" + errorMsg, Toast.LENGTH_LONG).show();
	    }
	});
```

### 4.3.4 取消下载

```
	OtaManager.stopDownloadPackage({mod_name}, new OtaManager.Callback<String>() {
	    @Override
	    public void onSuccess(String result) {
	    }
	    @Override
	    public void onFail(int errorCode, String errorMessage) {
	    }
	});
```

参数说明：

```
/**
* 请求SDK停止下载固件包接口
* @param mod_name 模块名称/型号
* @return 0表示成功
*/
public static int stopDownloadPackage(String mod_name,Callback<String> callback)
```

### 4.3.5 取消下载

```
	OtaManager.reportUpgradeResult({module},{code}, new OtaManager.Callback<String>() {
	           @Override
	           public void onSuccess(String result) {
	               hideLoadingDialog();
	               Toast.makeText(MainActivity.this,result,Toast.LENGTH_SHORT).show();
	           }
	           @Override
	           public void onFail(int errorCode, String errorMessage) {
	               hideLoadingDialog();
	               Toast.makeText(MainActivity.this,errorMessage+" "+errorCode,Toast.LENGTH_SHORT).show();
	           }
	       });
```

参数说明：

```
/**
* param[in]:module,产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_module_t
*     {
*    "module":{
*       "supportDiff":0,///< 必须
*       "mod_name":"ZJW_TEST_SWITCH",///< 必须
*       "fw_ver":"V1.0.0 build 211115"///< 必须
*        }
*    }
* param[in]:errCode,0-升级成功，其他-升级失败错误码，失败错误码使用ezDevSDK_error.h文件内的ezOtaSDK_upgrade_errcode_e
* Return: 0-成功
**/
public static void reportUpgradeResult(String moudule,int errCode,Callback<String> callback)
```

### 4.3.6 反初始化

```
	OtaManager.fini(new OtaManager.Callback<Integer>() {
	    @Override
	    public void onSuccess(Integer code) {
	        Toast.makeText(MainActivity.this,"反初始化成功",Toast.LENGTH_SHORT).show();
	    }
	    @Override
	    public void onFail(int errorCode, String errorMessage) {
	        Toast.makeText(MainActivity.this,"反初始化失败 "+errorMessage,Toast.LENGTH_SHORT).show();
	    }
	});
```

参数说明：

```
/**
* 反初始化
* Return: 0-反初始化成功
* Return: other-反初始化失败
*/
public static void fini(Callback<Integer> callback)
```

### 4.3.7 设置日志

```
/**
* 设置日志
* @param logLevel logLevel：0-5
* @param logFile 日志文件保存路径，非必须
*/
OtaManager.setLogLevel(int logLevel, File logFile);
```