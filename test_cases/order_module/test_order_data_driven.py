"""
test_order_data_driven.py - 订单管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/order_data.json")


class TestOrder(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_order_api(self, case):
        """按数据文件中的参数执行订单管理接口测试"""
        ctx = self._ctx()
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "detail":
            detail = data.get("data") or {}
            assert str(detail.get("id")) == str(payload["id"]), f"返回订单与请求不一致: {detail}"
