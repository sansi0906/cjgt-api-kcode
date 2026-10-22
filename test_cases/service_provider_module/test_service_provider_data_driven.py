"""
test_service_provider_data_driven.py - 服务商管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/service_provider_data.json")


class TestServiceProvider(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_service_provider_api(self, case):
        """按数据文件中的参数执行服务商管理接口测试"""
        ctx = self._ctx() if case.get("need_entity") else {
            "unique_phone": self._unique_phone(),
            "unique_company_name": self._unique_company_name(),
            "unique_uscc": self._unique_uscc(),
        }
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        api = case["api"]
        if api == "save":
            row = self.fetch_business_row(self.TABLE, "contact_phone = %s", (payload["contactPhone"],))
            assert row, f"服务商未落库: {payload['contactPhone']}"
            self.register_business_row(self.TABLE, row["id"])
            assert row["company_name"] == payload["companyName"], f"公司名称未落库: {row}"
        elif api == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["company_name"] == payload["companyName"], f"公司名称未更新: {row}"
            assert row["contact_person"] == payload["contactPerson"], f"联系人未更新: {row}"
        elif api == "change_status":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["status"] == payload["status"], f"服务商状态未更新: {row}"
