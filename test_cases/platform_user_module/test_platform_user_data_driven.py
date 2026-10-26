"""
test_platform_user_data_driven.py - 平台用户管理数据驱动测试
============================================================
从 data/platform_user_data.json 读取用例，按接口类型分派调用并断言业务码。

占位符约定：
- ${unique_phone}  本次运行生成的唯一手机号
- ${user_phone}    预置测试用户的手机号
- ${user_id}       预置测试用户的用户ID
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import TestBase

CASES, IDS = load_param_cases("data/platform_user_data.json")


class TestPlatformUserDataDriven(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_platform_user_api(self, case):
        """按数据文件中的参数执行平台用户管理接口测试"""
        ctx = self._ctx() if case.get("need_user") else {
            "unique_phone": self._unique_phone(),
        }
        self.run_case(case, ctx)

    def assert_side_effect(self, case, payload, data, ctx):
        """校验接口成功后的数据落库情况"""
        api = case["api"]
        if api == "save":
            row = self.fetch_business_row("cjgt_platform_user", "user_name = %s", (payload["userName"],))
            assert row, f"新增用户未落库: {payload['userName']}"
            self.register_business_row("cjgt_platform_user", row["id"])
        elif api == "edit":
            row = self.fetch_business_row("cjgt_platform_user", "id = %s", (payload["id"],))
            assert row["real_name"] == payload["realName"], f"真实姓名未更新: {row}"
            assert row["sex"] == payload["sex"], f"性别未更新: {row}"
        elif api == "change_status":
            row = self.fetch_business_row("cjgt_platform_user", "id = %s", (payload["id"],))
            assert row["status"] == payload["status"], f"状态未更新: {row}"
        elif api == "delete":
            row = self.fetch_business_row("cjgt_platform_user", "id = %s", (payload["id"],))
            assert row["delete_status"] == 1, f"删除状态未更新: {row}"
        elif api == "page":
            result = data.get("result") or data.get("data") or {}
            assert "records" in result or "list" in result, f"分页结果结构异常: {data}"
