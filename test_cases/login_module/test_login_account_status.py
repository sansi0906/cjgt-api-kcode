"""
test_login_account_status.py - 账号状态异常登录测试
=====================================================
覆盖平台用户禁用、服务商禁用、账号逻辑删除三种不可登录场景。

说明：业务库中的逻辑删除数据会被业务侧清理任务物理清除，因此删除态账号由用例
自行创建（复用管理员/服务商密码盐）并在 teardown 中清理；禁用态账号若已被清理，
用例会自动补建，保证用例稳定可重复执行。
"""

import uuid

import pytest
from .test_base import TestBase


class TestLoginAccountStatus(TestBase):
    _skip_auto_login = True

    def _fetch_row(self, table, column, value):
        pg_helper = self._get_pg_helper()
        return pg_helper.fetch_one(
            f"SELECT id, status, delete_status FROM {table} WHERE {column} = %s", (value,)
        )

    def test_admin_login_failed_when_account_disabled(self):
        """管理后台账号被禁用(status=0)时登录应返回 01000009"""
        username = self.require_account("disabled_admin_username")
        row = self._fetch_row("cjgt_platform_user", "user_name", username)
        if not row:
            self._create_temp_platform_user(username, status=0, delete_status=0)
            row = self._fetch_row("cjgt_platform_user", "user_name", username)
        assert row, "禁用的管理后台账号不存在，无法执行状态异常测试"
        assert row["status"] == 0, f"账号应为禁用状态(status=0)，实际 {row['status']}"

        response = self.client.login(
            username=username,
            password=self.config["disabled_admin_password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000009")

    def test_provider_login_failed_when_account_disabled(self):
        """服务商账号被禁用(status=0)时登录应返回 01000009"""
        phone = self.require_account("disabled_provider_username")
        row = self._fetch_row("cjgt_service_provider", "contact_phone", phone)
        if not row:
            self._create_temp_service_provider(phone, status=0, delete_status=0)
            row = self._fetch_row("cjgt_service_provider", "contact_phone", phone)
        assert row, "禁用的服务商账号不存在，无法执行状态异常测试"
        assert row["status"] == 0, f"账号应为禁用状态(status=0)，实际 {row['status']}"

        response = self.client.login(
            username=phone,
            password=self.config["disabled_provider_password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("provider_web_type", 1),
        )
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000009")

    def test_admin_login_failed_when_account_deleted(self):
        """账号被逻辑删除(delete_status=1)时登录应返回 01000009"""
        username = self.require_account("deleted_admin_username")
        self._create_temp_platform_user(username, status=1, delete_status=1)
        row = self._fetch_row("cjgt_platform_user", "user_name", username)
        assert row, "已删除账号创建失败"
        assert row["delete_status"] == 1, f"账号应为已删除状态(delete_status=1)，实际 {row['delete_status']}"

        response = self.client.login(
            username=username,
            password=self.config["deleted_admin_password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        self.validator.assert_status_code(response, 200)
        self.assert_login_failure(response.json(), expected_code="01000009")
