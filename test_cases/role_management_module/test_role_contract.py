"""
test_role_contract.py - 角色管理接口契约校验
=============================================
覆盖 Swagger 声明的必填项与取值约束，与后端实际行为不一致的用例标记为
backend_bug / xfail，待后端修复后自动转为通过。
"""

import pytest

from .test_base import TestBase


class TestRoleContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: status 非法取值未校验")
    @pytest.mark.backend_bug
    def test_save_should_reject_invalid_status(self):
        """status 仅允许 0/1，非法值应校验失败"""
        role_no = self._unique_role_no()
        try:
            response = self.client.post("/common/role/save", json={
                "roleName": self._unique_role_name(),
                "roleNo": role_no,
                "status": 5,
            })
            self.validator.assert_status_code(response, 200)
            self.assert_api_failure(response.json())
        finally:
            row = self.fetch_business_row("cjgt_platform_role", "role_no = %s", (role_no,))
            if row:
                self.delete_business_row("cjgt_platform_role", row["id"])

    @pytest.mark.xfail(reason="Backend bug: changeStatus 未校验 status 取值")
    @pytest.mark.backend_bug
    def test_change_status_should_reject_invalid_status(self):
        """changeStatus 的 status 仅允许 0/1"""
        role_id, _, _ = self._create_role()
        response = self.client.post("/common/role/changeStatus", json={"id": role_id, "status": 2})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: changeStatus 缺少 status 时仍返回成功")
    @pytest.mark.backend_bug
    def test_change_status_should_require_status(self):
        """Swagger 标记 status 必填"""
        role_id, _, _ = self._create_role()
        response = self.client.post("/common/role/changeStatus", json={"id": role_id})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000006")

    @pytest.mark.xfail(reason="Backend bug: delete 对不存在的角色ID仍返回成功")
    @pytest.mark.backend_bug
    def test_delete_should_reject_unknown_role(self):
        """不存在的角色ID应校验失败"""
        response = self.client.post("/common/role/delete", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: edit 不存在的角色ID返回“角色名称已存在”错误提示")
    @pytest.mark.backend_bug
    def test_edit_should_report_unknown_role(self):
        """不存在的角色ID应返回“角色不存在”"""
        response = self.client.post("/common/role/edit", json={
            "id": 99999999,
            "roleName": self._unique_role_name(),
            "roleNo": self._unique_role_no(),
            "status": 1,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000018")
