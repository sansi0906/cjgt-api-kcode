"""
test_home_data_driven.py - 首页数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/home_data.json")


class TestHome(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_home_api(self, case):
        """按数据文件中的参数执行首页接口测试"""
        self.run_case(case, {})
