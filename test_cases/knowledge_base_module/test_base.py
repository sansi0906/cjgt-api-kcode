"""
test_base.py - 知识库管理测试基类
"""

import uuid

from utils.module_base import DataDrivenApiTestBase
from utils.factories import KnowledgeBaseFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "knowledge_base_module"
    _module_desc = "知识库管理模块"

    api_paths = {
        "save": "/platform/knowledge/save",
        "page": "/platform/knowledge/page",
        "edit": "/platform/knowledge/edit",
        "detail": "/platform/knowledge/detail",
        "delete": "/platform/knowledge/delete",
        "change_status": "/platform/knowledge/changeStatus",
    }

    TABLE = "cjgt_knowledge_base"

    @staticmethod
    def _unique_title():
        return "自动化知识" + str(uuid.uuid4().int % 10**6).zfill(6)

    def _create_knowledge(self, title=None):
        title = title or self._unique_title()
        params = KnowledgeBaseFactory.build_save_payload(
            title=title,
            content="知识内容",
            consultType=1,
            displayPosition=[0, 1],
            applicableArea=[{"provinceAreaCode": "120000", "provinceAreaName": "天津市",
                           "cityAreaCode": "120100", "cityAreaName": "天津市",
                           "districtAreaCode": "120101", "districtAreaName": "和平区"}],
        )
        row_id = self.create_by_api("save", params,
                                    self.TABLE, "title", title)
        return row_id, title

    def _ctx(self, title=None):
        row_id, knowledge_title = self._create_knowledge(title)
        return {"entity_id": row_id, "entity_name": knowledge_title, "unique_title": self._unique_title()}
