"""
test_base.py - 经营范围配置管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase
from utils.factories import BusinessScopeFactory, UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "business_scope_module"
    _module_desc = "经营范围配置管理模块"

    api_paths = {
        "add": "/platform/businessScope/add",
        "paging": "/platform/businessScope/paging",
        "edit": "/platform/businessScope/edit",
        "update_status": "/platform/businessScope/updateStatus",
        "delete": "/platform/businessScope/del",
    }

    TABLE = "cjgt_business_scope"

    @staticmethod
    def _unique_scope_name():
        return UniqueValueFactory.unique_scope_name()

    def _create_scope(self, name=None):
        name = name or self._unique_scope_name()
        params = BusinessScopeFactory.build_add_params(scopeName=name, remark="自动化备注")
        row_id = self.create_by_api("add", params,
                                    self.TABLE, "scope_name", name)
        return row_id, name

    def _ctx(self, name=None):
        row_id, scope_name = self._create_scope(name)
        return {"entity_id": row_id, "entity_name": scope_name, "unique_scope_name": self._unique_scope_name()}
