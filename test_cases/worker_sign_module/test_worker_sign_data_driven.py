"""
test_worker_sign_data_driven.py - 超级个体入驻数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/worker_sign_data.json")


class TestWorkerSign(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_worker_sign_api(self, case):
        """按数据文件中的参数执行超级个体入驻接口测试"""
        self.run_case(case, {})

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "station_list":
            payload_data = data.get("data") or {}
            assert "stationsList" in payload_data, f"驿站列表结构异常: {data}"
        elif case["api"] == "worker_info":
            assert "userUuid" in (data.get("data") or {}), f"工人信息结构异常: {data}"
