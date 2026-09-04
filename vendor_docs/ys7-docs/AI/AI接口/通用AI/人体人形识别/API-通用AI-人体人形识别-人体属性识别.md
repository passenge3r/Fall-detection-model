# API-通用AI-人体人形识别-人体属性识别

> 更新时间: 2026-07-01T18:43:41.000+08:00

> 文档ID: 1306 | 来源树: AI

---

## 人体属性识别

- 接口功能

   该接口用于识别用户上传照片中的人体属性信息，包括人体的穿着衣物，其颜色，类型等。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/human/analysis/body`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0：图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 图片，分辨率范围：800\*600~4096\*2160像素（但宽不能大于4096px且高不能大于2160px），图片最大2M。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/human/analysis/body' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image='
```

- 返回数据

```
{
    "requestId": "d17ed5583c8a4487a538e47b225beb35",
    "data": [
        {
            "jacetColor": { "val": "black", "des": "黑" },
            "ride": { "val": "no", "des": "不骑车" },
            "hat": { "val": "no", "des": "不戴帽子" },
            "bag": { "val": "no", "des": "不背包" },
            "trousersType": { "val": "longTrousers", "des": "长裤" },
            "trousersColor": { "val": "yellow", "des": "黄" },
            "hairStyle": { "val": "shortHair", "des": "短发" },
            "things": { "val": "no", "des": "不拎东西" },
            "gender": { "val": "male", "des": "男" },
            "rect": { "x": 202.00038, "y": 86.00064, "width": 489.99985, "height": 980 }
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
| data | Array | 人体属性识别结果列表 |
| jacetType | String | 上衣类型 |
| jacetColor | String | 上衣颜色 |
| ride | String | 是否骑车 |
| hat | String | 是否带帽 |
| bag | String | 是否背包 |
| trousersType | Map<String,String> | 下装类型 |
| trousersColor | Map<String,String> | 下装颜色 |
| hairStyle | Map<String,String> | 发型 |
| things | Map<String,String> | 是否拎东西 |
| gender | Map<String,String> | 性别 |
| ageGroup | String | 年龄段 |
| rect | Location | 人体在图片中的坐标 |

**坐标（Location）**

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| height | Int | 人体在图片中的高度，单位px |
| width | Int | 人体在图片中的宽度，单位px |
| x | Int | 人体在图片中左上角的横坐标，单位px |
| y | Int | 人体在图片中左上角的纵坐标，单位px |

**上衣颜色（jacetColor）/下衣颜色（trousersColor）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| white | 白 |
| silver | 银 |
| gray | 灰 |
| black | 黑 |
| red | 红 |
| deepBlue | 深蓝 |
| blue | 蓝 |
| yellow | 黄 |
| green | 绿 |
| brown | 棕 |
| pink | 粉 |
| purple | 紫 |
| deepGray | 深灰 |
| cyan | 青 |
| orange | 橙 |
| mixture | 混色 |

**上衣类型（jacetType）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| shortSleeve | 短袖 |
| longSleeve | 长袖 |

**下装类型（trousersType）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| shortTrousers | 短裤 |
| longTrousers | 长裤 |
| skirt | 裙子 |

**是否骑车（ride）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| no | 不骑车 |
| yes | 骑车 |

**是否带帽（hat）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| no | 不戴帽子 |
| yes | 戴帽子 |

**是否背包（bag）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| no | 不背包 |
| yes | 背包 |

**发型（hairStyle）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| shortHair | 短发 |
| longHair | 长发 |

**是否拎东西（things）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| no | 不拎东西 |
| yes | 拎东西 |

**性别（gender）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| male | 男 |
| female | 女 |

**年龄段（ageGroup）：**

| val | des |
| --- | --- |
| unknown | 未知 |
| earlyYouth | 少年 |
| youth | 青年 |
| middle | 中年 |
| old | 老年 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 |  |
| 10007 | 调用次数超限 |  |
| 10013 | 无权限调用 |  |
| 10029 | 接口调用太频繁 |  |
| 49999 | 操作异常 | 接口调用异常 |
| 50000 | 服务器异常 |  |
| 60200 | 非法的服务名 |  |
| 60201 | 缺失必传参数或参数校验错误 |  |
| 60202 | 参数解析错误 |  |
| 60203 | 未开通相关服务 |  |
| 60204 | 服务已开通 |  |
| 60205 | 服务内部错误 |  |
| 60206 | 并发数超限 |  |
| 60210 | 图片数据错误 |  |
| 60211 | 图片尺寸错误(太大或太小) |  |
| 60212 | 图片大小超过2M限制 |  |
| 60213 | 下载图片失败 |  |
| 60214 | 参数错误 |  |
| 60215 | 转存图片失败 |  |
| 60216 | 参数错误：无效服务名称 |  |
| 60405 | 图片地址错误 |  |
| 60507 | 服务超时 |  |
| 60508 | 服务器繁忙 |  |
| 60509 | 该功能暂时不支持 |  |