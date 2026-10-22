"""
test_login_data_driven.py - 数据驱动登录测试
==================================================
从 data/login_data.json 读取测试数据，按角色（管理后台/服务商后台）参数化执行登录测试。

角色取值：
- admin    管理后台账号，webType 来自 config["web_type"]
- provider 服务商后台账号，webType 来自 config["provider_web_type"]

账号与密码默认取自全局配置（.env 注入），用例可通过 username/password 字段覆盖。
"""

import pytest
from utils.data_driver import load_param_cases, resolve_role_account

from .test_base import TestBase


class TestLoginDataDriven(TestBase):
    _skip_auto_login = True
    @pytest.mark.parametrize(
        "test_case",
        load_param_cases("data/login_data.json")[0],
        ids=load_param_cases("data/login_data.json")[1],
    )
    def test_login_with_data(self, test_case):
        """使用数据文件中的参数执行登录测试"""
        if test_case.get("role") == "provider":
            self.require_account("provider_username")
        username, password, web_type = resolve_role_account(test_case, self.config)

        response = self.client.login(
            username=username,
            password=password,
            login_type=self.config.get("login_type", 1),
            web_type=web_type,
        )
        self.validator.assert_status_code(response, test_case["expected_status"])
        data = response.json()

        if test_case.get("expect_success"):
            self.assert_login_payload(data, expect_username=username)
        else:
            self.assert_login_failure(data, expected_code=test_case.get("expect_code"))
