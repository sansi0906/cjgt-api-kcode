"""
test_open_api_data_driven.py - open-api 数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/open_api_data.json")


class TestOpenApi(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_open_api(self, case):
        """按数据文件中的参数执行 open-api 接口测试"""
        self.run_case(case, {})
