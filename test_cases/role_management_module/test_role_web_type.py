"""
test_role_web_type.py - 角色管理 WebType 隔离测试
==================================================
/common/role/* 接口按当前登录用户的 WebType 过滤，
管理后台（webType=0）与服务商后台（webType=1）可见的角色集合应互相隔离。
"""

import pytest

from .test_base import TestBase


class TestRoleWebType(TestBase):
    @pytest.mark.smoke
    def test_role_created_by_admin_not_visible_to_provider(self):
        """管理后台创建的角色不应出现在服务商后台的角色列表中"""
        role_id, role_name, role_no = self._create_role()

        admin_response = self.client.select_role_all()
        self.validator.assert_status_code(admin_response, 200)
        self.assert_api_success(admin_response.json())
        admin_roles = admin_response.json().get("data") or []
        admin_names = {r.get("roleName") for r in admin_roles}
        assert role_name in admin_names, f"管理后台未查到自建角色: {role_name}"

        provider_username = self.config.get("provider_username") or ""
        if not provider_username:
            pytest.skip("未配置服务商测试账号，跳过该用例")

        provider_login = self.client.login(
            username=self.config["provider_username"],
            password=self.config["provider_password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("provider_web_type", 1),
        )
        self.validator.assert_status_code(provider_login, 200)
        self.assert_api_success(provider_login.json())
        provider_token = provider_login.json().get("data", {}).get("token")
        assert provider_token, "服务商登录未返回 token"

        provider_response = self.client.session.post(
            f"{self.client.base_url}/common/role/selectRoleAll",
            json={},
            headers={"Content-Type": "application/json", "token": provider_token},
            timeout=self.client.timeout,
        )
        self.validator.assert_status_code(provider_response, 200)
        self.assert_api_success(provider_response.json())
        provider_roles = provider_response.json().get("data") or []
        provider_names = {r.get("roleName") for r in provider_roles}
        assert role_name not in provider_names, \
            f"服务商后台不应看到管理后台角色: {role_name}"

    def test_role_web_type_follows_login_account(self):
        """角色归属的 webType 应与创建者一致"""
        role_id, _, role_no = self._create_role()
        row = self._role_row(role_id)
        assert row["web_type"] == self.config.get("web_type"), \
            f"角色 webType 应为 {self.config.get('web_type')}，实际 {row['web_type']}"
