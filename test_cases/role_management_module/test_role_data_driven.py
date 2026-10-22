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

API_PATHS = {
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

CASES, IDS = load_param_cases("data/role_data.json")


class TestRoleDataDriven(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_role_api(self, case):
        """按数据文件中的参数执行角色管理接口测试"""
        role_id = None
        role_name = None
        role_no = None

        if case.get("need_role"):
            role_id, role_name, role_no = self._create_role()

        payload = {
            key: self._resolve(value, role_id=role_id, role_name=role_name, role_no=role_no)
            for key, value in (case.get("payload") or {}).items()
        }

        response = self.client.post(API_PATHS[case["api"]], json=payload)
        self.validator.assert_status_code(response, 200)
        data = response.json()

        if case.get("expect_success"):
            self.assert_api_success(data)
            self._assert_side_effect(case, payload, data, role_id, role_no)
        else:
            self.assert_api_failure(data, expected_code=case.get("expect_code"))

    def _resolve(self, value, role_id=None, role_name=None, role_no=None):
        if value == "${unique_role_name}":
            return self._unique_role_name()
        if value == "${unique_role_no}":
            return self._unique_role_no()
        if value == "${role_id}":
            return role_id
        if value == "${role_name}":
            return role_name
        if value == "${role_no}":
            return role_no
        return value

    def _assert_side_effect(self, case, payload, data, role_id, role_no):
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
