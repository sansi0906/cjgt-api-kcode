"""
test_server_data_driven.py - 服务商端 /server/* 接口数据驱动测试
===============================================================
从 data/server_data.json 读取用例，按 api + method 字段分派原生 HTTP 请求，
并断言 HTTP 状态码与业务码。

占位符约定：
- ${contact_no}   客户联系编号（占位，业务参数缺失场景下值不影响）
- ${work_order_id} 工单ID（占位）
- ${consult_id}   咨询ID（占位）
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import ProviderTestBase

CASES, IDS = load_param_cases("data/server_data.json")

# api 名 -> 接口路径
API_PATHS = {
    "home": "/server/home",
    "customer_page": "/server/customer/page",
    "customer_detail": "/server/customer/detail",
    "customer_declare_config": "/server/customer/declare/config",
    "customer_declare_config_save": "/server/customer/declare/config/save",
    "customer_declare_cycles": "/server/customer/declare/cycles",
    "customer_declare_tax_types": "/server/customer/declare/taxTypes",
    "customer_license_detail": "/server/customer/license/detail",
    "customer_license_upload": "/server/customer/license/upload",
    "knowledge_consult_page": "/server/knowledge/consult/page",
    "knowledge_consult_detail": "/server/knowledge/consult/detail",
    "work_order_page": "/server/workOrder/page",
    "work_order_detail": "/server/workOrder/detail",
    "work_order_accept": "/server/workOrder/accept",
    "work_order_reject": "/server/workOrder/reject",
}


class TestServerDataDriven(ProviderTestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_server_api(self, case):
        """按数据文件中的参数执行服务商端接口测试"""
        api = case["api"]
        if api not in API_PATHS:
            pytest.skip(f"未映射的 api: {api}")

        http_method = (case.get("method") or "POST").upper()
        path = API_PATHS[api]
        payload = dict(case.get("payload") or {})
        payload = self._resolve_placeholders(payload)

        if http_method == "GET":
            response = self.client.get(path, params={k: v for k, v in payload.items() if v is not None})
        else:
            response = self.client.post(path, json=payload)

        self.validator.assert_status_code(response, 200)
        data = response.json()

        if case.get("expect_success"):
            self.assert_api_success(data)
        else:
            self.assert_api_failure(data, expected_code=case.get("expect_code"))

    def _resolve_placeholders(self, payload):
        """解析用例中的占位符为固定测试值"""
        resolved = {}
        for key, value in payload.items():
            if value == "${contact_no}":
                resolved[key] = "CN_TEST_00000001"
            elif value == "${work_order_id}":
                resolved[key] = 99999999
            elif value == "${consult_id}":
                resolved[key] = 99999999
            else:
                resolved[key] = value
        return resolved
