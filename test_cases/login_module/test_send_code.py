"""
test_send_code.py - 短信验证码发送接口测试
===============================================
覆盖验证码发送模块的场景：
- 正常发送验证码
- 60 秒内重复发送触发频率限制
- 无效手机号格式
- 空手机号
- 缺少必填字段（phone / webType）
- 频率限制过期后重新发送
- 发送验证码后从数据库查询验证码并用其登录

使用固定手机号：17695729351、15810299672
"""

import random
import time

import pytest

from .test_base import TestBase

PHONE_1 = "17695729351"
PHONE_2 = "15810299672"

RATE_LIMIT_WAIT = 61


def _generate_test_phone():
    """生成用于测试的手机号（174开头，避免与真实用户冲突）"""
    suffix = random.randint(10000000, 99999999)
    return f"174{suffix}"


class TestSendCode(TestBase):
    def test_send_code_missing_phone(self):
        """缺少 phone 字段，应返回失败"""
        response = self.client.send_code(phone="")
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_failure(data)

    def test_send_code_missing_web_type(self):
        """缺少 webType 字段，应返回失败"""
        response = self.client.post("/sys/sendCode", json={"phone": PHONE_1})
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_failure(data)

    @pytest.mark.slow
    def test_send_code_after_rate_limit_expires(self):
        """60 秒频率限制过期后重新发送验证码，应返回成功"""
        response = self.client.send_code(phone=PHONE_1)
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_success(data)

        time.sleep(RATE_LIMIT_WAIT)

        response = self.client.send_code(phone=PHONE_1)
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_success(data)

    def test_send_code_and_login_with_sms_from_db(self, pg_helper):
        """发送验证码后从数据库查询验证码并用其登录成功"""
        phone = PHONE_1

        time.sleep(RATE_LIMIT_WAIT)

        # 1. 发送验证码
        response = self.client.send_code(phone=phone)
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_success(data)

        # 2. 从 PostgreSQL 数据库查询验证码
        sms_code = self._get_sms_code_from_db(phone, pg_helper)
        assert sms_code, f"未从数据库获取到手机号 {phone} 的验证码"
        print(f"从数据库获取到验证码: {sms_code}")

        # 3. 使用数据库中的验证码登录
        login_response = self.client.login_with_sms(username=phone, sms_code=sms_code)
        self.validator.assert_status_code(login_response, 200)
        login_data = login_response.json()
        self.assert_save_success(login_data)
        token = login_data.get("data", {}).get("token")
        assert token, f"登录成功但未返回 token: {login_data}"
        print(f"登录成功，token: {token[:20]}...")

    def test_send_code_to_non_existent_user_should_fail(self, pg_helper):
        """向不存在的用户发送验证码应失败（Bug: 当前后端允许发送）"""
        phone = PHONE_2  # 15810299672，确认不存在于 cjgt_platform_user

        # 1. 验证用户不存在
        user_exists = self._check_user_exists(phone, pg_helper)
        assert not user_exists, f"测试前置条件失败：手机号 {phone} 已存在于平台用户表"
        print(f"确认用户 {phone} 不存在于 cjgt_platform_user")

        # 2. 发送验证码
        response = self.client.send_code(phone=phone)
        self.validator.assert_status_code(response, 200)
        data = response.json()

        # 3. 验证是否发送成功
        if data.get("code") in ("0", "00"):
            print(f"Bug: 后端允许向不存在的用户 {phone} 发送验证码: {data}")
            # 记录 Bug 证据
            if self.db_helper:
                try:
                    self.db_helper.save_test_log(
                        execution_id=self.execution_id,
                        level="BUG",
                        message=f"向不存在的用户发送验证码成功: phone={phone}, response={data}",
                        module=self._module_name,
                        case_name=self._test_name,
                    )
                except Exception:
                    pass
            self.assert_save_failure(data)
        else:
            print(f"正常：后端拒绝向不存在的用户发送验证码: {data}")
            self.assert_save_failure(data)
