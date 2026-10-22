"""
test_tax_type_config_data_driven.py - 税种配置管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/tax_type_config_data.json")


class TestTaxTypeConfig(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_tax_type_api(self, case):
        """按数据文件中的参数执行税种配置接口测试"""
        ctx = self._ctx() if case.get("need_entity") else {"unique_tax_name": self._unique_tax_name()}
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "add":
            row = self.fetch_business_row(self.TABLE, "tax_type_name = %s", (payload["taxTypeName"],))
            assert row, f"税种未落库: {payload['taxTypeName']}"
            self.register_business_row(self.TABLE, row["id"])
            assert row["tax_type_name"] == payload["taxTypeName"], f"税种名称未落库: {row}"
        elif case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["tax_type_name"] == payload["taxTypeName"], f"税种名称未更新: {row}"
            assert row["fixed_display"] == payload["fixedDisplay"], f"固定展示标识未更新: {row}"
        elif case["api"] == "status":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["status"] == payload["status"], f"税种状态未更新: {row}"
