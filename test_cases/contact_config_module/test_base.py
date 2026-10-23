"""
test_base.py - 合同服务配置管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase
from utils.factories import UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "contact_config_module"
    _module_desc = "合同服务配置管理模块"

    api_paths = {
        "save": "/platform/contactConfig/save",
        "paging": "/platform/contactConfig/paging",
        "edit": "/platform/contactConfig/edit",
        "detail": "/platform/contactConfig/detail",
        "delete": "/platform/contactConfig/delete",
    }

    TABLE = "cjgt_contact_config"
    ITEM_TABLE = "cjgt_service_item"

    @staticmethod
    def _unique_title():
        return UniqueValueFactory.unique_title("合同服务")

    def _create_service_item(self):
        """新建服务项目（业务约束：一个服务项目仅允许一条合同服务配置）"""
        item_name = UniqueValueFactory.unique_name("合同项")
        item_code = UniqueValueFactory.unique_item_code()
        response = self.client.post("/platform/serviceItem/add", json={
            "itemName": item_name, "billingMethod": 1, "itemCode": item_code,
        })
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row(self.ITEM_TABLE, "item_name = %s", (item_name,))
        assert row, f"服务项目未落库: {item_name}"
        self.register_business_row(self.ITEM_TABLE, row["id"])
        return row["id"]

    def _create_contact(self, service_item_id=None):
        """新增合同服务，返回 (id, title)"""
        service_item_id = service_item_id or self._create_service_item()
        title = self._unique_title()
        row_id = self.create_by_api("save", {
            "title": title,
            "serviceItemId": service_item_id,
            "content": "合同服务内容",
            "priceContent": "价格内容",
        }, self.TABLE, "title", title)
        return row_id, title, service_item_id

    def _ctx(self, with_item=False):
        row_id, title, item_id = self._create_contact()
        ctx = {"entity_id": row_id, "entity_name": title, "unique_title": self._unique_title(),
               "service_item_id": item_id}
        if with_item:
            ctx["extra_service_item_id"] = self._create_service_item()
        return ctx
