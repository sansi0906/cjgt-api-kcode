# Backend 缺陷列表 (backend_bug / xfail)

共 32 个缺陷，均已用 `@pytest.mark.backend_bug` + `@pytest.mark.xfail` 标记，待后端修复后自动转为通过。

## 1. 参数校验缺失（必填项 / 取值范围未校验）

| # | 模块 | 用例 | 接口 | 缺陷描述 | 预期 | 实际 |
|---|------|------|------|----------|------|------|
| 1 | OCR | test_ocr_should_validate_required_params | /platform/ocr/\*, /api/ocr/\* | 缺少图片参数时未做必填校验 | 返回 01000006 | 返回系统异常 02 |
| 2 | 平台用户 | test_save_should_require_role_group_id | /platform/user/save | roleGroupId 缺失时仍创建成功 | 返回 01000006 | 返回成功 |
| 3 | 平台用户 | test_save_should_reject_unknown_role_group | /platform/user/save | roleGroupId 不存在时仍创建成功 | 校验失败 | 返回成功 |
| 4 | 平台用户 | test_change_status_should_reject_invalid_status | /platform/user/changeStatus | 非法 status 值(2)未校验 | 校验失败 | 返回成功 |
| 5 | 平台用户 | test_change_status_should_reject_unknown_user | /platform/user/changeStatus | 不存在的用户ID仍返回成功 | 校验失败 | 返回成功 |
| 6 | 平台用户 | test_delete_should_reject_unknown_user | /platform/user/delete | 不存在的用户ID仍返回成功 | 校验失败 | 返回成功 |
| 7 | 角色管理 | test_save_should_reject_invalid_status | /common/role/save | status 非法取值(5)未校验 | 校验失败 | 返回成功 |
| 8 | 角色管理 | test_change_status_should_reject_invalid_status | /common/role/changeStatus | status 取值未校验(2) | 校验失败 | 返回成功 |
| 9 | 角色管理 | test_change_status_should_require_status | /common/role/changeStatus | 缺少 status 时仍返回成功 | 返回 01000006 | 返回成功 |
| 10 | 角色管理 | test_delete_should_reject_unknown_role | /common/role/delete | 不存在的角色ID仍返回成功 | 校验失败 | 返回成功 |
| 11 | 角色管理 | test_edit_should_report_unknown_role | /common/role/edit | 不存在的角色ID返回错误提示 | 返回“角色不存在” | 返回“角色名称已存在” |
| 12 | 服务项目 | test_add_should_reject_invalid_billing_method | /platform/serviceItem/add | billingMethod 非法取值(5)未校验 | 校验失败 | 返回成功 |
| 13 | 服务项目 | test_add_should_reject_duplicate_name | /platform/serviceItem/add | 服务项目名称重复未校验 | 校验失败 | 返回成功 |
| 14 | 服务项目 | test_update_status_should_reject_invalid_is_display | /platform/serviceItem/updateStatus | isDisplay 非法取值(9)未校验 | 校验失败 | 返回成功 |
| 15 | 服务项目 | test_edit_unknown_item_error_message | /platform/serviceItem/edit | 不存在的项目ID错误文案不对 | 应为“服务项目不存在” | 返回“菜单不存在” |
| 16 | 服务项目 | test_update_status_unknown_item_error_message | /platform/serviceItem/updateStatus | 不存在的项目ID错误文案不对 | 应为“服务项目不存在” | 返回“菜单不存在” |
| 17 | 合同配置 | test_save_should_require_content | /platform/contactConfig/save | content 缺失时未做必填校验 | 返回 01000006 | 返回系统异常 02 |
| 18 | 登录 | test_login_password_mode_without_sms_code | /sys/login | smsCode OpenAPI 标记必填但后端未校验 | 返回失败 | 返回成功（契约偏差） |

## 2. 不存在的资源ID未校验（应返回失败，实际返回成功）

