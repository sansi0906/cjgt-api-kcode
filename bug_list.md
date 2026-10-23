# 后端 Bug 列表

> 依据：http://172.16.1.165:9200/doc.html#/home  
> 测试时间：2026-07-31  
> 测试环境：E:\GrlApiTest  
> 测试套件：217 passed, 19 failed（含 10 个安全漏洞 + 8 个后端 Bug + 1 个环境限制）

---

## 1. 必填项校验 Bug

### Bug 1-1：保存用户时缺少 status 必填项，后端未校验

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/user/save |
| **入参** | `{"userName": "174xxxxxxxx", "realName": "测试用户", "sex": 1, "roleGroupId": 5, "status": null}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | OpenAPI 规范中 `PlatformUserSaveReqDto` 标记 `status` 为必填项，但传 `null` 时后端未做校验，返回成功 code:00 |

### Bug 1-2：区域定价树查询缺少 areaList 必填项，后端未校验

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/pricing/treeByAreas |
| **入参** | `{"serviceItemId": 1, "areaList": null}` |
| **出参** | `{"code": "00", "message": "成功", "data": {"serviceItemId": "151", "serviceItemName": null, "servicePricingTree": []}}` |
| **Bug描述** | OpenAPI 规范中 `ServicePricingAreaTreeQueryReqDto` 标记 `areaList` 为必填项，但传 `null` 时后端未做校验，返回成功 code:00 |

### Bug 1-3：密码登录模式下缺少 smsCode 必填项，后端未校验

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /sys/login |
| **入参** | `{"username": "admin", "password": "xxxx", "loginType": 1, "webType": 0, "smsCode": null}` |
| **出参** | `{"code": "00", "message": "成功", "data": {"token": "xxx"}}` |
| **Bug描述** | OpenAPI 规范中 `LoginReqDto` 标记 `smsCode` 为必填项，但密码登录模式下传 `null` 时后端未做校验，返回成功 code:00 |

---

## 2. 存在性校验 Bug（删除/编辑/改状态未校验记录是否存在）

### Bug 2-1：删除不存在的用户，返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/user/delete |
| **入参** | `{"id": 999999}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 删除用户前未校验用户是否存在，传入不存在的 ID 999999 返回成功 code:00，预期应返回失败 |

### Bug 2-2：编辑不存在的用户，返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/user/edit |
| **入参** | `{"id": 999999, "userName": "174xxxxxxxx", "realName": "测试用户", "sex": 1, "roleGroupId": 5, "status": 1}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 编辑用户前未校验用户是否存在，传入不存在的 ID 999999 返回成功 code:00，预期应返回失败 |

### Bug 2-3：修改不存在的用户状态，返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/user/changeStatus |
| **入参** | `{"id": 999999, "status": 0}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 修改用户状态前未校验用户是否存在，传入不存在的 ID 999999 返回成功 code:00，预期应返回失败 |

### Bug 2-4：删除不存在的服务商，返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/serverUser/delete |
| **入参** | `{"id": 999999}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 删除服务商前未校验服务商是否存在，传入不存在的 ID 999999 返回成功 code:00，预期应返回失败 |

### Bug 2-5：删除不存在的知识库，返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/knowledge/delete |
| **入参** | `{"id": 999999}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 删除知识库前未校验知识库是否存在，传入不存在的 ID 999999 返回成功 code:00，预期应返回失败 |

---

## 3. 接口逻辑 Bug

### Bug 3-1：经营范围详情接口对所有 ID 返回 404

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/businessScope/detail |
| **入参（存在的 ID）** | `{"id": 1}` |
| **出参** | HTTP 404 / `{"code": "03", "message": "服务不存在", "data": null}` |
| **Bug描述** | detail 接口对所有 ID（包括数据库中存在的 ID）均返回 HTTP 404 或 code:03，属于后端查询逻辑 Bug |

### Bug 3-2：无 Token 登出返回成功

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /sys/logout |
| **入参** | 无 Token 请求头 |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 登出接口未校验 Token，无 Token 时返回成功 code:00，预期应返回认证失败 |

---

## 4. 安全漏洞（SQL 注入 / XSS）

### Bug 4-1：知识库标题存在 SQL 注入漏洞

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/knowledge/save |
| **入参** | `{"title": "' OR '1'='1", "content": "TestContent", "consultType": 1, "displayPosition": [0, 1], "applicableArea": [...]}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 知识库 title 字段未过滤 SQL 注入 payload，后端接受并返回成功，存在 SQL 注入风险 |

### Bug 4-2：知识库标题存在 XSS 漏洞

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/knowledge/save |
| **入参** | `{"title": "<script>alert('xss')</script>", "content": "TestContent", ...}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 知识库 title 字段未过滤 XSS payload，后端接受并返回成功，存在 XSS 风险 |

