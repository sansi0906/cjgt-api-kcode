"""
test_base.py - 服务商端测试基类
=================================
所有服务商端 (/server/*) 模块测试类的基类，提供客户端初始化、服务商登录、
断言、数据库记录等通用功能。
"""

import pytest

from api_clients.provider_client import ProviderClient
from utils.base_test import BaseTest


class ProviderTestBase(BaseTest):
    _module_name = "server_module"
    _module_desc = "服务商端模块"
    _skip_auto_login = False

    @pytest.fixture(autouse=True)
    def setup(self, config, execution_id, db_helper, pg_cleanup, request):
        """自动初始化服务商客户端、验证器并以服务商身份登录"""
        self.client = ProviderClient(base_url=config["base_url"])
        from utils.validator import ResponseValidator
        self.validator = ResponseValidator()
        self.config = config
        self.execution_id = execution_id
        self.db_helper = db_helper
        self.pg_cleanup = pg_cleanup
        self._created_ids = []
        self._business_rows = []
        self._module_id = None
        self._test_name = request.node.name
        if not self._skip_auto_login:
            token = self.login()
            self.client.set_token(token)

    def login(self, username=None, password=None, login_type=None, web_type=None):
        """执行服务商登录并返回 Token"""
        response = self.client.login(
            username=username or self.config["provider_username"],
            password=password or self.config["provider_password"],
            login_type=login_type if login_type is not None else self.config.get("provider_web_type", 1),
            web_type=web_type if web_type is not None else self.config.get("provider_web_type", 1),
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") in ("0", "00"), f"Provider login failed: {data}"
        return data.get("data", {}).get("token")
