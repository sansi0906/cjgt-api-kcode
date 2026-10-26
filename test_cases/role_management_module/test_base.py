"""
test_base.py - 角色管理测试基类
=================================
提供角色管理模块的通用造数、清理与断言辅助方法
"""

import pytest
from utils.module_base import DataDrivenApiTestBase
from utils.factories import UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "role_management_module"
    _module_desc = "角色管理模块"

    api_paths = {
        "save": "/common/role/save",
        "page": "/common/role/page",
        "detail": "/common/role/detail",
        "edit": "/common/role/edit",
        "change_status": "/common/role/changeStatus",
        "delete": "/common/role/delete",
        "select_role_all": "/common/role/selectRoleAll",
        "select_menu_list": "/common/role/selectMenuListByRoleId",
        "add_role_menu": "/common/role/addRoleMenu",
    }

    TABLE = "cjgt_platform_role"

    @staticmethod
    def _unique(prefix="AUTO", length=6):
        """生成唯一标识"""
        return UniqueValueFactory.unique_id(prefix, length)

    def _unique_role_name(self):
        return UniqueValueFactory.unique_role_name()

    def _unique_role_no(self):
        return UniqueValueFactory.unique_role_no()

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

    def _ctx(self, role_id=None, role_name=None, role_no=None):
        """造数上下文：need_role 时创建角色"""
        if role_id is None:
            role_id, role_name, role_no = self._create_role()
        return {
            "role_id": role_id,
            "role_name": role_name,
            "role_no": role_no,
            "unique_role_name": self._unique_role_name(),
            "unique_role_no": self._unique_role_no(),
        }
