"""
test_base.py - 超级个体档案管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "super_individual_module"
    _module_desc = "超级个体档案管理模块"

    api_paths = {
        "page": "/platform/workerProfile/page",
        "detail": "/platform/workerProfile/detail/{worker_user_no}",
        "contracts": "/platform/workerProfile/contracts/{worker_user_no}",
        "assignment_records": "/platform/workerProfile/assignmentRecords/{worker_user_no}",
    }

    TABLE = "cjgt_worker_base_info"

    def _sample_worker(self):
        """取一条已存在的超级个体档案作为测试基线数据"""
        row = self.fetch_business_row(
            self.TABLE, "delete_status = 0 AND worker_user_no IS NOT NULL ORDER BY id DESC LIMIT 1")
        if not row:
            import pytest
            pytest.skip("业务库中无可用超级个体档案数据")
        return row

    def _ctx(self):
        row = self._sample_worker()
        return {"worker_user_no": row["worker_user_no"], "worker_phone": row["phone"]}
