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

