"""
test_base.py - 服务工单管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "work_order_module"
    _module_desc = "平台工单管理模块"

    api_paths = {
        "page": "/platform/workOrder/page",
        "detail": "/platform/workOrder/detail",
        "assign": "/platform/workOrder/assign",
        "assign_station": "/platform/workOrder/assignStation",
        "assignments": "/platform/workOrder/assignments",
    }

    TABLE = "cjgt_service_work_order"

    def _sample_work_order(self):
        """取一条已存在的工单作为测试基线数据"""
        row = self.fetch_business_row(self.TABLE, "delete_status = 0 ORDER BY id DESC LIMIT 1")
        if not row:
            import pytest
            pytest.skip("业务库中无可用工单数据")
        return row

    def _ctx(self):
        row = self._sample_work_order()
        return {"work_order_id": row["id"], "work_order_no": row["work_order_no"]}
