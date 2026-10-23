"""
test_pricing_data_driven.py - 服务定价配置管理数据驱动测试
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/pricing_data.json")


class TestPricing(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_pricing_api(self, case):
        """按数据文件中的参数执行服务定价接口测试"""
        ctx = self._ctx()
        payload_ctx = dict(ctx)

        # 仅对标记 need_pricing 的用例，用 factories 生成的值覆盖 case payload 中已存在的字段
        # 保留原本缺失的字段（如 missing_service_item_id 不应包含 serviceItemId）
        case_payload = dict(case.get("payload") or {})
        if case.get("need_pricing"):
            factory_payload = ctx.get("pricing_payload", {})
            for key in list(case_payload.keys()):
                if key in factory_payload:
                    case_payload[key] = factory_payload[key]
        case_with_factory_payload = dict(case)
        case_with_factory_payload["payload"] = case_payload

        row = self._pricing_row()
        original = (row["pending_amount"], row["effective_time"]) if row else (None, None)

        try:
            self.run_case(case_with_factory_payload, payload_ctx)
        finally:
            # 还原待生效金额与生效时间，避免污染业务数据
            if row and original != (row["pending_amount"], row["effective_time"]):
                self.update_business_row(self.TABLE, row["id"], {
                    "pending_amount": original[0], "effective_time": original[1],
                })

    def assert_side_effect(self, case, payload, data, ctx):
        if case["api"] == "update_pricing":
            row = self._pricing_row()
            assert row is not None, "定价记录不存在"
            assert float(row["pending_amount"]) == float(payload["pendingAmount"]), \
                f"待生效金额未更新: {row}"
