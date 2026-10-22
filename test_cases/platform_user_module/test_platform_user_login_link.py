"""
test_platform_user_login_link.py - 平台用户状态与登录联动测试
=================================================================
验证平台用户被禁用/删除后无法登录，与登录模块的异常态场景形成闭环。
"""

import pytest

from .test_base import TestBase


class TestPlatformUserLoginLink(TestBase):
    @pytest.mark.smoke
    def test_disabled_user_cannot_login(self):
        """用户被禁用后登录应返回 01000009"""
        user_id, phone = self._create_user()
        response = self.client.post("/platform/user/changeStatus", json={"id": user_id, "status": 0})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

        row = self.fetch_business_row("cjgt_platform_user", "id = %s", (user_id,))
        assert row["status"] == 0, f"状态未落库: {row}"

        login_response = self.client.login(
            username=phone,
            password="123456",
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        self.validator.assert_status_code(login_response, 200)
        self.assert_api_failure(login_response.json(), expected_code="01000009")

    def test_deleted_user_cannot_login(self):
        """用户被删除后登录应返回 01000009"""
        user_id, phone = self._create_user()
        response = self.client.post("/platform/user/delete", json={"id": user_id})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

        row = self.fetch_business_row("cjgt_platform_user", "id = %s", (user_id,))
        assert row["delete_status"] == 1, f"删除状态未落库: {row}"

        login_response = self.client.login(
            username=phone,
            password="123456",
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        self.validator.assert_status_code(login_response, 200)
        self.assert_api_failure(login_response.json(), expected_code="01000009")
