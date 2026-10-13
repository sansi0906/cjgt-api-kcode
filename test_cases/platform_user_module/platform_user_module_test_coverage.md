# 平台用户管理模块接口测试覆盖用例

> 生成时间：2026-08-12
> 测试环境：http://172.16.1.165:9200
> 数据库：MySQL 172.16.1.163 (test_cjgt)

## test_user_change_status.py

| 测试用例 | 说明 |
|----------|------|
| test_disable_existing_user | 禁用已启用的用户，应返回成功 |
| test_enable_existing_user | 启用已禁用的用户，应返回成功 |
| test_change_status_non_existing_user | 修改不存在的用户状态，预期应返回失败，但后端实际返回成功（疑似未做存在性校验） |
| test_change_status_missing_id | 缺少 id 字段，应返回失败 |
| test_change_status_missing_status | 缺少 status 字段，应返回失败 |

## test_user_delete.py

| 测试用例 | 说明 |
|----------|------|
| test_delete_existing_user | 删除已存在的用户，应返回成功 |
| test_delete_non_existing_user | 删除不存在的用户，预期应返回失败，但后端实际返回成功（疑似未做存在性校验） |
| test_delete_user_not_found_after_delete | 删除用户后，分页查询应不再返回该用户 |
| test_delete_missing_id | 缺少 id 字段，应返回失败 |

## test_user_detail.py

| 测试用例 | 说明 |
|----------|------|
| test_detail_existing_user | 获取已存在的用户详情，应返回成功并包含完整用户信息 |
| test_detail_non_existing_user | 获取不存在的用户详情，应返回失败 |
| test_detail_missing_id | 缺少 id 字段，应返回失败 |

## test_user_edit.py

| 测试用例 | 说明 |
|----------|------|
| test_edit_user_success | 使用有效参数编辑用户，应返回成功 |
| test_edit_user_not_exist | 编辑不存在的用户ID，预期应返回失败，但后端实际返回成功（疑似未做存在性校验） |
| test_edit_user_missing_real_name | 缺少 realName，应返回失败 |
| test_edit_user_invalid_phone | 使用无效手机号格式，应返回失败 |
| test_edit_user_change_status | 修改用户状态（启用/禁用），应返回成功 |
| test_edit_user_change_sex | 修改用户性别，应返回成功 |
| test_edit_user_missing_id | 缺少 user_id，应返回失败 |
| test_edit_user_missing_user_name | 缺少 userName，应返回失败 |
| test_edit_user_missing_status | 缺少 status，应返回失败 |
| test_edit_user_missing_real_name | 缺少 realName，应返回失败 |
| test_edit_user_missing_role_group_id | 缺少 roleGroupId，应返回失败 |
| test_edit_user_missing_sex | 缺少 sex，应返回失败 |

## test_user_page.py

| 测试用例 | 说明 |
|----------|------|
| test_page_users_success | 正常分页查询，应返回成功 |
| test_page_users_by_user_name | 按用户名模糊查询，应返回匹配结果 |
| test_page_users_by_role_group_id | 按角色组ID筛选，应返回匹配结果 |
| test_page_users_by_status | 按状态筛选（启用），应返回匹配结果 |
| test_page_users_invalid_page_num | 使用无效页码（0），应返回失败或空结果 |
| test_page_users_large_page_size | 使用超大每页条数（超过100），应返回失败或限制结果 |

## test_user_reset_pwd.py

| 测试用例 | 说明 |
|----------|------|
| test_reset_pwd_success | 重置已知用户密码，应返回成功 |
| test_reset_pwd_invalid_user_id | 使用不存在的用户ID重置密码，应返回失败 |
| test_reset_pwd_zero_user_id | 使用用户ID为0重置密码，应返回失败 |
| test_reset_pwd_missing_id | 缺少 id 字段，应返回失败 |

## test_user_save.py

| 测试用例 | 说明 |
|----------|------|
| test_save_user_success | 使用有效参数创建用户，应返回成功 |
| test_save_user_duplicate_phone | 使用已注册的手机号创建用户，应返回失败 |
| test_save_user_missing_user_name | 缺少 userName 字段，应返回失败 |
| test_save_user_missing_real_name | 缺少 realName 字段，应返回失败 |
| test_save_user_invalid_phone | 使用无效手机号格式，应返回失败 |
| test_save_user_missing_role_group_id | roleGroupId 设为 0，应返回失败 |
| test_save_user_missing_sex | sex 设为 None，应返回失败 |
| test_save_user_missing_status | 缺少 status 字段，后端实际接受并返回成功（必填校验不严格） |
| test_save_user_missing_all_required | 所有必填字段均为空，应返回失败 |

## 统计

- 测试文件数：7
- 测试用例数：43

### 覆盖接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/platform/user/save` | POST | 新增/保存平台用户 |
| `/platform/user/page` | POST | 分页查询用户列表 |
| `/platform/user/edit` | POST | 编辑用户信息 |
| `/platform/user/delete` | POST | 删除用户 |
| `/platform/user/detail` | POST | 查询用户详情 |
| `/platform/user/changeStatus` | POST | 修改用户状态 |
| `/platform/user/resetPwd` | POST | 重置用户密码 |
