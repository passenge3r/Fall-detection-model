# 设置人脸识别解锁开关（PUT）

> 设置人脸识别解锁开关（PUT）

> 更新时间: 2026-05-25T16:38:39.000+08:00

> 文档ID: 5089 | 来源树: OPEN_API

---

# 设置人脸识别解锁开关（PUT）

> otap设备属性设置接口

---

## 接口URL

https://open.ys7.com/api/v3/device/otap/prop

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| Content-Type | application/json | Y |  |  |
| accessToken | string | Y | 用户访问令牌 |  |
| deviceSerial | string | Y | 设备序列号 |  |
| localIndex | string | Y | 资源序号 |  |
| resourceCategory | string | Y | 资源种类，描述资源的类型，离家模式按键指示灯：DoorLock |  |
| domainIdentifier | string | Y | 功能点领域，填写报备时的属性所在领域，离家模式按键指示灯：DoorLockCtrl |  |
| propIdentifier | string | Y | 功能点标识，填写报备时的属性标识符，离家模式按键指示灯：FaceRecognitionUnlockCfg |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| data | json | Y | Body部分，JSON结构，格式参见属性报备时的示例报文。 提交该PUT请求时，HTTP头中的Content- Type请设置为 application/json |  |
| -enabled | boolean | Y | 人脸识别解锁开关：true-开，false-关 |  |
| -sensitivity | int | 灵敏度, 0-高, 1-低, 2-中 |  |  |
| -mode | int | 解锁方式, 0-自动, 1-手动 |  |  |
| -veinEnabled | boolean | Y | 掌静脉解锁功能开关, true-开，false-关 |  |

### 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: at.d907x2hg1593weqo3ne8xwvy1yv64f7u-6f16l1ahik-16bycsf-jcpn9lvxo' \
--header 'deviceSerial: BG9859941' \
--header 'localIndex: 0' \
--header 'resourceCategory: DoorLock' \
--header 'domainIdentifier: DoorLockCtrl' \
--header 'propIdentifier: FaceRecognitionUnlockCfg' \
--header 'Content-Type: application/json' \
--data '{
    "data": {
        "enabled": false,
        "sensitivity": 1,
        "mode": 0
    }
}'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |
| data | object | data |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 400 | 10001 | 参数错误 |  |
| 403 | 10031 | 账号无权限访问此设备 |  |
| 200 | 20007 | 设备不在线 |  |
| 403 | 20018 | 该用户不拥有该设备 |  |