"""
test_base.py - 菜单管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase
from utils.factories import UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "menu_module"
    _module_desc = "菜单管理模块"

    api_paths = {
        "paging": "/common/menu/paging",
        "menu_tree_sel": "/common/menu/menuTreeSel",
        "menu_tree_sel_all": "/common/menu/menuTreeSelAll",
        "get": "/common/menu/get",
        "edit": "/common/menu/edit",
        "delete": "/common/menu/del",
        "add": "/common/menu/add",
    }

    TABLE = "cjgt_menu"

    @staticmethod
    def _unique_menu_name():
        return UniqueValueFactory.unique_menu_name()

    def _create_menu(self, name=None):
        name = name or self._unique_menu_name()
        row_id = self.create_by_api("add", {
            "menuName": name, "menuType": "C", "parentId": 0, "webType": 0,
        }, self.TABLE, "menu_name", name)
        return row_id, name

    def _ctx(self, name=None):
        row_id, menu_name = self._create_menu(name)
        return {"entity_id": row_id, "entity_name": menu_name, "unique_menu_name": self._unique_menu_name()}
