"""
test_knowledge_base_contract.py - 知识库管理接口契约校验
"""

import pytest

from .test_base import TestBase


class TestKnowledgeBaseContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: changeStatus 对不存在的知识库ID仍返回成功")
    @pytest.mark.backend_bug
    def test_change_status_should_reject_unknown_id(self):
        """不存在的知识库应校验失败"""
        response = self.client.post("/platform/knowledge/changeStatus", json={"id": 99999999, "status": 0})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: delete 对不存在的知识库ID仍返回成功")
    @pytest.mark.backend_bug
    def test_delete_should_reject_unknown_id(self):
        """不存在的知识库应校验失败"""
        response = self.client.post("/platform/knowledge/delete", json={"id": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())
