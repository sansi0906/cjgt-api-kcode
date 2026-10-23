"""
test_base.py - 首页测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "home_module"
    _module_desc = "首页模块"

    api_paths = {
        "home": "/platform/home",
    }
