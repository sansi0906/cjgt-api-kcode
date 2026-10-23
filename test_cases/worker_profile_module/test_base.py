"""
test_base.py - 工作者档案测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "worker_profile_module"
    _module_desc = "工作者档案模块"

    api_paths = {
        "page": "/platform/workerProfile/page",
        "detail": "/platform/workerProfile/detail/{workerUserNo}",
        "assignment_records": "/platform/workerProfile/assignmentRecords/{workerUserNo}",
        "contracts": "/platform/workerProfile/contracts/{workerUserNo}",
    }

    def _get_worker_user_no(self):
        """从 workerProfile 分页列表中取一个有效的 workerUserNo"""
        response = self.client.post(self.api_paths["page"], json={"pageNum": 1, "pageSize": 1})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        records = response.json().get("data", {}).get("records", [])
        assert records, "workerProfile 列表为空，无法获取 workerUserNo"
        return records[0]["workerUserNo"]
