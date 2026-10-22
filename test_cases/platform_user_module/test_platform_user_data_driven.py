"""
test_platform_user_data_driven.py - 平台用户管理数据驱动测试
==============================================================
从 data/platform_user_data.json 读取用例，按接口类型分派调用并断言业务码。

占位符约定：
- ${unique_phone}  本次运行生成的唯一手机号
- ${user_phone}    预置测试用户的手机号
- ${user_id}       预置测试用户的用户ID
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import TestBase

API_PATHS = {
    "save": "/platform/user/save",
    "page": "/platform/user/page",
    "detail": "/platform/user/detail",
    "edit": "/platform/user/edit",
    "change_status": "/platform/user/changeStatus",
    "delete": "/platform/user/delete",
}

CASES, IDS = load_param_cases("data/platform_user_data.json")


class TestPlatformUserDataDriven(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_platform_user_api(self, case):
        """按数据文件中的参数执行平台用户管理接口测试"""
        payload = dict(case.get("payload") or {})
        user_id = None
        user_phone = None

        if case.get("need_user"):
            user_id, user_phone = self._create_user()

        payload = {
            key: self._resolve(value, user_id=user_id, user_phone=user_phone)
            for key, value in payload.items()
        }

        response = self.client.post(API_PATHS[case["api"]], json=payload)
        self.validator.assert_status_code(response, 200)
        data = response.json()

        if case.get("expect_success"):
            self.assert_api_success(data)
            self._assert_side_effect(case, payload, data, user_id, user_phone)
        else:
            self.assert_api_failure(data, expected_code=case.get("expect_code"))

    def _resolve(self, value, user_id=None, user_phone=None):
        """解析用例中的占位符"""
        if value == "${unique_phone}":
            return self._unique_phone()
        if value == "${user_phone}":
            return user_phone
        if value == "${user_id}":
            return user_id
        return value

    def _assert_side_effect(self, case, payload, data, user_id, user_phone):
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
