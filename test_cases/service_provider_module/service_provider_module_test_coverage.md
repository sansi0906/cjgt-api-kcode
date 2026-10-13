# 服务商管理模块测试用例覆盖文档

## 模块信息

- **模块路径**: `test_cases/service_provider_module/`
- **测试文件**: `test_service_provider.py`
- **基类文件**: `test_base.py`
- **用例总数**: 29 个
- **Smoke 用例**: 3 个
- **后端 Bug 标记**: 1 个

---

## 用例清单

| 序号 | 用例 ID | 用例名称 | 接口 | 场景 | 标记 |
|------|---------|----------|------|------|------|
| 1 | SP-001 | test_save_service_provider_success | `/platform/serverUser/save` | 使用标准参数新增服务商，按正常逻辑应返回成功 | smoke |
| 2 | SP-002 | test_save_service_provider_duplicate_name | `/platform/serverUser/save` | 使用重复的公司名称新增服务商，应返回失败 | |
| 3 | SP-003 | test_page_service_providers_success | `/platform/serverUser/page` | 正常分页查询服务商，应返回成功 | smoke |
| 4 | SP-004 | test_page_service_providers_by_name | `/platform/serverUser/page` | 按公司名称模糊查询服务商 | |
| 5 | SP-005 | test_get_provider_detail_existing | `/platform/serverUser/detail` | 获取已存在的服务商详情，应返回成功 | |
| 6 | SP-006 | test_get_provider_detail_non_existing | `/platform/serverUser/detail` | 获取不存在的服务商详情，应返回失败 | |
| 7 | SP-007 | test_edit_service_provider_success | `/platform/serverUser/edit` | 编辑已存在的服务商，应返回成功 | |
| 8 | SP-008 | test_edit_service_provider_missing_company_name | `/platform/serverUser/edit` | 编辑服务商缺少 companyName，应返回失败 | |
| 9 | SP-009 | test_edit_service_provider_missing_unified_social_code | `/platform/serverUser/edit` | 编辑服务商缺少 unifiedSocialCode，应返回失败 | |
| 10 | SP-010 | test_edit_service_provider_missing_office_address | `/platform/serverUser/edit` | 编辑服务商缺少 officeAddress，应返回失败 | |
| 11 | SP-011 | test_edit_service_provider_missing_service_area | `/platform/serverUser/edit` | 编辑服务商缺少 serviceArea，应返回失败 | |
| 12 | SP-012 | test_edit_service_provider_missing_contact_person | `/platform/serverUser/edit` | 编辑服务商缺少 contactPerson，应返回失败 | |
| 13 | SP-013 | test_edit_service_provider_missing_contact_phone | `/platform/serverUser/edit` | 编辑服务商缺少 contactPhone，应返回失败 | |
| 14 | SP-014 | test_edit_service_provider_missing_service_items | `/platform/serverUser/edit` | 编辑服务商缺少 serviceItems，应返回失败 | |
| 15 | SP-015 | test_change_status_disable | `/platform/serverUser/changeStatus` | 禁用已启用的服务商，应返回成功 | |
| 16 | SP-016 | test_change_status_enable | `/platform/serverUser/changeStatus` | 启用已禁用的服务商，应返回成功 | |
| 17 | SP-017 | test_reset_password_success | `/platform/serverUser/resetPwd` | 重置已存在的服务商密码，应返回成功 | |
| 18 | SP-018 | test_reset_password_non_existing | `/platform/serverUser/resetPwd` | 重置不存在的服务商密码，按正常逻辑应返回失败 | |
| 19 | SP-019 | test_delete_service_provider_success | `/platform/serverUser/delete` | 删除已存在的服务商，应返回成功 | |
| 20 | SP-020 | test_delete_service_provider_non_existing | `/platform/serverUser/delete` | 删除不存在的服务商，预期应返回失败，但后端实际返回成功（疑似未做存在性校验） | backend_bug |
| 21 | SP-021 | test_delete_service_provider_missing_id | `/platform/serverUser/delete` | 删除服务商缺少 id，应返回失败 | |
| 22 | SP-022 | test_detail_missing_id | `/platform/serverUser/detail` | 获取服务商详情缺少 id，应返回失败 | |
| 23 | SP-023 | test_change_status_missing_id | `/platform/serverUser/changeStatus` | 修改服务商状态缺少 id，应返回失败 | |
| 24 | SP-024 | test_change_status_missing_status | `/platform/serverUser/changeStatus` | 修改服务商状态缺少 status，应返回失败 | |
| 25 | SP-025 | test_reset_password_missing_id | `/platform/serverUser/resetPwd` | 重置服务商密码缺少 id，应返回失败 | |
| 26 | SP-026 | test_save_service_provider_missing_company_name | `/platform/serverUser/save` | 新增服务商缺少 companyName，应返回失败 | |
| 27 | SP-027 | test_save_service_provider_missing_unified_social_code | `/platform/serverUser/save` | 新增服务商缺少 unifiedSocialCode，应返回失败 | |
| 28 | SP-028 | test_save_service_provider_missing_office_address | `/platform/serverUser/save` | 新增服务商缺少 officeAddress，应返回失败 | |
| 29 | SP-029 | test_save_service_provider_missing_service_area | `/platform/serverUser/save` | 新增服务商缺少 serviceArea，应返回失败 | |
| 30 | SP-030 | test_save_service_provider_missing_contact_person | `/platform/serverUser/save` | 新增服务商缺少 contactPerson，应返回失败 | |
| 31 | SP-031 | test_save_service_provider_missing_contact_phone | `/platform/serverUser/save` | 新增服务商缺少 contactPhone，应返回失败 | |
| 32 | SP-032 | test_save_service_provider_missing_service_items | `/platform/serverUser/save` | 新增服务商缺少 serviceItems，应返回失败 | |

