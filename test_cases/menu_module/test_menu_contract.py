"""
test_menu_contract.py - 菜单管理接口契约校验
"""

import pytest

from .test_base import TestBase


class TestMenuContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: del 对不存在的菜单ID仍返回成功")
    @pytest.mark.backend_bug
    def test_delete_should_reject_unknown_id(self):
        """不存在的菜单应校验失败"""
        response = self.client.post("/common/menu/del", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())
