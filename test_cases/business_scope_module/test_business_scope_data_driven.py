"""
test_business_scope_data_driven.py - 经营范围配置管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/business_scope_data.json")


class TestBusinessScope(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_business_scope_api(self, case):
        """按数据文件中的参数执行经营范围接口测试"""
        ctx = self._ctx() if case.get("need_entity") else {"unique_scope_name": self._unique_scope_name()}
        if case.get("pre_disable"):
            # 业务规则：启用状态的数据不允许删除，需先禁用
            self.run_case({"api": "update_status", "payload": {"id": ctx["entity_id"], "isEnabled": 0},
                           "expect_success": True}, ctx)
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "add":
            row = self.fetch_business_row(self.TABLE, "scope_name = %s", (payload["scopeName"],))
            assert row, f"经营范围未落库: {payload['scopeName']}"
            self.register_business_row(self.TABLE, row["id"])
            assert row["scope_name"] == payload["scopeName"], f"经营范围名称未落库: {row}"
        elif case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["scope_name"] == payload["scopeName"], f"经营范围名称未更新: {row}"
        elif case["api"] == "update_status":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["is_enabled"] == payload["isEnabled"], f"启用状态未更新: {row}"
