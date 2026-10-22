"""
test_base.py - open-api 测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "open_api_module"
    _module_desc = "open-api 内部接口模块"

    api_paths = {
        "post": "/api/cjgt",
    }
