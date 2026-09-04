# AI产品开发指南

> AI产品开发指南

> 更新时间: 2026-05-25T16:37:31.000+08:00

> 文档ID: 4224 | 来源树: AI

---

# AI产品开发指南

## 使用前提

### 必要条件

已开通萤石云开发者账号
完成企业实名认证

## 🔑 认证准备

```
# 获取accessToken流程示例
curl -X POST "https://open.ys7.com/api/lapp/token/get" \
     -d "appKey=您的应用密钥" \
     -d "appSecret=您的应用密钥"
```

## 📦 请求规范

### **公共请求头**

```
Content-Type: application/json
accessToken: at.xxxxx
```

## ⚠️ 重要限制说明

```
+检测接口特殊要求：
- 需联系客服申请开通
- 仅支持JPG/PNG格式
- 单图片处理耗时约1-5秒

! 人体识别注意事项：
1. Base64不允许包含MIME类型声明
2. URL有效期需>5分钟
```

## 📄 响应处理

```
{
  "msg": "success",//响应信息
  "code": "200",//响应编码
  "data": {//响应数据
    "frameIdx": 0,//第0帧图片，对于此算法类型无实际意义
    "imageHeight": 375,//图片高度
    "imageWidth": 500,//图片宽度
    "contentAnn": {/分析结果
      "bboxes": [//检测框信息 
        {
          "points": [//坐标点集合，第一个点代表左上的坐标点，第二个代表右下的坐标点位，以此形成一个矩形区域
            {
              "x": 0.684,//x点，默认宽度为1，按比例缩放
              "y": 0.536//y点，默认高度为1，按比例缩放
            },
            {
              "x": 0.866,//x点
              "y": 0.73866665//y点
            }
          ],
          "weight": 0.3819,//检测置信度，代表算法检测出来的可信度
          "index": 0,//检测框编号
          "tagInfo": {//检测框tag
            "tag": "球",//tag的key
            "labels": null//对key的描述
          }
        }
      ],
      "textInfos": null//检测结果文字描述
    }
  },
  "requestId": "0EF7819-ea38-11e7-bf0d-fa16sR4ESL11"//请求id
}
```

## 错误代码表

| 状态码 | 类型 | 解决方案指引 |
| --- | --- | --- |
| 10001 | 认证失败 | 检查token有效期（默认7天） |
| 60201 | 参数错误 | 检测入参 |
| 60203 | 未开通相关服务 | 联系客服开通 |
| 60214 | 参数错误:无效的图片 | 检查图片规格 |

## 🛠️ 开发最佳实践

### 异步处理方案

```
# Python异步处理示例
import time

def async_analysis(image_url):
    task_id = submit_task(image_url)
    retry_count = 0
    while retry_count < 5:
        result = get_result(task_id)
        if result['status'] == 'completed':
            return result
        time.sleep(2 ** retry_count)  # 指数退避
        retry_count += 1
    raise TimeoutError("分析超时")
```

### 性能优化建议

图片预处理：

```
# 使用ffmpeg压缩图片
ffmpeg -i input.jpg -q:v 2 -vf "scale='min(1024,iw)':-2" output.jpg
```

连接池配置：

```
// Java HttpClient配置示例
PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
cm.setMaxTotal(20);  // 最大连接数
cm.setDefaultMaxPerRoute(5);  // 单路由最大连接
```

缓存策略：

```
AccessToken缓存至少24小时
```