# API-通用AI-车辆车牌识别-车辆属性检测

> 更新时间: 2026-07-01T18:44:38.000+08:00

> 文档ID: 1332 | 来源树: AI

---

## 车辆属性检测

- 接口功能

   该接口用于识别用户上传照片中的车辆属性信息，包括车身颜色、品牌等。图片大小800\*600px – 3900\*2300px（但宽不能大于3900px且高不能大于2300px）。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/vehicle/analysis/props`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0:图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 图片，分辨率范围：800\*600~3900\*2300像素，图片最大2M。注：下载图片时可能由于网络等原因导致下载时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/vehicle/analysis/props' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image='
```

- 返回数据

```
{
    "requestId": "ba37e869a03946288edc36d413I013c2",
    "data": [
        {
            "plateNumber": "浙AJ268V",
            "vehicleColor": { "val": "unknown", "des": "未知" },
            "vehicleType": { "val": "vehicle", "des": "轿车" },
            "vehicleLogo": "日产",
            "vehicleSublogo": "日产-骐达",
            "vehicleModel": "日产-骐达-2009,2008",
            "rect": { "x": 432.00003, "y": 293.99954, "width": 640, "height": 640.0006 }
        }
    ],
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data | Array | 检测结果列表 |
| data[].plateNumber | String | 车牌号 |
| data[].vehicleColor | Object | 车身颜色（val:值，des:描述） |
| data[].vehicleType | Object | 车辆类型（val:值，des:描述） |
| data[].vehicleLogo | String | 品牌 |
| data[].vehicleSublogo | String | 子品牌 |
| data[].vehicleModel | String | 车辆年款 |
| data[].rect | Location | 车辆在图片中的坐标 |
| data[].rect.height | Int | 车辆的高度，单位px |
| data[].rect.width | Int | 车辆的宽度，单位px |
| data[].rect.x | Int | 车辆在图片中左上角的横坐标，单位px |
| data[].rect.y | Int | 车辆在图片中左上角的纵坐标，单位px |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 10007 | 调用次数超限 | 调用次数超限 |
| 10013 | 无权限调用 | 无权限调用 |
| 10029 | 接口调用太频繁 | 降低调用频率 |
| 49999 | 操作异常 | 接口调用异常 |
| 50000 | 服务器异常 | 服务器异常 |
| 60200 | 非法的服务名 | 非法的服务名 |
| 60201 | 缺失必传参数或参数校验错误 | 缺失必传参数或参数校验错误 |
| 60202 | 参数解析错误 | 参数解析错误 |
| 60203 | 未开通相关服务 | 未开通相关服务 |
| 60204 | 服务已开通 | 服务已开通 |
| 60205 | 服务内部错误 | 服务内部错误 |
| 60206 | 并发数超限 | 并发数超限 |
| 60210 | 图片数据错误 | 图片数据错误 |
| 60211 | 图片尺寸错误(太大或太小) | 图片尺寸错误 |
| 60212 | 图片大小超过2M限制 | 图片大小超过2M限制 |
| 60213 | 下载图片失败 | 下载图片失败 |
| 60214 | 参数错误 | 参数错误 |
| 60215 | 转存图片失败 | 转存图片失败 |
| 60216 | 参数错误：无效服务名称 | 无效服务名称 |
| 60405 | 图片地址错误 | 图片地址错误 |
| 60507 | 服务超时 | 服务超时 |
| 60508 | 服务器繁忙 | 服务器繁忙 |
| 60509 | 该功能暂时不支持 | 该功能暂时不支持 |
| 60511 | OCR识别失败 | OCR识别失败 |