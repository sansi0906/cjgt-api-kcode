"""
test_contact_config_data_driven.py - 合同服务配置管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/contact_config_data.json")


class TestContactConfig(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_contact_config_api(self, case):
        """按数据文件中的参数执行合同服务配置接口测试"""
        if case.get("need_item"):
            item_id = self._create_service_item()
            ctx = {"unique_title": self._unique_title(), "service_item_id": item_id}
            if case["api"] == "save":
                # 同一服务项目重复新增：先建一条再重复
                if case["name"] == "save_duplicate_service_item":
                    self.run_case({"api": "save", "expect_success": True, "payload": {
                        "title": self._unique_title(), "serviceItemId": item_id,
                        "content": "首次配置", "priceContent": "价格"}}, ctx)
            self.run_case(case, ctx)
            return

        ctx = self._ctx() if case.get("need_entity") else {"unique_title": self._unique_title()}
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "save":
            row = self.fetch_business_row(self.TABLE, "title = %s", (payload["title"],))
            assert row, f"合同服务未落库: {payload['title']}"
            self.register_business_row(self.TABLE, row["id"])
        elif case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["title"] == payload["title"], f"合同服务标题未更新: {row}"
            assert row["content"] == payload["content"], f"合同服务内容未更新: {row}"
