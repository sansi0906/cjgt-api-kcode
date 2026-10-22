"""
test_login_boundary.py - 登录接口参数边界与角色隔离测试
=====================================================
覆盖场景：
- 缺少 webType / 非法 loginType
- 短信登录模式（loginType=0）带密码
- 管理后台账号与服务商账号交叉使用 webType（角色隔离）
- 密码登录模式下不传 smsCode
"""

import pytest

from .test_base import TestBase


class TestLoginBoundary(TestBase):
    _skip_auto_login = True
    @pytest.mark.smoke
    def test_login_missing_web_type(self):
        """缺少 webType，应返回 01000014 不支持的登录方式"""
        response = self.client.post("/sys/login", json={
            "username": self.config["username"],
            "password": self.config["password"],
            "loginType": self.config.get("login_type", 1),
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000014")

    def test_login_invalid_login_type(self):
        """非法 loginType，应返回 01000014 不支持的登录方式"""
        response = self.client.post("/sys/login", json={
            "username": self.config["username"],
            "password": self.config["password"],
            "loginType": 9,
            "webType": self.config.get("web_type", 0),
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000014")

    @pytest.mark.skip(reason="短信相关用例暂不执行：环境不允许发送短信验证码")
    def test_login_sms_mode_without_sms_code(self):
        """loginType=0 短信模式但未传短信验证码，应返回 01000010"""
        response = self.client.post("/sys/login", json={
            "username": self.config["username"],
            "password": self.config["password"],
            "loginType": 0,
            "webType": self.config.get("web_type", 0),
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000010")

    def test_admin_account_with_provider_web_type(self):
        """管理后台账号使用服务商 webType=1，应返回 01000009（角色隔离）"""
        response = self.client.post("/sys/login", json={
            "username": self.config["username"],
            "password": self.config["password"],
            "loginType": self.config.get("login_type", 1),
            "webType": self.config.get("provider_web_type", 1),
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000009")

    def test_provider_account_with_admin_web_type(self):
        """服务商账号使用管理后台 webType=0，应返回 01000009（角色隔离）"""
        self.require_account("provider_username")
        response = self.client.post("/sys/login", json={
            "username": self.config["provider_username"],
            "password": self.config["provider_password"],
            "loginType": self.config.get("login_type", 1),
            "webType": self.config.get("web_type", 0),
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000009")

    @pytest.mark.skip(reason="短信相关用例暂不执行：环境不允许发送短信验证码")
    @pytest.mark.backend_bug
    def test_login_password_mode_without_sms_code(self):
        """密码登录模式不传 smsCode：OpenAPI 标记必填但后端未校验，返回成功（已知契约偏差）"""
        response = self.client.post("/sys/login", json={
            "username": self.config["username"],
            "password": self.config["password"],
            "loginType": self.config.get("login_type", 1),
            "webType": self.config.get("web_type", 0),
            "smsCode": None,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_login_payload(response.json(), expect_username=self.config["username"])
