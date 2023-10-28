## search_api_development
用户输入词查询商品项目API

## 环境部署
1.部署的时候需要在环境上修改配置文件
- ops.conf： 文件中配置使用数据库的连接信息 
- 
2.需要将商品文件先存入es，创建索引：product_basic_index
- 字段： "title", "description", "sku_id"
- 示例
```buildoutcfg
PUT /product_basic_index/_bulk
{ "index": { "_id": "sku_id_001" } }
{ "title": "商品名称001", "description": "这是第一个商品.", "sku_id":"sku_id_001"}
{ "index": { "_id": "sku_id_002" } }
{ "title": "商品名称002", "description": "这是第二个商品.", "sku_id":"sku_id_002" }
{ "index": { "_id": "sku_id_003" } }
{ "title": "商品名称003", "description": "这是第三个商品.", "sku_id":"sku_id_003" }
```
3.采用jieba对用户输入词分词

4.采用redis缓存用户查询次数

## 请求示例
1.接口
- http://localhost:5000/rs/rc/product_search/1.0.0.0

2.参数
```
{
    "user_id":"sdhkhuiasydiuashhk",
    "search_key":"商品名称001",
    "size":10,
    "extra":{}
}
```
3. 返回值
```
{
    "code": 0,
    "data": [
        {
            "extra": {
                "description": "这是第三个商品.",
                "title": "商品名称003"
            },
            "rec_id": "sku_id_003",
            "rec_type": "",
            "res_type": null,
            "score": 1
        }
    ],
    "msg": "查询成功",
    "status": 0,
    "success": true
}
```
