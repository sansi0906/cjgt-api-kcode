"""
test_base.py - 服务项目配置测试基类
====================================
提供服务项目配置模块的通用造数、清理与断言辅助方法
"""

import uuid

import pytest
from utils.base_test import BaseTest


class TestBase(BaseTest):
    _module_name = "service_item_module"
    _module_desc = "服务项目配置管理模块"

    @staticmethod
    def _unique_item_name():
        """生成唯一服务项目名称（后端限制最多 10 个字）"""
        return "自动化" + str(uuid.uuid4().int % 10**6).zfill(6)

    @staticmethod
    def _unique_item_code():
        return "AUTO" + str(uuid.uuid4().int % 10**8).zfill(8)

    def _create_item(self, item_name=None, billing_method=1, item_code=None):
        """创建服务项目，返回 (item_id, item_name)"""
        item_name = item_name or self._unique_item_name()
        item_code = item_code or self._unique_item_code()
        response = self.client.add_service_item(
            item_name=item_name,
            billing_method=billing_method,
            subtitle="自动化副标题",
            item_desc="自动化介绍",
            item_code=item_code,
        )
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row("cjgt_service_item", "item_code = %s", (item_code,))
        assert row, f"创建服务项目未落库: {item_code}"
        self.register_business_row("cjgt_service_item", row["id"])
        return row["id"], item_name

    def _item_row(self, item_id):
        return self.fetch_business_row("cjgt_service_item", "id = %s", (item_id,))
