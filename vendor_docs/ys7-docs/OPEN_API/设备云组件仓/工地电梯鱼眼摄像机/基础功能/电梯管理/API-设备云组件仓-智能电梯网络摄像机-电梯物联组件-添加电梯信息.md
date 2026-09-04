# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-添加电梯信息

> 更新时间: 2026-06-30T11:54:40.000+08:00

> 文档ID: 1613 | 来源树: OPEN_API

---

## 添加电梯信息

- 接口功能

   录入电梯的各项信息，可在此过程中绑定相应的摄像头设备

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/info/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 绑定的设备序列号 | N |
| body | customSerial | String | 自定义电梯唯一编号 | N |
| body | elevatorNum | String | 电梯编号 | N |
| body | buildingNum | String | 电梯所属建筑物编号 | N |
| body | address | String | 详细地址 | N |
| body | elevatorType | String | 电梯类型：PASSENGER-乘客电梯，FREIGHT-载货电梯，ESCALATOR-自动扶梯，FIRE-消防员电梯，VILLA-别墅电梯 | Y |
| body | productModel | String | 电梯出厂产品型号 | N |
| body | productDate | String | 电梯出厂日期(yyyy-MM-dd) | N |
| body | propertyName | String | 物业姓名 | N |
| body | propertyPhone | String | 物业电话 | N |
| body | maintEnterprise | String | 维保企业名称 | N |
| body | maintName | String | 维保人员姓名 | N |
| body | maintPhone | String | 维保人员手机号 | N |
| body | maintCycle | Int | 维保周期 | N |
| body | useEnterprise | String | 使用企业 | N |
| body | worksiteId | String | 关联区域ID | Y |
| body | useStatus | String | 电梯使用状态：USING-在用，SCRAPPED-报废，DISABLED-停用，LOGOUT-注销 | Y |
| body | elevatorPersonsLimit | Int | 电梯载人上限(人) | N |
| body | elevatorLoadLimit | Int | 电梯载重上限(kg) | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/elevator/info/add' \
--header 'accessToken: at.xxxxx' \
--data-urlencode 'deviceSerial=AD2580467' \
--data-urlencode 'customSerial=123' \
--data-urlencode 'elevatorNum=12' \
--data-urlencode 'buildingNum=12' \
--data-urlencode 'address=海威市' \
--data-urlencode 'elevatorType=FREIGHT' \
--data-urlencode 'productModel=VT-120' \
--data-urlencode 'productDate=2022-01-10' \
--data-urlencode 'propertyName=绿城' \
--data-urlencode 'propertyPhone=95061877' \
--data-urlencode 'maintEnterprise=绿城' \
--data-urlencode 'maintName=王琳' \
--data-urlencode 'maintPhone=12345678' \
--data-urlencode 'maintCycle=30' \
--data-urlencode 'useEnterprise=融侨' \
--data-urlencode 'worksiteId=f2412cec91c4461a9f64fdc6b618e105' \
--data-urlencode 'useStatus=USING' \
--data-urlencode 'elevatorPersonsLimit=21' \
--data-urlencode 'elevatorLoadLimit=1000'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "elevatorSerial": "2dea4ab0051142eea09cd64853b6eb97"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Object | 响应体 |
| data.elevatorSerial | String | 电梯平台唯一标识，添加成功后由平台生成 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |