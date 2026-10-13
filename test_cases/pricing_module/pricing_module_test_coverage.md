# 服务定价配置管理模块接口测试覆盖用例

> 生成时间：2026-08-12
> 测试环境：http://172.16.1.165:9200
> 数据库：MySQL 172.16.1.163 (test_cjgt)

## test_pricing.py

| 测试用例 | 说明 |
|----------|------|
| test_import_pricing_success | 使用有效Excel文件导入服务定价数据 |
| test_get_pricing_tree_success | 获取已导入定价数据的服务项目定价树 |
| test_get_pricing_tree_no_data | 获取未导入定价数据的服务项目定价树，应返回空树 |
| test_get_pricing_tree_missing_id | 缺少 serviceItemId，应返回失败 |
| test_get_pricing_tree_by_areas_success | 根据区域列表获取服务定价树 |
| test_get_pricing_tree_by_areas_missing_id | 缺少 serviceItemId，应返回失败 |
| test_update_pricing_success | 更新已存在的服务项目定价 |
| test_update_pricing_no_record | 更新未导入定价数据的服务项目定价，按正常逻辑应返回失败 |
| test_update_pricing_missing_amount | 更新定价缺少 amount，应返回失败 |
| test_update_pricing_missing_area_list | 更新定价缺少 areaList，应返回失败 |
| test_update_pricing_missing_service_item_id | 更新定价缺少 serviceItemId，应返回失败 |
| test_get_pricing_tree_missing_service_item_id | 获取定价树缺少 serviceItemId，应返回失败 |
| test_get_pricing_tree_by_areas_missing_area_list | 根据区域获取定价树缺少 areaList，后端实际返回空树（必填校验不严格） |

## 统计

- 测试文件数：1
- 测试用例数：13

### 覆盖接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/platform/pricing/import` | POST | 导入服务定价数据 |
| `/platform/pricing/getPricingTree` | POST | 获取价格树 |
| `/platform/pricing/getPricingTreeByArea` | POST | 按区域获取价格树 |
| `/platform/pricing/updatePricing` | POST | 更新服务定价 |
