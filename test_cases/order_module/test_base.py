"""
test_base.py - 订单管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "order_module"
    _module_desc = "平台订单管理模块"

    api_paths = {
        "page": "/platform/order/page",
        "detail": "/platform/order/detail",
        "check_provider": "/platform/order/checkProvider",
        "upload_voucher": "/platform/order/uploadVoucher",
    }

    TABLE = "cjgt_order"

    def _sample_order(self):
        """取一条已存在的订单作为测试基线数据"""
        row = self.fetch_business_row(self.TABLE, "delete_status = 0 ORDER BY id DESC LIMIT 1")
        if not row:
            import pytest
            pytest.skip("业务库中无可用订单数据")
        return row

    def _order_without_contract(self):
        """取一条未关联签约信息的订单"""
        row = self.fetch_business_row(
            self.TABLE,
            "delete_status = 0 AND contact_no NOT IN (SELECT contact_no FROM cjgt_worker_sign WHERE contact_no IS NOT NULL) "
            "ORDER BY id LIMIT 1",
        )
        if not row:
            import pytest
            pytest.skip("业务库中无可用订单数据")
        return row

    def _ctx(self):
        row = self._sample_order()
        return {"order_id": row["id"], "order_no": row["order_no"]}

    def _ctx_without_contract(self):
        row = self._order_without_contract()
        return {"order_id": row["id"], "order_no": row["order_no"]}
