"""
test_agreement_data_driven.py - 用户协议管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/agreement_data.json")


class TestAgreement(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_agreement_api(self, case):
        """按数据文件中的参数执行用户协议接口测试"""
        if case.get("free_agreement_type"):
            # 业务约束：每种协议类型仅允许一条，先让出该类型
            backup = self._backup_agreement(case["free_agreement_type"])
            try:
                ctx = {"unique_agreement_name": self._unique_agreement_name()}
                self.run_case(case, ctx)
                row = self.fetch_business_row(self.TABLE, "agreement_name = %s",
                                             (ctx["unique_agreement_name"],))
                if row:
                    self.register_business_row(self.TABLE, row["id"])
            finally:
                # 先移除本次新建的协议，避免与恢复的备份冲突（agreement_type 唯一约束）
                new_row = self.fetch_business_row(self.TABLE, "agreement_name = %s",
                                                 (ctx["unique_agreement_name"],))
                if new_row:
                    self.delete_business_row(self.TABLE, new_row["id"])
                self._restore_agreement(backup)
            return

        ctx = self._ctx() if case.get("need_entity") else {"unique_agreement_name": self._unique_agreement_name()}
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "edit":
            row = self.entity_row(self.TABLE, payload["id"])
            assert row["agreement_name"] == payload["agreementName"], f"协议名称未更新: {row}"
            assert row["agreement_content"] == payload["agreementContent"], f"协议内容未更新: {row}"
