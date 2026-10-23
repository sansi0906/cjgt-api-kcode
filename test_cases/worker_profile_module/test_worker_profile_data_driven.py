"""
test_worker_profile_data_driven.py - 工作者档案数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/worker_profile_data.json")


class TestWorkerProfile(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_worker_profile_api(self, case):
        """按数据文件中的参数执行工作者档案接口测试"""
        ctx = {}
        if case.get("need_entity"):
            ctx["workerUserNo"] = self._get_worker_user_no()
        self.run_case(case, ctx)
