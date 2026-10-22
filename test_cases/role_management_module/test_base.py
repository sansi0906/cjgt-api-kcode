"""
test_base.py - 角色管理测试基类
=================================
提供角色管理模块的通用造数、清理与断言辅助方法
"""

import uuid

import pytest
from utils.base_test import BaseTest


class TestBase(BaseTest):
    _module_name = "role_management_module"
    _module_desc = "角色管理模块"

    @staticmethod
    def _unique(prefix="AUTO", length=6):
        """生成唯一标识"""
        return prefix + str(uuid.uuid4().int % (10 ** length)).zfill(length)

    def _unique_role_name(self):
        return "自动化角色" + str(uuid.uuid4().int % 10**6).zfill(6)

    def _unique_role_no(self):
        return self._unique("AUTO", 8)

    def _create_role(self, role_name=None, role_no=None, status=1, role_remark="自动化创建"):
        """创建角色，返回 (role_id, role_name, role_no)"""
        role_name = role_name or self._unique_role_name()
        role_no = role_no or self._unique_role_no()
        response = self.client.save_role(
            role_name=role_name,
            role_no=role_no,
            status=status,
            role_remark=role_remark,
        )
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row("cjgt_platform_role", "role_no = %s", (role_no,))
        assert row, f"创建角色未落库: {role_no}"
        self.register_business_row("cjgt_platform_role", row["id"])
        return row["id"], role_name, role_no

    def _role_row(self, role_id):
        return self.fetch_business_row("cjgt_platform_role", "id = %s", (role_id,))