### Bug 4-3：知识库内容存在 XSS 漏洞

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /platform/knowledge/save |
| **入参** | `{"title": "TestTitle", "content": "<script>alert('xss')</script>", ...}` |
| **出参** | `{"code": "00", "message": "成功", "data": null}` |
| **Bug描述** | 知识库 content 字段未过滤 XSS payload，后端接受并返回成功，存在 XSS 风险 |

---

## 5. 环境限制（非 Bug）

### 限制 5-1：短信发送每日上限

| 项目 | 内容 |
|------|------|
| **请求地址** | POST /sys/sendCode |
| **入参** | `{"phone": "17695729351"}` |
| **出参** | `{"code": "01000044", "message": "the number of sms messages sent from a single mobile number every day exceeds the upper limit", "data": null}` |
| **说明** | 测试手机号 17695729351 当日发送短信次数超过系统上限，属于测试环境限制，非后端 Bug |

---

## Bug 汇总

| 类别 | Bug 数量 | 涉及接口 |
|------|----------|----------|
| 必填项校验 Bug | 3 | /platform/user/save, /platform/pricing/treeByAreas, /sys/login |
| 存在性校验 Bug | 5 | /platform/user/delete, /platform/user/edit, /platform/user/changeStatus, /platform/serverUser/delete, /platform/knowledge/delete |
| 接口逻辑 Bug | 2 | /platform/businessScope/detail, /sys/logout |
| 安全漏洞（SQL 注入 / XSS） | 3 | /platform/knowledge/save |
| **后端 Bug 总计（旧）** | **13** | - |
| 环境限制 | 1 | /sys/sendCode |

---

## 6. 接口契约校验缺陷（来自 *_contract.py，共 35 个，标记 backend_bug/xfail）

> 这些缺陷通过 pytest `@pytest.mark.xfail` + `@pytest.mark.backend_bug` 标记，后端修复后用例将自动转为通过。

### 6.1 平台用户管理（5 个）— /platform/user/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-1 | test_save_should_require_role_group_id | POST /platform/user/save | roleGroupId 缺失时仍创建成功（Swagger 标记必填） |
| 6-2 | test_save_should_reject_unknown_role_group | POST /platform/user/save | roleGroupId 不存在时仍创建成功 |
| 6-3 | test_change_status_should_reject_invalid_status | POST /platform/user/changeStatus | status 非法取值（2）未校验 |
| 6-4 | test_change_status_should_reject_unknown_user | POST /platform/user/changeStatus | 不存在的用户 ID 仍返回成功 |
| 6-5 | test_delete_should_reject_unknown_user | POST /platform/user/delete | 不存在的用户 ID 仍返回成功 |

### 6.2 角色管理（5 个）— /common/role/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-6 | test_save_should_reject_invalid_status | POST /common/role/save | status 非法取值（5）未校验 |
| 6-7 | test_change_status_should_reject_invalid_status | POST /common/role/changeStatus | status 非法取值（2）未校验 |
| 6-8 | test_change_status_should_require_status | POST /common/role/changeStatus | 缺少 status 时仍返回成功 |
| 6-9 | test_delete_should_reject_unknown_role | POST /common/role/delete | 不存在的角色 ID 仍返回成功 |
| 6-10 | test_edit_should_report_unknown_role | POST /common/role/edit | 不存在的角色 ID 返回错误文案“角色名称已存在” |

### 6.3 服务项目配置（6 个）— /platform/serviceItem/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-11 | test_add_should_reject_invalid_billing_method | POST /platform/serviceItem/add | billingMethod 非法取值（5）未校验 |
| 6-12 | test_add_should_reject_duplicate_name | POST /platform/serviceItem/add | 服务项目名称重复未校验 |
| 6-13 | test_update_status_should_reject_invalid_is_display | POST /platform/serviceItem/updateStatus | isDisplay 非法取值（9）未校验 |
| 6-14 | test_edit_unknown_item_error_message | POST /platform/serviceItem/edit | 不存在的项目 ID 错误文案为“菜单不存在” |
| 6-15 | test_update_status_unknown_item_error_message | POST /platform/serviceItem/updateStatus | 不存在的项目 ID 错误文案为“菜单不存在” |
| 6-16 | test_paging_should_support_time_range | POST /platform/serviceItem/paging | 带创建时间区间时后端返回系统异常(02) |

