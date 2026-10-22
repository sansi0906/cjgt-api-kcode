"""
test_file_data_driven.py - 文件管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/file_data.json")


class TestFile(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_file_api(self, case):
        """按数据文件中的参数执行文件管理接口测试"""
        ctx = {}
        if case.get("upload") or case.get("api") != "upload":
            ctx["file_uri"] = self._upload_sample()
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "upload":
            file_data = data.get("data") or {}
            assert file_data.get("uri"), f"上传未返回文件路径: {data}"
            assert file_data.get("name") == "kilo_test.png", f"文件原名不正确: {data}"
        elif case["api"] == "original_name":
            assert data.get("data"), f"未返回文件原名称: {data}"
