"""
test_base.py - 平台用户管理测试基类
=====================================
提供平台用户管理模块的通用造数、清理与断言辅助方法
"""

import uuid

import pytest
from utils.base_test import BaseTest


class TestBase(BaseTest):
    _module_name = "platform_user_module"
    _module_desc = "平台用户管理模块"

    @staticmethod
    def _unique_phone(prefix="176"):
        """生成唯一测试手机号"""
        return prefix + str(uuid.uuid4().int % 10**8).zfill(8)

    def _create_user(self, phone=None, real_name="自动化测试用户", sex=1, role_group_id=5, status=1):
        """通过接口创建平台用户，返回 (user_id, phone)"""
        phone = phone or self._unique_phone()
        response = self.client.save_platform_user(
            user_name=phone,
            real_name=real_name,
            sex=sex,
            role_group_id=role_group_id,
            status=status,
        )
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row("cjgt_platform_user", "user_name = %s", (phone,))
        assert row, f"创建用户未落库: {phone}"
        self.register_business_row("cjgt_platform_user", row["id"])
        return row["id"], phone

    def _user_status(self, user_id):
        """查询平台用户状态"""
        row = self.fetch_business_row("cjgt_platform_user", "id = %s", (user_id,))
        return row
