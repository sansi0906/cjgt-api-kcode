"""
test_base.py - 合同管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "contract_module"
    _module_desc = "合同管理模块"

    api_paths = {
        "page": "/platform/contract/page",
    }
