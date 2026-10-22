"""
test_common_contract.py - 公共接口契约校验
"""

import pytest

from .test_base import TestBase


class TestCommonContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: 对 GET 接口使用 POST 返回系统异常(02)，应返回 405")
    @pytest.mark.backend_bug
    def test_platform_home_should_reject_post(self):
        """平台首页为 GET 接口，POST 调用应返回 405"""
        response = self.client.post("/platform/home", json={})
        self.validator.assert_status_code(response, 405)
