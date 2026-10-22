"""
test_base.py - 公共接口测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "common_module"
    _module_desc = "公共接口模块"

    api_paths = {
        "area_tree_all": "/common/area/treeAll",
        "get_user_info": "/common/getUserInfo",
        "platform_home": "/platform/home",
    }
