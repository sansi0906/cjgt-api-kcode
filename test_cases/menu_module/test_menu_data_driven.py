"""
test_menu_data_driven.py - 菜单管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/menu_data.json")


class TestMenu(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_menu_api(self, case):
        """按数据文件中的参数执行菜单管理接口测试"""
        ctx = self._ctx() if case.get("need_entity") else {"unique_menu_name": self._unique_menu_name()}
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "add":
            row = self.fetch_business_row(self.TABLE, "menu_name = %s", (payload["menuName"],))
            assert row, f"菜单未落库: {payload['menuName']}"
            self.register_business_row(self.TABLE, row["id"])
        elif case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["menu_name"] == payload["menuName"], f"菜单名称未更新: {row}"
