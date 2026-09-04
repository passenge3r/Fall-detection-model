# ezOtaSDK-jni接入手册

> ezOtaSDK-jni接入手册

> 更新时间: 2026-05-25T16:44:41.000+08:00

> 文档ID: 1868 | 来源树: SDK及示例

---

# 1.概述

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
| deviceName | 设备序列号，设备实际的序列号。由您定义。需要保证产品下唯一，不可重复。 | 由您定义，可提前导入萤石OTA控制台，便于管理。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理。 |
| deviceId | 设备ID，设备注册并激活后平台颁发的唯一ID。萤石开放平台中设备唯一标识。 | SDK在第一次注册激活成功或向平台获取并回调给设备保存，设备拿到后必须固话保证不丢失。后续可在萤石开放平台OTA控制台-设备列表中获取。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理 |
| dasHttpPort | 升级接入服务端口号，默认https为443端口 |  |
| dasHttpHost | 升级接入服务域名 | http:dev.ys7.com |
| deviceMac | 设备网卡的MAC地址 |  |

# 3. OTA产品接入流程

1. 在OTA控制台中创建产品信息，并获取productKey与deviceLicense（即产品ID与产品密钥）——详见[《使用指南》](https://open.ys7.com/help/1715)3.1.1创建产品（产品线）
2. 在控制台中创建产品模块。——详见[《使用指南》](https://open.ys7.com/help/1715)3.4.1添加模块
3. 在控制台中导入设备信息。——详见[《使用指南》](https://open.ys7.com/help/1715)3.3.1导入设备
4. ezOtaSDK设备接入。——详见本文档
5. 上传升级包、下发升级任务。激活设备后升级——详见详见[《使用指南》](https://open.ys7.com/help/1715)3.5、3.6内容

## 3.1ezOtaSDK设备接入流程

![](http://resource.eziot.com/group2/M00/00/B7/CtwQF2UmETKAcY4SAAEZ3X9apaQ801.png)

# 4. ezOtaSDK库文件依赖关系

## 4.1库文件列表：

libezOtaSDK.so：jni OTA库

libota.a(.so)：OTA升级模块

libcomm.a(.so)：公共组件模块，日志、json、http、https

libezos.a(.so)：系统抽象接口，用于兼容linux、windows、rt-thread、freeRTOS等系统

libmbedtls.a(.so)：SSL加密模块，对于使用HTTPS可选择使用mbedtls或者openssl

## 4.2头文件列表

ezOtaSDK.java：jni接口

ezOtaSDK\_error.h：SDK错误码描述

## 4.3库文件依赖关系

![](http://resource.eziot.com/group2/M00/00/B7/CtwQFmUmEeeAIzs6AABGr9R3xsg901.png)

## 4.4SDK目录结构

- doc——接入文档
- example——参考demo
- - cpp\_example——cpp测试demo
- - jni\_example——jni测试demo
- inc——头文件
- lib——库文件

# 5. 设备接口调用流程

## 5.1SDK初始化流程

- 初始化前先设置日志级别，每次启动只需初始化一次即可
- SDK回调给设备的deviceId，设备必须保存好，不可以丢失，否则会导致设备被风控或拉黑
- jni接口：public native int init(String initInfo);
- return 0 - 成功,other-失败\ref ezOtaSDK\_errcode\_e

![](http://resource.eziot.com/group2/M00/00/B7/CtwQF2UmEr-AKsXSAAE3LG6SkA4958.png)

## 5.2查升级包流程

- 查包间隔建议在5分钟以上每次，不可以频繁查包
- 查包前确保SDK已经初始化
- jni接口：public native String query\_package(String modules);
- \retval 0 - 成功
- \retval ota\_errcode\_no\_package-没有查到有部署固件包
  ![](http://resource.eziot.com/group2/M00/00/B7/CtwQFmUmE1eAGPv6AADhZazlpmc711.png)

## 5.3执行升级流程

必须在有查到可升级包的情况下才可以调用下载接口，否则调用无效

下载固件包接口：

- jni接口：public native int download\_package(String package\_info);
- return 0 - 成功,other-失败\ref ezOtaSDK\_errcode\_e

上报升级结果接口：

- jni接口：public native int report\_upgrade\_result(String module, int errCode);
- return 0 - 成功,other-失败\ref ezOtaSDK\_errcode\_e

![](http://resource.eziot.com/group2/M00/00/B7/CtwQF2UmE9qAeNsSAAF4yQ35buM996.png)

# 6. SDK错误码说明

见ezOtaSDK\_error.h文件

# 7. SDK接口说明(参考demo为HelloWorld.java)

## 7.1设置SDK日志级别

```
/*************************************************
* Function:    set_log_level
* Description: 设置SDK日志级别
* Input:       log_level：0-5
* Input:       log_path: 日志文件保存路径，非必须
* Output:      N/A
* Return:      状态码
*************************************************/
public native int set_log_level(int log_level, String log_path);
```

表7.1-1 ezOtaSDK\_set\_log\_level接口定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | log\_level | 设置日志级别 | 必须 |
| const char \* | log\_path | 设置日志文件保存路径 | 非必须 |

## 7.2SDK初始化接口

```
/******************
* Function:    init
* Description: SDK初始化接口
* param:initInfo,初始化信息信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_init_info_t
*     {
*        "byfile":0,     ///< 必须，1-configInfo是文件路径，0-configInfo是json字符串
*        "deviceId":"RkaPdVlwmWpMTOrsOWvwJbKhRG1pyLCY",
*        "configInfo":{        ///< 必须,可以是文件路径也可以是json字符串
*            "dasHttpPort":443,  ///< 必须，平台端口
*            "dasHttpHost":"test12-devapi.ys7.com",  ///< 必须，平台域名
*            "deviceMac":"3C:05:82:12:34:56",    ///< 必须，设备MAC地址
*            "devVersion":"v1.0.0 build 220915",    ///< 必须，设备版本号
*            "productLicense":{
*                "productKey":"TEST_OTA_OPEN",///< 必须
*                "deviceName":"test1-deviceName",///< 必须
*                "deviceLicense":"FM2G692TtBhT4byQy3zmD3"///< 必须
*            }
*        }
*    }
* Return: 0-初始化成功
* Return: other-初始化失败
******************/
public native int init(String initInfo);
```

表7.2-1 ezOtaSDK\_init\_info\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | byFile | configInfo参数类型：0：configInfo为ezOtaSDK\_config\_info\_t结构体,1：configInfo为文件路径 | 必须 |
| string/object | configInfo | byFile=0：configInfo为ezOtaSDK\_config\_info\_t结构体byFile=1：configInfo为文件路径 | 必须 |

表7.2-2 configInfo定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | dasHttpPort | 平台端口 | 必须 |
| string | dasHttpHost | 平台域名 | 必须 |
| string | deviceMac | 设备网卡的MAC地址 | 必须 |
| string | devVersion | 设备固件版本号 | 必须 |
| object | productLicense | 产品license信息，与控制台产品信息中的“产品密钥”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.1产品管理 | 必须 |

表7.2-3 productLicense定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| string | productKey | 产品ID，萤石开放平台中产品的唯一标识。在业务中用于唯一标识产品信息。在SDK集成等中均需应用。开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 | 必须 |
| string | deviceName | 设备序列号，设备实际的序列号。由您定义。需要保证产品下唯一，不可重复。由您定义，可提前导入萤石OTA控制台，便于管理。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理 | 必须 |
| string | deviceLicense | 产品密钥，确认产品使用权限，在SDK集成等中均需应用。开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 | 必须 |

## 7.3SDK反初始化接口

```
/******************
* Function:    fini
* Description: SDK反初始化接口
* Return: 0-反初始化成功
* Return: other-反初始化失败
******************/
public native int fini();
```

## 7.4SDK查包接口

```
/******************
* Function:    query_package
* Description: SDK查包接口
* param[in]:modules,产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_modules_t
*     {
*        "num":1,                ///< 必须，模块数量 
*        "modules":[
*            {
*                "supportDiff":0,///< 必须
*                "mod_name":"ZJW_TEST_SWITCH",///< 必须
*                "fw_ver":"V1.0.0 build 211115"///< 必须
*            }
*        ]
*    }
* Return:packageList,产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_firmwarePackageList_t
*     {
*        "errCode":0,        ///< 错误码信息，如果查不到包，此处为对应错误码 
*        "num":1,            ///< 查到的可升级模块数量 
*        "packageList":[
*            {
*                "fileType":1,   ///< 固件类型，0：整包，1：差分包 
*                "mod_name":"ZJW_TEST_SWITCH",   ///< 模块名称 
*                "filesize":15412,       ///< 升级包文件大小 
*                "fw_ver":"V1.1.0 build 220531",      ///< 模块最新的固件版本号, 格式为:V1.1.0 build 220427格式 
*                "fw_ver_dst":"V1.0.0 build 211115",      ///< 差分升级的目标版本, 如果为差分包，该参数为当前固件版本
*                "digest":"12162bbff30bf22b7ada1e744a3a04af",    ///< 升级包摘要,MD5小写摘要 
*                "dsc":"升级包描述",
*                "conditions":{
*                    "silent_upgrade":1,   ///< 升级方式：0-触发升级,1-静默升级 
*                    "battery_limit":90,   ///< 升级时和下载固件包时最低电量要求：限制百分比:0-100,0表示不限制 
*                    "network_limit":0,       ///< 固件包下载网络要求 0-不限制,1-非流量模式可以下载（非4G/5G模式可下载） 
*                    "startTime":"20:00", ///< 允许/建议下载和升级的开始时间00:00（小时：分钟） 
*                    "endTime":"08:00"    ///< 允许/建议下载和升级的结束时间 00:00（小时：分钟）
*                }
*            }
*        ]
*    }
******************/
public native String query_package(String modules);
```

表7.4-1 modules定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | num | 查询的模块数量，支持多模块升级例如：1个应用表示一个模块，子系统也属于一个模块 | 必须 |
| object | modules | 模块的信息列表 | 必须 |

表7.4-2 module定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | supportDiff | 是否支持差分升级 | 必须 |
| string | mod\_name | 设备型号/模块名称模块ID，获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.4模块管理。 | 必须 |
| string | fw\_ver | 设备/模块当前的版本号，格式必须为V1.0.0 build 220427格式 | 必须 |

表7.4-3 packageList定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | errCode | 错误码信息 0：查包成功ota\_errcode\_no\_package：没有查到有部署固件包other：失败ref ezOtaSDK\_errcode\_e |
| int | num | 查询到的可升级模块数量 |
| object | packageList | 查询到的可升级包信息 |

表7.4-4ezOtaSDK\_firmwarePackageInfo\_t定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | fileType | 固件包类型，0：整包；1：差分包与控制台上传包时的“升级包类型”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| string | filesize | 升级包文件大小 |
| string | mod\_name | 模块名称/型号模块ID，与控制台上传包时的“所属OTA模块”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| string | fw\_ver | 模块最新的固件版本号, 格式为:V1.1.0 build 220427格式与控制台上传包时的“升级包版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| string | fw\_ver\_dst | 与控制台上传包时的“待升级版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| string | digest | 升级包MD5签名，用于校验与控制台上传包时的“Md5”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| string | dsc | 升级包描述，例如：本次升级迭代了xxxxx内容，解决了xxxxxBUG与控制台上传包时的“升级包描述”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| object | conditions | 升级条件 |

表7.4-5 conditions定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | silent\_upgrade | 升级方式：0-触发升级,1-静默升级 |
| int | battery\_limit | 升级时和下载固件包时最低电量要求：限制百分比:0-100,0表示不限制 |
| int | network\_limit | 固件包下载网络要求 0-不限制,1-非流量模式可以下载（非4G/5G模式可下载） |
| string | startTime | 允许/建议下载和升级的开始时间00:00（小时：分钟） |
| string | endTime | 允许/建议下载和升级的开始时间00:00（小时：分钟） |

## 7.5SDK开始下载固件包接口

```
/******************
* Function:    download_package
* Description: SDK下载固件包接口
* param:package_info,产品信息，json字符串，参考结构体ezOtaSDK_download_info_t
*     {
*        "fileType":1,     ///< 必须,固件类型，0：整包，1：差分包 
*        "mod_name":"ZJW_TEST_SWITCH",///< 必须
*        "fw_ver":"V1.1.0 build 220531",///< 必须
*        "fw_ver_dst":"V1.0.0 build 211115",///< 非必须，当为差分包时必须传入,如果为差分包，该参数为当前固件版本
*        "dirpath":"file"///< 必须
*    }
* Return:      0-下载成功
******************/
public native int download_package(String package_info);
```

表7.5-1 package\_info定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | fileType | 固件包类型，0：整包；1：差分包与控制台上传包时的“升级包类型”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| string | mod\_name | 模块名称/型号模块ID，与控制台上传包时的“所属OTA模块”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| string | fw\_ver | 需要下载的固件版本号, 格式为:V1.1.0 build 220427格式与控制台上传包时的“升级包版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| string | fw\_ver\_dst | 如果为差分包需要输入当前模块的固件版本号与控制台上传包时的“待升级版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| string | dirpath | ota文件临时存放目录路径，目录后面不要带/ | 非必须 |

## 7.6SDK停止下载固件包接口

```
/******************
* Function:    stop_download_package
* Description: 请求SDK停止下载固件包接口
* param:mod_name，模块名称/型号
* Return:      0-下载成功
******************/
public native int stop_download_package(String mod_name);
```

## 7.7SDK上报升级结果接口

```
/******************
* Function:    query_package
* Description: SDK查包接口
* param[in]:module,产品模块信息，json字符串，参考ezOtaSDK.h文件内结构体：ezOtaSDK_module_t
*     {
*        "module":{
*            "mod_name":"ZJW_TEST_SWITCH",///< 必须，模块名称/设备型号 
*            "fw_ver":"V1.0.0 build 211115"///< 必须，版本号 
*        }
*    }
* param[in]:errCode,0-升级成功，其他-升级失败错误码，失败错误码使用ezDevSDK_error.h文件内的ezOtaSDK_upgrade_errcode_e
* Return: 0-成功
******************/
public native int report_upgrade_result(String module, int errCode);
```

# 8. 参考用例

见jni\_example/HelloWorld.java