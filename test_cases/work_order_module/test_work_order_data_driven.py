"""
test_work_order_data_driven.py - 服务工单管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/work_order_data.json")


class TestWorkOrder(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_work_order_api(self, case):
        """按数据文件中的参数执行工单管理接口测试"""
        ctx = self._ctx() if case.get("need_order") else self._ctx()
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "detail":
            detail = data.get("data") or {}
            assert str(detail.get("id")) == str(payload["workOrderId"]), f"返回工单与请求不一致: {detail}"
        elif case["api"] == "assignments":
            assert isinstance(data.get("data"), list), f"分配记录结构异常: {data}"
