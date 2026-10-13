# 合同服务配置管理模块接口测试覆盖用例

> 生成时间：2026-08-12
> 测试环境：http://172.16.1.165:9200
> 数据库：MySQL 172.16.1.163 (test_cjgt) / PostgreSQL 172.16.1.165 (cjgt)

## test_agreement.py

| 测试用例 | 说明 |
|----------|------|
| test_page_agreements_success | 正常分页查询协议列表，应返回成功 |
| test_get_agreement_detail_existing | 查询已存在的协议详情，应返回成功 |
| test_get_agreement_detail_non_existing | 查询不存在的协议详情，应返回失败 |
| test_get_agreement_detail_missing_id | 缺少ID查询详情，应返回失败 |
| test_edit_agreement_success | 正常编辑协议，应返回成功 |

## test_contact_config.py

| 测试用例 | 说明 |
|----------|------|
| test_save_contact_config_success | 使用有效参数创建合同配置（关联服务项目），应返回成功 |
| test_save_contact_config_missing_service_item_id | 缺少 serviceItemId，应返回失败 |
| test_save_contact_config_missing_title | 缺少 title，应返回失败 |
| test_save_contact_config_invalid_service_item_id | 无效服务项目ID，应返回失败 |
| test_save_contact_config_duplicate_1to1 | 同一服务项目创建多个合同配置（违反1:1关系），应返回失败 |
| test_page_contact_configs_success | 正常分页查询合同配置，应返回成功 |
| test_page_contact_configs_by_service_item_id | 按服务项目ID查询合同配置，应返回成功 |
| test_get_contact_config_detail_existing | 查询已存在的合同配置详情，应返回成功 |
| test_get_contact_config_detail_non_existing | 查询不存在的合同配置ID，应返回失败 |
| test_edit_contact_config_success | 正常编辑合同配置，应返回成功 |
| test_edit_contact_config_not_exist | 编辑不存在的合同配置，应返回失败 |
| test_delete_contact_config_success | 正常删除合同配置，应返回成功 |
| test_delete_contact_config_non_existing | 删除不存在的合同配置，应返回失败 |

## test_contract.py

| 测试用例 | 说明 |
|----------|------|
| test_page_contracts_success | 正常分页查询合同列表，应返回成功 |
| test_page_contracts_by_contact_no | 按合同编号模糊查询，应返回成功 |
| test_page_contracts_by_party_a_name | 按甲方名称查询，应返回成功 |
| test_page_contracts_invalid_page_num | 无效页码（0），应返回失败 |
| test_page_contracts_large_page_size | 超大每页条数（1000），应返回失败 |

## 统计

- 测试文件数：4
- 测试用例数：23

### 覆盖接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/platform/contactConfig/save` | POST | 保存合同配置（合同服务配置） |
| `/platform/contactConfig/paging` | POST | 分页查询合同配置 |
| `/platform/contactConfig/detail` | POST | 查询合同配置详情 |
| `/platform/contactConfig/edit` | POST | 编辑合同配置 |
| `/platform/contactConfig/delete` | POST | 删除合同配置 |
| `/platform/contract/page` | POST | 分页查询合同列表 |
| `/platform/agreement/page` | POST | 分页查询协议列表 |
| `/platform/agreement/detail` | POST | 查询协议详情 |
| `/platform/agreement/edit` | POST | 编辑协议 |

### 关联关系

- 合同配置（合同服务配置）与服务项目配置为 **1:1 关联** 关系
- 创建合同配置前需先创建服务项目
- 一个服务项目只能有一个合同配置
