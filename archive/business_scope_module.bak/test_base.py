"""
test_base.py - 经营范围配置管理模块测试基类
==================================================
提供经营范围配置管理模块的通用测试设置和辅助方法
"""

import time

import pytest
from utils.base_test import BaseTest


class TestBase(BaseTest):
    _module_name = "business_scope_module"
    _module_desc = "经营范围配置管理模块"

    def _unique_scope_name(self):
        """生成唯一的经营范围名称（最长20个字符）"""
        return f"Scope{int(time.time() * 1000) % 100000}"

    def _save_and_get_id(self, scope_name=None, remark=None):
        """新增经营范围并通过分页查询获取ID

        Returns:
            (scope_id, scope_name) 元组
        """
        scope_name = scope_name or self._unique_scope_name()
        return self._create_and_get_id(
            create_fn=lambda: self.client.add_business_scope(
                scope_name=scope_name,
                remark=remark or "TestRemark",
            ),
            query_fn=lambda: self.client.page_business_scopes(page_num=1, page_size=10, scope_name=scope_name),
            match_key="scopeName",
            match_value=scope_name,
        )

    def _delete_test_data(self, item_id):
        """删除测试数据"""
        self.client.delete_business_scope(scope_id=item_id)
