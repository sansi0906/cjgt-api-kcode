"""
test_login_db_verify.py - 登录结果与业务库回查测试
==================================================
校验登录成功后，被测系统业务库（165 PostgreSQL）中的账号状态与登录时间被正确更新，
用于验证"接口返回成功"与"数据真实落库"一致。
"""

import time

import pytest
from .test_base import TestBase


class TestLoginDbVerify(TestBase):
    _skip_auto_login = True

    def _fetch_login_time(self, table, column, value):
        pg_helper = self._get_pg_helper()
        sql = f"SELECT last_login_time FROM {table} WHERE {column} = %s"
        result = pg_helper.fetch_one(sql, (value,))
        return result.get("last_login_time") if result else None

    @pytest.mark.smoke
    def test_admin_login_updates_platform_user_last_login_time(self):
        """管理后台登录后，平台用户表 last_login_time 应刷新"""
        before = self._fetch_login_time("cjgt_platform_user", "user_name", self.config["username"])
        time.sleep(1)
        response = self.client.login(
            username=self.config["username"],
            password=self.config["password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        self.validator.assert_status_code(response, 200)
        self.assert_login_payload(response.json(), expect_username=self.config["username"])
        after = self._fetch_login_time("cjgt_platform_user", "user_name", self.config["username"])
        assert after is not None, "平台用户不存在，无法校验登录时间"
        assert after != before, f"last_login_time 未刷新: before={before}, after={after}"

    def test_provider_login_updates_service_provider_last_login_time(self):
        """服务商后台登录后，服务商表 last_login_time 应刷新"""
        self.require_account("provider_username")
        before = self._fetch_login_time("cjgt_service_provider", "contact_phone", self.config["provider_username"])
        time.sleep(1)
        response = self.client.login(
            username=self.config["provider_username"],
            password=self.config["provider_password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("provider_web_type", 1),
        )
        self.validator.assert_status_code(response, 200)
        self.assert_login_payload(response.json(), expect_username=self.config["provider_username"])
        after = self._fetch_login_time("cjgt_service_provider", "contact_phone", self.config["provider_username"])
        assert after is not None, "服务商账号不存在，无法校验登录时间"
        assert after != before, f"last_login_time 未刷新: before={before}, after={after}"

    def test_login_response_time_within_threshold(self):
        """登录接口响应时间应满足性能阈值"""
        response = self.client.login(
            username=self.config["username"],
            password=self.config["password"],
            login_type=self.config.get("login_type", 1),
            web_type=self.config.get("web_type", 0),
        )
        duration_ms = self.assert_response_time(response, max_duration_ms=2000)
        print(f"login response time: {duration_ms}ms")
