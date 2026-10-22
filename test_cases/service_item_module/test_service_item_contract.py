"""
test_service_item_contract.py - 服务项目配置接口契约校验
========================================================
覆盖 Swagger 声明的取值约束，与后端实际行为不一致的用例标记为 backend_bug / xfail。
"""

import pytest

from .test_base import TestBase


class TestServiceItemContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: billingMethod 非法取值未校验")
    @pytest.mark.backend_bug
    def test_add_should_reject_invalid_billing_method(self):
        """billingMethod 仅允许 1/2，非法值应校验失败"""
        item_code = self._unique_item_code()
        try:
            response = self.client.post("/platform/serviceItem/add", json={
                "itemName": self._unique_item_name(),
                "billingMethod": 5,
                "itemCode": item_code,
            })
            self.validator.assert_status_code(response, 200)
            self.assert_api_failure(response.json())
        finally:
            row = self.fetch_business_row("cjgt_service_item", "item_code = %s", (item_code,))
            if row:
                self.delete_business_row("cjgt_service_item", row["id"])

    @pytest.mark.xfail(reason="Backend bug: 服务项目名称重复未校验")
    @pytest.mark.backend_bug
    def test_add_should_reject_duplicate_name(self):
        """同名服务项目应校验失败"""
        item_code = self._unique_item_code()
        try:
            response = self.client.post("/platform/serviceItem/add", json={
                "itemName": self._unique_item_name(),
                "billingMethod": 1,
                "itemCode": item_code,
            })
            self.validator.assert_status_code(response, 200)
            self.assert_api_failure(response.json())
        finally:
            row = self.fetch_business_row("cjgt_service_item", "item_code = %s", (item_code,))
            if row:
                self.delete_business_row("cjgt_service_item", row["id"])

    @pytest.mark.xfail(reason="Backend bug: updateStatus 非法 isDisplay 未校验")
    @pytest.mark.backend_bug
    def test_update_status_should_reject_invalid_is_display(self):
        """isDisplay 仅允许 0/1"""
        item_id, _ = self._create_item()
        response = self.client.post("/platform/serviceItem/updateStatus", json={"id": item_id, "isDisplay": 9})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    def test_edit_should_reject_unknown_item(self):
        """编辑不存在的服务项目应返回失败（错误码 01000025）"""
        response = self.client.post("/platform/serviceItem/edit", json={
            "id": 99999999,
            "itemName": self._unique_item_name(),
            "billingMethod": 1,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000025")

    @pytest.mark.xfail(reason="Backend bug: edit 不存在的项目ID错误文案为“菜单不存在”")
    @pytest.mark.backend_bug
    def test_edit_unknown_item_error_message(self):
        """错误文案应为“服务项目不存在”"""
        response = self.client.post("/platform/serviceItem/edit", json={
            "id": 99999999,
            "itemName": self._unique_item_name(),
            "billingMethod": 1,
        })
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data, expected_code="01000025")
        assert "服务项目不存在" in (data.get("message") or ""), \
            f"错误文案不正确: {data.get('message')}"

    def test_update_status_should_reject_unknown_item(self):
        """切换不存在的服务项目展示状态应返回失败（错误码 01000025）"""
        response = self.client.post("/platform/serviceItem/updateStatus", json={"id": 99999999, "isDisplay": 1})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000025")

    @pytest.mark.xfail(reason="Backend bug: updateStatus 不存在的项目ID错误文案为“菜单不存在”")
    @pytest.mark.backend_bug
    def test_update_status_unknown_item_error_message(self):
        """错误文案应为“服务项目不存在”"""
        response = self.client.post("/platform/serviceItem/updateStatus", json={"id": 99999999, "isDisplay": 1})
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data, expected_code="01000025")
        assert "服务项目不存在" in (data.get("message") or ""), \
            f"错误文案不正确: {data.get('message')}"

    @pytest.mark.xfail(reason="Backend bug: paging 带创建时间区间时后端返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_paging_should_support_time_range(self):
        """按创建时间区间查询应正常返回"""
        response = self.client.post("/platform/serviceItem/paging", json={
            "pageNum": 1,
            "pageSize": 10,
            "startTime": "2020-01-01 00:00:00",
            "endTime": "2030-01-01 00:00:00",
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