| # | 模块 | 用例 | 接口 | 缺陷描述 |
|---|------|------|------|----------|
| 19 | 登出 | test_logout_without_token | /sys/logout | 无 Token 登出，应返回失败，实际返回成功 code:00 |
| 20 | 登出 | test_logout_with_invalid_token | /sys/logout | 无效 Token 登出，应返回失败，实际返回 02（系统繁忙） |
| 21 | 菜单 | test_delete_should_reject_unknown_id | /common/menu/del | 不存在的菜单ID仍返回成功 |
| 22 | 定价 | test_tree_should_reject_unknown_service_item | /platform/pricing/tree | 不存在的服务项目ID仍返回成功 |
| 23 | 服务商 | test_change_status_should_reject_unknown_id | /platform/serverUser/changeStatus | 不存在的服务商ID仍返回成功 |
| 24 | 服务商 | test_delete_should_reject_unknown_id | /platform/serverUser/delete | 不存在的服务商ID仍返回成功 |
| 25 | 知识库 | test_change_status_should_reject_unknown_id | /platform/knowledge/changeStatus | 不存在的知识库ID仍返回成功 |
| 26 | 知识库 | test_delete_should_reject_unknown_id | /platform/knowledge/delete | 不存在的知识库ID仍返回成功 |
| 27 | 服务项目 | test_edit_should_reject_unknown_item | /platform/serviceItem/edit | 编辑不存在的项目应返回失败（注意：此用例未标 backend_bug，已通过） |
| 28 | 服务项目 | test_update_status_should_reject_unknown_item | /platform/serviceItem/updateStatus | 切换不存在项目状态应返回失败（注意：此用例未标 backend_bug，已通过） |

> 注：用例 27、28 已通过（未标 backend_bug），列于此仅作对照，非缺陷。

## 3. 错误文案不正确

| # | 模块 | 用例 | 接口 | 缺陷描述 | 预期文案 | 实际文案 |
|---|------|------|------|----------|----------|----------|
| 29 | 服务商 | test_detail_unknown_id_error_message | /platform/serverUser/detail | 不存在的服务商错误文案不对 | “服务商不存在” | “用户不存在或状态失效” |

## 4. 接口行为异常（返回系统异常 / 状态码不对）

| # | 模块 | 用例 | 接口 | 缺陷描述 | 预期 | 实际 |
|---|------|------|------|----------|------|------|
| 30 | 公共 | test_platform_home_should_reject_post | /platform/home | GET 接口用 POST 调用，应返回 405 | 返回 405 | 返回系统异常 02 |
| 31 | 定价 | test_import_pricing_excel | /platform/pricing/import | 导入服务定价 Excel 返回系统异常 | 返回成功 | 返回系统异常 02 |
| 32 | 工人乐 | test_gongrenle_info_should_return_data | /api/worker-sign/gongrenle-info | 查询用户详情返回系统异常 | 返回成功 | 返回系统异常 02 |
| 33 | 工人乐 | test_station_detail_should_return_data | /api/worker-sign/gongrenle-station-detail | 查询驿站详情返回系统异常 | 返回成功 | 返回系统异常 02 |
| 34 | 服务项目 | test_paging_should_support_time_range | /platform/serviceItem/paging | 带创建时间区间查询返回系统异常 | 返回成功 | 返回系统异常 02 |

## 缺陷分布（按模块）

| 模块 | 缺陷数 |
|------|--------|
| service_item_module | 6 |
| role_management_module | 5 |
| platform_user_module | 5 |
| service_provider_module | 3 |
| login_module | 2 |
| knowledge_base_module | 2 |
| pricing_module | 2 |
| worker_sign_module | 2 |
| contact_config_module | 1 |
| ocr_module | 1 |
| menu_module | 1 |
| common_module | 1 |
| server_module | 0 |
| 合计 | 32 |

## 备注

- 所有缺陷用例均标记 `@pytest.mark.xfail` + `@pytest.mark.backend_bug`，后端修复后用例会自动由 xfail 转为 passed。
- `test_login_password_mode_without_sms_code` 同时标记 `@pytest.mark.skip`（短信环境限制）与 `@pytest.mark.backend_bug`。
- `test_logout_without_token` 同样标记 `@pytest.mark.xfail` + `@pytest.mark.backend_bug`。
- `test_contact_config_*` 模块此前有 6 个执行失败（非 xfail），属于 contact_config_module 的回归失败，与 backend_bug 缺陷不同类别。
