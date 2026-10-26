"""
test_base.py - 服务项目配置测试基类
====================================
提供服务项目配置模块的通用造数、清理与断言辅助方法
"""

import pytest
from utils.module_base import DataDrivenApiTestBase
from utils.factories import ServiceItemFactory, UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "service_item_module"
    _module_desc = "服务项目配置管理模块"

    api_paths = {
        "add": "/platform/serviceItem/add",
        "paging": "/platform/serviceItem/paging",
        "list_display": "/platform/serviceItem/listDisplay",
        "edit": "/platform/serviceItem/edit",
        "update_status": "/platform/serviceItem/updateStatus",
    }

    @staticmethod
    def _unique_item_name():
        """生成唯一服务项目名称（后端限制最多 10 个字）"""
        return UniqueValueFactory.unique_item_name()

    @staticmethod
    def _unique_item_code():
        return UniqueValueFactory.unique_item_code()

    def _create_item(self, item_name=None, billing_method=1, item_code=None):
        """创建服务项目，返回 (item_id, item_name)"""
        item_name = item_name or self._unique_item_name()
        item_code = item_code or self._unique_item_code()
        params = ServiceItemFactory.build_add_params(
            item_name=item_name,
            billing_method=billing_method,
            subtitle="自动化副标题",
            item_desc="自动化介绍",
            item_code=item_code,
        )
        response = self.client.add_service_item(**params)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row("cjgt_service_item", "item_code = %s", (item_code,))
        assert row, f"创建服务项目未落库: {item_code}"
        self.register_business_row("cjgt_service_item", row["id"])
        return row["id"], item_name

    def _item_row(self, item_id):
        return self.fetch_business_row("cjgt_service_item", "id = %s", (item_id,))

    def _ctx(self, item_id=None, item_name=None):
        """造数上下文：need_item 时创建项目，返回 factories 生成的值"""
        if item_id is None:
            item_id, item_name = self._create_item()
        return {
            "item_id": item_id,
            "item_name": item_name,
            "unique_item_name": self._unique_item_name(),
            "unique_item_code": self._unique_item_code(),
        }
