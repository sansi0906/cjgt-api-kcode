"""
test_super_individual_data_driven.py - 超级个体档案管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/super_individual_data.json")


class TestSuperIndividual(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_super_individual_api(self, case):
        """按数据文件中的参数执行超级个体档案接口测试"""
        ctx = self._ctx() if case.get("need_worker") else {
            "worker_user_no": case.get("payload", {}).get("worker_user_no", "NON_EXISTENT_999"),
        }
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        api = case["api"]
        if api == "detail":
            detail = data.get("data") or {}
            assert detail.get("workerUserNo") == ctx["worker_user_no"], f"返回档案与请求不一致: {detail}"
        elif api in ("contracts", "assignment_records"):
            assert isinstance(data.get("data"), list), f"列表结构异常: {data}"
        elif api == "page":
            result = data.get("result") or data.get("data") or {}
            assert "records" in result or "list" in result, f"分页结果结构异常: {data}"
