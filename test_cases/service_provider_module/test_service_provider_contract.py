"""
test_service_provider_contract.py - 服务商管理接口契约校验
"""

import pytest

from .test_base import TestBase


class TestServiceProviderContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: changeStatus 对不存在的服务商ID仍返回成功")
    @pytest.mark.backend_bug
    def test_change_status_should_reject_unknown_id(self):
        """不存在的服务商应校验失败"""
        response = self.client.post("/platform/serverUser/changeStatus", json={"id": 99999999, "status": 0})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: delete 对不存在的服务商ID仍返回成功")
    @pytest.mark.backend_bug
    def test_delete_should_reject_unknown_id(self):
        """不存在的服务商应校验失败"""
        response = self.client.post("/platform/serverUser/delete", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: detail 不存在的服务商返回“用户不存在或状态失效”")
    @pytest.mark.backend_bug
    def test_detail_unknown_id_error_message(self):
        """错误文案应为“服务商不存在”"""
        response = self.client.post("/platform/serverUser/detail", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data, expected_code="01000009")
        assert "服务商不存在" in (data.get("message") or ""), f"错误文案不正确: {data.get('message')}"

    @pytest.mark.skip(reason="重置密码会发送短信验证码，环境不允许发送短信")
    def test_reset_pwd(self):
        """重置服务商密码（会发送短信，暂不执行）"""
        row_id, _, _, _ = self._create_provider()
        response = self.client.post("/platform/serverUser/resetPwd", json={"id": row_id})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
