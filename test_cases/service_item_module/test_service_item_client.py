import pytest

from .test_base import TestBase


class TestServiceItemClient(TestBase):
    """客户端封装方法冒烟测试，确保各封装方法的路径与参数映射正确"""

    def test_client_service_item_crud_flow(self):
        item_id, item_name = self._create_item()

        page = self.client.page_service_items(page_num=1, page_size=5)
        self.validator.assert_status_code(page, 200)
        self.assert_api_success(page.json())

        display = self.client.list_display_service_items()
        self.validator.assert_status_code(display, 200)
        self.assert_api_success(display.json())

        hidden = self.client.list_display_service_items(is_display=0)
        self.validator.assert_status_code(hidden, 200)
        self.assert_api_success(hidden.json())

        edit = self.client.edit_service_item(
            item_id, "客户端改名项目", 2, subtitle="客户端副标题", item_desc="客户端介绍")
        self.validator.assert_status_code(edit, 200)
        self.assert_api_success(edit.json())

        status = self.client.update_service_item_status(item_id, 0)
        self.validator.assert_status_code(status, 200)
        self.assert_api_success(status.json())
        row = self._item_row(item_id)
        assert row["is_display"] == 0, f"展示状态未更新: {row}"
