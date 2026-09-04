# API-通用AI-人证核验-身份证二要素+人像核验接口

> 更新时间: 2026-07-01T18:45:10.000+08:00

> 文档ID: 1347 | 来源树: AI

---

## 身份证二要素+人像核验接口

- 接口功能

   输入身份证号、对应姓名与人像信息，通过公安库认证，返回是否一致。

- 请求地址

`https://open.ys7.com/api/component/certificate/alp/ccp`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | bizCode | String | 业务码 | Y |
| Body | name | String | 姓名 | Y |
| Body | cardno | String | 身份证号码 | Y |
| Body | photo | String | 压缩处理后的图片字符串，压缩算法见下方“压缩算法”说明 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/component/certificate/alp/ccp?bizCode=xxxxx&accessToken=at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=张三' \
--data-urlencode 'cardno=330100199001010000' \
--data-urlencode 'photo='
```

- 返回数据

```
{
    "code": "1",
    "resultflow": "xxxxxxxxx",
    "similar": "99",
    "msg": "验证一致"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 响应码 |
| msg | String | 返回信息 |
| similar | String | 相似度 |
| resultflow | String | 结果流水号 |

- 返回码

| 返回码 | 返回消息 | 描述（是否通过公安认证） |
| --- | --- | --- |
| 1 | 验证一致 | 是 |
| 0 | 身份证信息有误 | 是 |
| -1 | 身份证信息与人像不匹配 | 是 |
| 2 | 失败，照片对比不一致 | 是 |
| 4 | 失败，身份证信息不一致 | 是 |
| 5 | 失败，证件不存在 | 是 |
| 6 | 失败，照片质量不佳 | 是 |
| 1001 | 请求参数格式错误 | 否 |
| 1002 | 用户名密码错误 | 否 |
| 1004 | 签名校验不通过，数据错误 | 否 |
| 1005 | 图片大小不符 | 否 |
| 1006 | 图像格式不支持 | 否 |
| 2002 | 连接数过多 | 否 |
| 2005 | 数据超时 | 否 |
| 4001 | 业务代码异常 | 否 |
| 4002 | 无权访问，请联系客服人员 | 否 |
| 9999 | 系统错误，或系统无法识别请求信息 | 否 |
| 10002 | accessToken异常或过期 | 否 |
| 50000 | 服务出现未知响应 | 否 |

**压缩算法（Java示例）**

```
private static int targetWidth = 270;  // 压缩后图片宽度
private static int targetHeight = 360; // 压缩后图片高度

public static String Compress(String sourceFile, int targetWidth, int targetHeight) {
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    File fromFile = new File(sourceFile);
    BufferedImage srcImage = null;
    int s_height = 0;
    int s_width = 0;
    try {
        srcImage = ImageIO.read(fromFile);
        s_height = srcImage.getHeight();
        s_width = srcImage.getWidth();
    } catch (IOException var13) {
        var13.printStackTrace();
    }
    if (targetWidth != s_width || targetHeight != s_height) {
        BigDecimal n = (new BigDecimal(s_height)).divide(new BigDecimal(s_width), 10, 0);
        BigDecimal m = (new BigDecimal(targetHeight)).divide(new BigDecimal(targetWidth), 10, 0);
        int flag = n.compareTo(m);
        try {
            if (flag == 0) {
                Thumbnails.of(new String[]{sourceFile}).forceSize(targetWidth, targetHeight).toOutputStream(outputStream);
            } else {
                if (flag > 0) {
                    srcImage = Thumbnails.of(new String[]{sourceFile}).width(targetWidth).asBufferedImage();
                } else if (flag < 0) {
                    srcImage = Thumbnails.of(new String[]{sourceFile}).height(targetHeight).asBufferedImage();
                }
                Thumbnails.Builder builder = Thumbnails.of(new BufferedImage[]{srcImage}).sourceRegion(Positions.CENTER, targetWidth, targetHeight).size(targetWidth, targetHeight);
                ImageOutputStream imageOut = ImageIO.createImageOutputStream(outputStream);
                ImageIO.write(builder.asBufferedImage(), "jpg", imageOut);
            }
            BASE64Encoder encoder = new BASE64Encoder();
            byte[] bytes = outputStream.toByteArray();
            return encoder.encodeBuffer(bytes).trim();
        } catch (IOException var14) {
            var14.printStackTrace();
        }
    }
    return readPhoto(sourceFile);
}

public static String readPhoto(String filepath) {
    FileInputStream fi = null;
    byte[] bytes = new byte[131072];
    try {
        fi = new FileInputStream(filepath);
        fi.read(bytes);
        fi.close();
    } catch (FileNotFoundException var6) {
        var6.printStackTrace();
    } catch (IOException var7) {
        var7.printStackTrace();
    }
    int index = bytes.length - 1;
    for (int i = bytes.length; i > 0; --i) {
        int a = bytes[i - 1];
        if (a != 0) {
            index = i;
            break;
        }
    }
    BASE64Encoder encoder = new BASE64Encoder();
    return encoder.encode(Arrays.copyOfRange(bytes, 0, index));
}
```