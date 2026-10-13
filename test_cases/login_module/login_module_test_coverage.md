# 登录模块接口测试覆盖用例

> 生成时间：2026-08-12
> 测试环境：http://172.16.1.165:9200
> 数据库：MySQL 172.16.1.163 (test_cjgt) / PostgreSQL 172.16.1.165 (cjgt)

## test_login.py

| 测试用例 | 说明 |
|----------|------|
| test_login_success | 使用正确凭证登录，应返回成功和 Token |
| test_login_invalid_username | 使用不存在的用户名登录，应返回失败 |
| test_login_invalid_password | 使用错误密码登录，应返回失败 |
| test_login_empty_username | 使用空用户名登录，应返回失败 |
| test_login_empty_password | 使用空密码登录，应返回失败 |
| test_login_missing_login_type | 缺少 loginType 字段，应返回失败 |
| test_login_missing_sms_code | 缺少 smsCode 字段，密码登录模式下后端未校验 smsCode |
| test_login_missing_web_type | 缺少 webType 字段，应返回失败 |

## test_login_data_driven.py

| 测试用例 | 说明 |
|----------|------|
| test_login_with_data | 使用数据文件中的参数执行登录测试 |

## test_logout.py

| 测试用例 | 说明 |
|----------|------|
| test_logout_with_valid_token | 使用有效 Token 登出，应返回成功 |
| test_logout_without_token | 无 Token 登出，预期应返回失败，但后端实际返回成功（疑似未做 Token 校验） |
| test_logout_with_invalid_token | 使用无效 Token 登出，应返回失败 |
| test_logout_with_empty_token | 使用空 Token 登出，应返回失败 |
| test_logout_then_relogin | 登出后重新登录，验证完整生命周期 |

## test_send_code.py

| 测试用例 | 说明 |
|----------|------|
| test_send_code_missing_phone | 缺少 phone 字段，应返回失败 |
| test_send_code_missing_web_type | 缺少 webType 字段，应返回失败 |
| test_send_code_after_rate_limit_expires | 60 秒频率限制过期后重新发送验证码，应返回成功 |
| test_send_code_and_login_with_sms_from_db | 发送验证码后从数据库查询验证码并用其登录成功 |
| test_send_code_to_non_existent_user_should_fail | 向不存在的用户发送验证码应失败（Bug: 当前后端允许发送） |

## 统计

- 测试文件数：4
- 测试用例数：20
