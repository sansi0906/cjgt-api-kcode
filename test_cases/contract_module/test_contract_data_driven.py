"""
test_contract_data_driven.py - 合同管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/contract_data.json")


class TestContract(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_contract_api(self, case):
        """按数据文件中的参数执行合同管理接口测试"""
        self.run_case(case, {})

    def assert_side_effect(self, case, payload, data, ctx):
        result = data.get("result") or data.get("data") or {}
        assert "records" in result or "list" in result, f"分页结果结构异常: {data}"
