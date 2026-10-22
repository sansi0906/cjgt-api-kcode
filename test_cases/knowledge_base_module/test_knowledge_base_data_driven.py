"""
test_knowledge_base_data_driven.py - 知识库管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/knowledge_base_data.json")


class TestKnowledgeBase(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_knowledge_api(self, case):
        """按数据文件中的参数执行知识库接口测试"""
        ctx = self._ctx() if case.get("need_entity") else {"unique_title": self._unique_title()}
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "save":
            row = self.fetch_business_row(self.TABLE, "title = %s", (payload["title"],))
            assert row, f"知识库未落库: {payload['title']}"
            self.register_business_row(self.TABLE, row["id"])
        elif case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["title"] == payload["title"], f"标题未更新: {row}"
            assert row["consult_type"] == payload["consultType"], f"咨询类型未更新: {row}"
        elif case["api"] == "change_status":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["status"] == payload["status"], f"状态未更新: {row}"