### 6.4 服务商管理（3 个）— /platform/serverUser/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-17 | test_change_status_should_reject_unknown_id | POST /platform/serverUser/changeStatus | 不存在的服务商 ID 仍返回成功 |
| 6-18 | test_delete_should_reject_unknown_id | POST /platform/serverUser/delete | 不存在的服务商 ID 仍返回成功 |
| 6-19 | test_detail_unknown_id_error_message | POST /platform/serverUser/detail | 不存在的服务商返回错误文案“用户不存在或状态失效” |

### 6.5 公共接口（1 个）— /platform/home

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-20 | test_platform_home_should_reject_post | POST /platform/home | GET 接口被 POST 调用返回系统异常(02)，应返回 405 |

### 6.6 合同服务配置（1 个）— /platform/contactConfig/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-21 | test_save_should_require_content | POST /platform/contactConfig/save | content 缺失时未做必填校验，返回系统异常(02) |

### 6.7 知识库管理（2 个）— /platform/knowledge/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-22 | test_change_status_should_reject_unknown_id | POST /platform/knowledge/changeStatus | 不存在的知识库 ID 仍返回成功 |
| 6-23 | test_delete_should_reject_unknown_id | POST /platform/knowledge/delete | 不存在的知识库 ID 仍返回成功 |

### 6.8 用户登出（1 个）— /sys/logout

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-24 | test_logout_without_token | POST /sys/logout | 无 Token 登出仍返回成功（未做 Token 校验） |

### 6.9 菜单管理（1 个）— /common/menu/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-25 | test_delete_should_reject_unknown_id | POST /common/menu/del | 不存在的菜单 ID 仍返回成功 |

### 6.10 OCR 识别（6 个）— /platform/ocr/*, /api/ocr/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-26 | test_ocr_should_validate_required_params | POST /platform/ocr/lic | 缺少图片参数时返回系统异常(02)，应返回 01000006 |
| 6-27 | test_ocr_should_validate_required_params | POST /platform/ocr/idCardFront | 缺少图片参数时返回系统异常(02)，应返回 01000006 |
| 6-28 | test_ocr_should_validate_required_params | POST /platform/ocr/idCardBack | 缺少图片参数时返回系统异常(02)，应返回 01000006 |
| 6-29 | test_ocr_should_validate_required_params | POST /api/ocr/lic | 缺少图片参数时返回系统异常(02)，应返回 01000006 |
| 6-30 | test_ocr_should_validate_required_params | POST /api/ocr/idCardFront | 缺少图片参数时返回系统异常(02)，应返回 01000006 |
| 6-31 | test_ocr_should_validate_required_params | POST /api/ocr/idCardBack | 缺少图片参数时返回系统异常(02)，应返回 01000006 |

### 6.11 服务定价（2 个）— /platform/pricing/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-32 | test_tree_should_reject_unknown_service_item | POST /platform/pricing/tree | 不存在的服务项目 ID 仍返回成功 |
| 6-33 | test_import_pricing_excel | POST /platform/pricing/import | 导入服务定价 Excel 返回系统异常(02) |

### 6.12 超级个体入驻（2 个）— /api/worker-sign/*

| 序号 | 用例 | 接口 | 缺陷描述 |
|------|------|------|----------|
| 6-34 | test_gongrenle_info_should_return_data | GET /api/worker-sign/gongrenle-info | 返回系统异常(02) |
| 6-35 | test_station_detail_should_return_data | GET /api/worker-sign/gongrenle-station-detail | 返回系统异常(02) |

## 契约缺陷汇总

| 模块 | 缺陷数量 |
|------|----------|
| 平台用户管理 | 5 |
| 角色管理 | 5 |
| 服务项目配置 | 6 |
| 服务商管理 | 3 |
| 公共接口 | 1 |
| 合同服务配置 | 1 |
| 知识库管理 | 2 |
| 用户登出 | 1 |
| 菜单管理 | 1 |
| OCR 识别 | 6 |
| 服务定价 | 2 |
| 超级个体入驻 | 2 |
| **合计** | **35** |

## 总计

| 类别 | Bug 数量 |
|------|----------|
| 旧后端 Bug | 13 |
| 接口契约校验缺陷 | 35 |
| **所有后端缺陷总计** | **48** |
| 环境限制 | 1 |