---

## 接口覆盖

| 接口路径 | 方法 | 用例数 | 覆盖场景 |
|----------|------|--------|----------|
| `/platform/serverUser/save` | POST | 7 | 新增成功、重名校验、6 个必填字段缺失 |
| `/platform/serverUser/page` | POST | 2 | 分页查询、按名称模糊查询 |
| `/platform/serverUser/detail` | POST | 2 | 查询已存在详情、查询不存在详情、缺少 id |
| `/platform/serverUser/edit` | POST | 8 | 编辑成功、7 个必填字段缺失 |
| `/platform/serverUser/changeStatus` | POST | 3 | 禁用、启用、缺少 id/status |
| `/platform/serverUser/resetPwd` | POST | 2 | 重置成功、重置不存在、缺少 id |
| `/platform/serverUser/delete` | POST | 4 | 删除成功、删除不存在(Bug)、缺少 id |

---

## 必填字段清单

根据用例分析，服务商管理接口的必填字段包括：

| 字段 | 类型 | 说明 |
|------|------|------|
| `companyName` | string | 公司名称 |
| `unifiedSocialCode` | string | 统一社会信用代码 |
| `officeAddress` | array | 办公地址（省市区结构） |
| `officeAddressDetail` | string | 办公地址详情 |
| `serviceArea` | array | 服务区域（省市区结构） |
| `contactPerson` | string | 联系人 |
| `contactPhone` | string | 联系电话 |
| `serviceItems` | array | 服务项目 ID 列表 |

---

## 已知后端 Bug

| Bug ID | 用例 | 问题描述 |
|--------|------|----------|
| BUG-XXX | SP-020 | 删除不存在的服务商，后端返回成功（code: 00），未做存在性校验 |

---

## 测试数据准备

- **服务商名称**: `测试服务商-{时间戳后4位}`（唯一）
- **手机号**: `174{8位随机数}`（唯一）
- **统一社会代码**: `9119XX{手机号}`
- **办公地址**: 延庆区（code: 110119000000）
- **服务区域**: 北京市（code: 110000000000）
- **服务项目**: 默认 [1]

---

## 执行说明

```bash
# 执行全部服务商模块测试
python -m pytest test_cases/service_provider_module/ -v --tb=short

# 执行 Smoke 用例
python -m pytest test_cases/service_provider_module/ -v -m smoke

# 执行单个用例
python -m pytest test_cases/service_provider_module/test_service_provider.py::TestServiceProvider::test_save_service_provider_success -v
```
