"""
test_service_item_data_driven.py - 服务项目配置数据驱动测试
============================================================
从 data/service_item_data.json 读取用例，覆盖 5 个服务项目接口的正向与逆向场景。

占位符约定：
- ${unique_item_name}  本次运行生成的唯一服务项目名称
- ${unique_item_code}  本次运行生成的唯一服务项目编码
- ${item_id}           预置测试项目的ID
- ${item_name}         预置测试项目的名称
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import TestBase

API_PATHS = {
    "add": "/platform/serviceItem/add",
    "paging": "/platform/serviceItem/paging",
    "list_display": "/platform/serviceItem/listDisplay",
    "edit": "/platform/serviceItem/edit",
    "update_status": "/platform/serviceItem/updateStatus",
}

CASES, IDS = load_param_cases("data/service_item_data.json")


class TestServiceItemDataDriven(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_service_item_api(self, case):
        """按数据文件中的参数执行服务项目配置接口测试"""
        item_id = None
        item_name = None

        if case.get("need_item"):
            item_id, item_name = self._create_item()

        payload = {
            key: self._resolve(value, item_id=item_id, item_name=item_name)
            for key, value in (case.get("payload") or {}).items()
        }

        response = self.client.post(API_PATHS[case["api"]], json=payload)
        self.validator.assert_status_code(response, 200)
        data = response.json()

        if case.get("expect_success"):
            self.assert_api_success(data)
            self._assert_side_effect(case, payload, data, item_id)
        else:
            self.assert_api_failure(data, expected_code=case.get("expect_code"))

    def _resolve(self, value, item_id=None, item_name=None):
        """解析占位符，支持整串占位与内嵌占位"""
        if not isinstance(value, str) or "${" not in value:
            return value
        mapping = {
            "${unique_item_name}": self._unique_item_name(),
            "${unique_item_code}": self._unique_item_code(),
            "${item_id}": item_id,
            "${item_name}": item_name,
        }
        for key, val in mapping.items():
            if key in value:
                value = value.replace(key, "" if val is None else str(val))
        return value

    def _assert_side_effect(self, case, payload, data, item_id):
        """校验接口成功后的落库情况"""
        api = case["api"]
        if api == "add":
            row = self.fetch_business_row("cjgt_service_item", "item_code = %s", (payload["itemCode"],))
            assert row, f"新增服务项目未落库: {payload['itemCode']}"
            assert row["item_name"] == payload["itemName"], f"项目名称未落库: {row}"
            assert row["billing_method"] == payload["billingMethod"], f"计费方式未落库: {row}"
            self.register_business_row("cjgt_service_item", row["id"])
        elif api == "edit":
            row = self._item_row(payload["id"])
            assert row["item_name"] == payload["itemName"], f"项目名称未更新: {row}"
            assert row["billing_method"] == payload["billingMethod"], f"计费方式未更新: {row}"
            assert row["subtitle"] == payload["subtitle"], f"副标题未更新: {row}"
        elif api == "update_status":
            row = self._item_row(payload["id"])
            assert row["is_display"] == payload["isDisplay"], f"展示状态未更新: {row}"
        elif api == "paging":
            result = data.get("result") or data.get("data") or {}
            assert "records" in result or "list" in result, f"分页结果结构异常: {data}"
        elif api == "list_display":
            items = data.get("data") or data.get("result") or []
            assert isinstance(items, list), f"列表结果结构异常: {data}"
