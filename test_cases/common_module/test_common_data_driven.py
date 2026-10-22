"""
test_common_data_driven.py - 公共接口数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/common_data.json")


class TestCommon(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_common_api(self, case):
        """按数据文件中的参数执行公共接口测试"""
        self.run_case(case, {})

    def assert_side_effect(self, case, payload, data, ctx):
        api = case["api"]
        if api == "get_user_info":
            info = data.get("data") or {}
            assert info.get("userName") == self.config["username"], f"返回的用户与登录账号不一致: {info}"
        elif api == "area_tree_all":
            tree = data.get("data")
            assert tree, "区域树不应为空"
        elif api == "platform_home":
            assert data.get("data") is not None, "首页数据不应为空"
