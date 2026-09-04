# API-云接入-通用设备管理-设备添加与删除-生成设备配网二维码

> API-云接入-通用设备管理-设备添加与删除-生成设备配网二维码

> 更新时间: 2026-05-25T16:38:03.000+08:00

> 文档ID: 663 | 来源树: OPEN_API

---

## 生成设备配网二维码

- 接口功能

  该接口用于生成设备扫描配网二维码二进制数据，需要自行转换成图片（300x300像素大小）。
- 请求地址

  `https://open.ys7.com/api/lapp/device/wifi/qrcode`
- 请求方式

  `POST`
- 子账户token请求所需最小权限

  `"Permission":"Config"` `"Resource":"Cam:序列号:通道号"`
- 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| accessToken | String | 授权过程获取的access\_token | Y |
| ssid | String | 路由器SSID，即WIFI名称，建议不要设置中文名称 | Y |
| password | String | WIFI密码 | Y |

- HTTP请求报文

```
POST /api/lapp/device/wifi/qrcode HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded
accessToken=at.0v1ksxnqdu5lxc2fak3ctbiq0r3269y9&ssid=8d6bi&password=Zhg%2C%2C222
```

- 返回数据

```
{
    "data": {
        "imageData": "/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQK5nxd/y5/8D/8AZaKK5cH/\r\nAB4/P8j3eJP+RXV/7d/9KRzNFFFe6flR6ZRRRXzJ+4hRRRQAV5nRRXp5d9r5fqfDcZ/8uP8At7/2\r\n0K6bwj/y+f8AAP8A2aiiunGfwJfL8zw+G/8AkaUv+3v/AElnTUUUV4Z+qhRRRQAUUUUAFFFFABXM\r\n+Lv+XP8A4H/7LRRXTg/48fn+R4fEn/Irq/8Abv8A6UjmaKKK90/KgooooAKKKKAP/9k=\r\n"
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| imageData | String | 生成的二维码二进制数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 10017 | appKey不存在 | 确认appKey是否正确 |
| 49999 | 数据异常 | 接口调用异常 |

- 说明

1、目前只有部分设备支持扫描配网二维码进行配网的功能，请确定您要添加的设备在以下支持功能的设备型号（设备型号可在设备底座标签上看到）列表中：

| 设备型号 |
| --- |
| CS-C2C-31WFR-B |
| CS-C2miniS-52WFR |
| CS-C2W-31WPFR |
| CS-C6T-32WMFR |
| CS-F2-31WFSRT |

2、该接口获取的是二维码图片二进制数据，生成图片需要将该二进制数据转换为图片，以下提供JAVA转换示例代码（存储到本地）：

```
package com.ys7.open;

import sun.misc.BASE64Decoder;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;

public class TestQRCode {
    static String data = "/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQK5nxd/y5/8D/8AZaKK5cH/\r\nAB4/P8j3eJP+RXV/7d/9KRzNFFFe6flR6ZRRRXzJ+4hRRRQAV5nRRXp5d9r5fqfDcZ/8uP8At7/2\r\n0K6bwj/y+f8AAP8A2aiiunGfwJfL8zw+G/8AkaUv+3v/AElnTUUUV4Z+qhRRRQAUUUUAFFFFABXM\r\n+Lv+XP8A4H/7LRRXTg/48fn+R4fEn/Irq/8Abv8A6UjmaKKK90/KgooooAKKKKAP/9k=\r\n";
    static BASE64Decoder decoder = new sun.misc.BASE64Decoder();

    public static void main(String[] args) throws Exception {
        base64StringToImage(data);
    }

    /**
     * 将二进制转换为图片
     *
     * @param base64String
     */
    static void base64StringToImage(String base64String) {
        try {
            byte[] bytes1 = decoder.decodeBuffer(base64String);
            ByteArrayInputStream bais = new ByteArrayInputStream(bytes1);
            BufferedImage bi1 = ImageIO.read(bais);
            File file = new File("D://QRCode.jpg");// 指定图片存储路径、图片名称和格式
            ImageIO.write(bi1, "jpg", file);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

3、接口获取的二维码二进制数据，可以直接写入HTML的img标签中，例如：

```
<img src="data:image/jpg;base64,...">  /*...填写生成的图片二进制数据即可*/
```