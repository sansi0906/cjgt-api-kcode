"""
test_role_data_driven.py - 角色管理数据驱动测试
================================================
从 data/role_data.json 读取用例，覆盖 9 个角色管理接口的正向与逆向场景。

占位符约定：
- ${unique_role_name}  本次运行生成的唯一角色名称
- ${unique_role_no}    本次运行生成的唯一角色编码
- ${role_id}           预置测试角色的ID
- ${role_name}         预置测试角色的名称
- ${role_no}           预置测试角色的编码
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import TestBase

CASES, IDS = load_param_cases("data/role_data.json")


class TestRoleDataDriven(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_role_api(self, case):
        """按数据文件中的参数执行角色管理接口测试"""
        ctx = self._ctx() if case.get("need_role") else {
            "unique_role_name": self._unique_role_name(),
            "unique_role_no": self._unique_role_no(),
        }
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        """校验接口成功后的落库情况"""
        api = case["api"]
        if api == "save":
            row = self.fetch_business_row("cjgt_platform_role", "role_no = %s", (payload["roleNo"],))
            assert row, f"新增角色未落库: {payload['roleNo']}"
            self.register_business_row("cjgt_platform_role", row["id"])
        elif api == "edit":
            row = self._role_row(payload["id"])
            assert row["role_name"] == payload["roleName"], f"角色名称未更新: {row}"
            assert row["role_remark"] == payload["roleRemark"], f"角色备注未更新: {row}"
        elif api == "change_status":
            row = self._role_row(payload["id"])
            assert row["status"] == payload["status"], f"角色状态未更新: {row}"
        elif api == "delete":
            row = self._role_row(payload["id"])
            assert row["delete_status"] == 1, f"删除状态未更新: {row}"
        elif api == "page":
            result = data.get("result") or data.get("data") or {}
            assert "records" in result or "list" in result, f"分页结果结构异常: {data}"
