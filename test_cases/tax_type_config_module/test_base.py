"""
test_base.py - 税种配置管理测试基类
"""

import uuid

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "tax_type_config_module"
    _module_desc = "税种配置管理模块"

    api_paths = {
        "add": "/platform/taxTypeConfig/add",
        "page": "/platform/taxTypeConfig/page",
        "edit": "/platform/taxTypeConfig/edit",
        "status": "/platform/taxTypeConfig/status",
    }

    TABLE = "cjgt_tax_type_config"

    @staticmethod
    def _unique_tax_name():
        return "自动化税种" + str(uuid.uuid4().int % 10**6).zfill(6)

    def _create_tax(self, name=None):
        """新增税种，返回 (id, name)"""
        name = name or self._unique_tax_name()
        row_id = self.create_by_api("add", {"taxTypeName": name, "fixedDisplay": 0},
                                    self.TABLE, "tax_type_name", name)
        return row_id, name

    def _ctx(self, name=None):
        row_id, tax_name = self._create_tax(name)
        return {"entity_id": row_id, "entity_name": tax_name, "unique_tax_name": self._unique_tax_name()}
