"""
test_platform_user_contract.py - 平台用户管理接口契约校验
============================================================
覆盖 Swagger 声明的必填项与取值约束，与后端实际行为不一致的用例标记为
backend_bug / xfail，待后端修复后自动转为通过。
"""

import pytest

from .test_base import TestBase


class TestPlatformUserContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: roleGroupId 缺失时仍创建成功（Swagger 标记必填）")
    @pytest.mark.backend_bug
    def test_save_should_require_role_group_id(self):
        """Swagger 标记 roleGroupId 必填，后端缺失时仍返回成功"""
        response = self.client.post("/platform/user/save", json={
            "userName": self._unique_phone(),
            "realName": "契约测试",
            "sex": 1,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000006")

    @pytest.mark.xfail(reason="Backend bug: roleGroupId 不存在时仍创建成功")
    @pytest.mark.backend_bug
    def test_save_should_reject_unknown_role_group(self):
        """角色组不存在时应校验失败"""
        response = self.client.post("/platform/user/save", json={
            "userName": self._unique_phone(),
            "realName": "契约测试",
            "sex": 1,
            "roleGroupId": 99999,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: changeStatus 非法 status 值未校验")
    @pytest.mark.backend_bug
    def test_change_status_should_reject_invalid_status(self):
        """status 仅允许 0/1，非法值应校验失败"""
        user_id, _ = self._create_user()
        response = self.client.post("/platform/user/changeStatus", json={"id": user_id, "status": 2})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: changeStatus 对不存在的用户ID仍返回成功")
    @pytest.mark.backend_bug
    def test_change_status_should_reject_unknown_user(self):
        """不存在的用户ID应校验失败"""
        response = self.client.post("/platform/user/changeStatus", json={"id": 99999999, "status": 0})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: delete 对不存在的用户ID仍返回成功")
    @pytest.mark.backend_bug
    def test_delete_should_reject_unknown_user(self):
        """不存在的用户ID应校验失败"""
        response = self.client.post("/platform/user/delete", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.skip(reason="重置密码会发送短信验证码，环境不允许发送短信")
    def test_reset_pwd(self):
        """重置密码（会发送短信，暂不执行）"""
        user_id, _ = self._create_user()
        response = self.client.post("/platform/user/resetPwd", json={"id": user_id})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
