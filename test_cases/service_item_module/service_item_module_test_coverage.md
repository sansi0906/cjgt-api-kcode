# 服务项目配置管理模块接口测试覆盖用例

> 生成时间：2026-08-12
> 测试环境：http://172.16.1.165:9200
> 数据库：MySQL 172.16.1.163 (test_cjgt) / PostgreSQL 172.16.1.165 (cjgt)

## test_service_item.py

| 测试用例 | 说明 |
|----------|------|
| test_add_service_item_success | 使用有效参数新增服务项目，应返回成功，并验证 PostgreSQL 数据库数据一致性及定价初始化 |
| test_add_service_item_missing_name | 缺少 itemName，应返回失败 |
| test_add_service_item_name_too_long | itemName 超过10个字符，应返回失败 |
| test_page_service_items_success | 正常分页查询服务项目，应返回成功 |
| test_page_service_items_by_name | 按服务项目名称模糊查询，应返回匹配结果 |
| test_list_display_service_items | 获取展示状态的服务项目列表，应返回成功 |
| test_list_display_service_items_filter | 按展示状态筛选服务项目列表 |
| test_update_status_disable | 禁用已启用的服务项目，应返回成功 |
| test_update_status_enable | 启用已禁用的服务项目，应返回成功 |
| test_edit_service_item_success | 使用有效参数编辑服务项目，应返回成功，并验证 PostgreSQL 数据库数据与入参一致 |
| test_edit_service_item_missing_name | 缺少 itemName，应返回失败 |
| test_edit_service_item_missing_id | 编辑服务项目缺少 id，应返回失败 |
| test_edit_service_item_missing_billing_method | 编辑服务项目缺少 billingMethod，应返回失败 |
| test_add_service_item_missing_billing_method | 新增服务项目缺少 billingMethod，应返回失败 |
| test_add_service_item_missing_item_name | 新增服务项目缺少 itemName，应返回失败 |
| test_add_service_item_yearly_billing | 使用按年计费(billingMethod=2)新增服务项目，应返回成功 |
| test_add_service_item_invalid_billing_method_zero | 使用无效计费方式(billingMethod=0)，应返回失败 |
| test_add_service_item_invalid_billing_method_overflow | 使用超出范围计费方式(billingMethod=99)，应返回失败 |
| test_update_status_missing_id | 切换服务项目展示状态缺少 id，应返回失败 |
| test_update_status_missing_is_display | 切换服务项目展示状态缺少 isDisplay，应返回失败 |
| test_add_service_item_subtitle_too_long | subtitle 超过100个字符，应返回失败 |
| test_add_service_item_desc_too_long | itemDesc 超过2000个字符，应返回失败 |
| test_edit_service_item_invalid_billing_method_zero | 编辑服务项目使用 billingMethod=0，应返回失败 |
| test_edit_service_item_invalid_billing_method_overflow | 编辑服务项目使用 billingMethod=99，应返回失败 |
| test_page_service_items_by_billing_method | 按 billingMethod 筛选服务项目，应返回匹配结果 |
| test_page_service_items_negative_page_num | 使用负数页码，应返回失败或空结果 |
| test_page_service_items_zero_page_size | 使用 pageSize=0，应返回失败或空结果 |
| test_page_service_items_by_is_display | 按 isDisplay 筛选服务项目，应返回匹配结果 |
| test_update_status_zero_id | 使用 id=0 切换状态，应返回失败 |
| test_update_status_negative_id | 使用负数 id 切换状态，应返回失败 |
| test_update_status_invalid_is_display_two | 使用 isDisplay=2 切换状态，应返回失败 |
| test_update_status_invalid_is_display_negative | 使用 isDisplay=-1 切换状态，应返回失败 |

## 统计

- 测试文件数：1
- 测试用例数：32

### 覆盖接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/platform/serviceItem/add` | POST | 新增服务项目 |
| `/platform/serviceItem/edit` | POST | 编辑服务项目 |
| `/platform/serviceItem/paging` | POST | 分页查询服务项目 |
| `/platform/serviceItem/updateStatus` | POST | 修改服务项目展示状态 |
| `/platform/serviceItem/listDisplay` | POST | 获取展示状态的服务项目列表 |

### 数据库验证

- `test_add_service_item_success`：验证 PostgreSQL `cjgt_service_item` 数据一致性及 `cjgt_service_pricing` 定价初始化
- `test_edit_service_item_success`：验证 PostgreSQL `cjgt_service_item` 编辑后数据与入参一致

### 已发现后端 Bug

- billingMethod 范围校验缺失：`0`/`99` 均可保存成功
- subtitle 超长校验缺失：>100 字符仍保存成功
- itemDesc 超长校验缺失：>2000 字符仍保存成功
- pageNum 负数校验缺失：`-1` 仍返回成功
- pageSize=0 校验缺失：返回空结果但未报错
- isDisplay 范围校验缺失：`2`/`-1` 仍保存成功
