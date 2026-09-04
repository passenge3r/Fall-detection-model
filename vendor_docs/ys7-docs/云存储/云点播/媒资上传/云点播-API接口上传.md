# 云点播-API接口上传

> 云点播-API接口上传

> 更新时间: 2026-05-25T16:37:11.000+08:00

> 文档ID: 4388 | 来源树: 云存储

---

# 云点播媒资上传API接口

开发者可以通过以下步骤，实现通过API接口传到云点播存储空间里。

1、获取上传地址：
<https://open.ys7.com/help/4439>

2、手动上传：
通过接口或者其他方式，将文件上传到步骤1里的上传地址

拿到步骤1的响应结果后，可使用post form表单上传的方式上传文件，示例如下：

```
curl --location 'https://open-mediarecoder.oss-cn-hangzhou.aliyuncs.com' \   // 该地址，取自 步骤1接口响应data集合结果元素的url
--form 'OSSAccessKeyId="LTAI4G6HFM3XPqa8rBjxHJRE"' \    //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'success_action_status="200"' \  //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'x-oss-server-side-encryption="AES256"' \ //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'Signature="D6AYlZEtH/9HGwls8lAGOCL81FM="' \  //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'key="E1/7/11/dc240b30c2b64dc5ac134279c1ec2595/0/PkNc0Lf/N1/GK1716834-1/00/8b0e2882"' \  //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'policy="eyJleHBpcmF0aW9uIjoiMjAyNi0wMS0wN1QwOTowNDo0MS4xMjlaIiwiY29uZGl0aW9ucyI6W1siZXEiLCIka2V5IiwiRTEvNy8xMS9kYzI0MGIzMGMyYjY0ZGM1YWMxMzQyNzljMWVjMjU5NS8wL1BrTmMwTGYvTjEvR0sxNzE2ODM0LTEvMDAvOGIwZTI4ODIiXSxbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwxLDEwNzM3NDE4MjQwXV19"' \   //该参数的key和value，取自 步骤1接口响应data集合结果元素的fields中的参数
--form 'file=@"/C:/Users/123/Pictures/Camera Roll/kafka.jpg"'   //file，要上传的文件，需要放到最后一个参数的位置
```

上传成功时，接口响应httpStatus为200 OK，示例如下：
![](https://izhstatic.ys7.com/vasp-openweb/1772422253330_%E9%98%BF%E9%87%8C%E4%BA%91postform%E8%A1%A8%E5%8D%95%E4%B8%8A%E4%BC%A0.png)

3、上传成功后，通知萤石上传成功，调保存元数据接口
<https://open.ys7.com/help/4440>