# API-设备云组件仓-执法记录仪-远程巡检组件-工地管理-修改工地

>  

> 更新时间: 2026-06-30T11:48:06.000+08:00

> 文档ID: 1534 | 来源树: OPEN_API

---

## 修改工地

- 接口功能

   设备、巡检记录等信息可在工地下进行相关管理及统计。其中工地相关信息（工地名称、工地位置、工地范围、工地备注信息）均支持进行二次编辑。

- 请求地址

`https://open.ys7.com/api/service/devicekit/common/worksite`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| body | worksiteId | String | 工地id，自动分配，不可修改 | Y |
| body | worksiteName | String | 工地名称 | N |
| body | longitude | Float | 工地定位-工地经度，用于标识工地的位置经度，支持小数点后六位，不传默认为0，示例：116.263379 | N |
| body | latitude | Float | 工地定位-工地纬度，用于标识工地的位置纬度，支持小数点后六位，不传默认为0，示例：40.2273 | N |
| body | worksiteRegion | String | 工地区域，用于划定工地区域范围，起点和终点经纬度相同，经纬度之间逗号分隔，点与点之间分号分隔(建议至少输入三个及以上不同点)，示例：-120.123,46.33;-120.30,45.33;-120.45,45.27;-120.123,46.33 | N |
| body | note | String | 备注 | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/common/worksite' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"worksiteId":"07b7ef7a815f40e08d89b86da392b138","worksiteName":"工地1","longitude":116.263379,"latitude":40.2273,"worksiteRegion":"-120.123,46.33;-120.30,45.33;-120.45,45.27;-120.123,46.33","note":"备注"}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交[工单](https://open.ys7.com/console/work.html)解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |