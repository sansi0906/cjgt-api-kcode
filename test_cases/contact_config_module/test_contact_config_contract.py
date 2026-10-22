"""
test_contact_config_contract.py - 合同服务配置接口契约校验
"""

import pytest

from .test_base import TestBase


class TestContactConfigContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: content 缺失时未做必填校验，返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_save_should_require_content(self):
        """Swagger 标记 content 必填，应返回 01000006"""
        item_id = self._create_service_item()
        response = self.client.post("/platform/contactConfig/save", json={
            "title": self._unique_title(),
            "serviceItemId": item_id,
            "priceContent": "价格内容",
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000006")
