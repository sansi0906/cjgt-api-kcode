"""
test_base.py - 登录模块测试基类
==================================================
提供登录模块的通用测试设置和辅助方法
"""

import time
import uuid
import datetime


def _now():
    return datetime.datetime.now()

import pytest
from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "login_module"
    _module_desc = "登录模块"

    api_paths = {
        "login": "/sys/login",
        "logout": "/sys/logout",
    }

    def _create_temp_platform_user(self, username, status=1, delete_status=0):
        """基于管理员账号复制密码盐，造一个临时平台用户，返回账号 id

        用于构造"禁用态/删除态"账号，避免依赖业务库中易被清理的预置数据。
        """
        pg_helper = self._get_pg_helper()
        template = pg_helper.fetch_one(
            "SELECT password, salt, real_name, sex, role_group_id, role_group_name, status, is_super_admin "
            "FROM cjgt_platform_user WHERE user_name = %s",
            (self.config["username"],),
        )
        assert template, "管理员账号不存在，无法创建临时账号"
        row_id = self.insert_business_row(
            "cjgt_platform_user",
            {
                "user_uuid": str(uuid.uuid4()),
                "user_no": "T" + str(uuid.uuid4().int % 10**8),
                "user_name": username,
                "password": template["password"],
                "real_name": "自动化临时账号",
                "salt": template["salt"],
                "status": status,
                "is_super_admin": 0,
                "create_user_name": "auto_test",
                "create_time": _now(),
                "delete_status": delete_status,
                "role_group_name": template["role_group_name"],
                "role_group_id": template["role_group_id"],
                "sex": template["sex"],
                "create_user_uuid": str(uuid.uuid4()),
                "last_modify_uuid": None,
            },
        )
        return row_id

    def _create_temp_service_provider(self, contact_phone, status=1, delete_status=0):
        """造一个临时服务商账号（复制服务商密码盐），返回账号 id"""
        pg_helper = self._get_pg_helper()
        template = pg_helper.fetch_one(
            "SELECT password, salt, role_group_id FROM cjgt_service_provider WHERE contact_phone = %s",
            (self.config["provider_username"],),
        )
        assert template, "服务商账号不存在，无法创建临时账号"
        row_id = self.insert_business_row(
            "cjgt_service_provider",
            {
                "provider_uuid": str(uuid.uuid4()),
                "company_no": "T" + str(uuid.uuid4().int % 10**8),
                "company_name": "自动化临时服务商",
                "unified_social_code": "AUTO" + str(uuid.uuid4().int % 10**10),
                "contact_phone": contact_phone,
                "contact_person": "自动化测试",
                "status": status,
                "delete_status": delete_status,
                "password": template["password"],
                "salt": template["salt"],
                "create_user_name": "auto_test",
                "create_time": _now(),
                "create_user_uuid": str(uuid.uuid4()),
                "last_modify_uuid": None,
                "role_group_id": template["role_group_id"],
            },
        )
        return row_id

    def assert_login_payload(self, data, expect_username=None):
        """断言登录成功且响应体结构完整（token 为 JWT 形态、账号一致）"""
        self.assert_login_success(data)
        payload = data.get("data") or {}
        assert "token" in payload, f"响应缺少 token: {data}"
        assert "userName" in payload, f"响应缺少 userName: {data}"
        token = payload["token"]
        assert token.startswith("eyJ") and token.count(".") == 2, \
            f"token 不符合 JWT 形态: {token}"
        if expect_username is not None:
            assert payload.get("userName") == expect_username, \
                f"响应账号与登录账号不一致: {data}"

    def require_account(self, config_key):
        """读取账号配置，未配置则跳过用例（避免新环境直接报错）"""
        value = self.config.get(config_key) or ""
        if not value:
            pytest.skip(f"未配置测试账号 {config_key}，跳过该用例")
        return value
