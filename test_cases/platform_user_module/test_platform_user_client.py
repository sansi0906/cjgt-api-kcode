import pytest

from .test_base import TestBase


class TestPlatformUserClient(TestBase):
    """客户端封装方法冒烟测试，确保各封装方法的路径与参数映射正确"""

    def test_client_page_users(self):
        response = self.client.page_users(page_num=1, page_size=5)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_user_crud_flow(self):
        user_id, phone = self._create_user()

        detail = self.client.get_user_detail(user_id)
        self.validator.assert_status_code(detail, 200)
        self.assert_api_success(detail.json())

        edit = self.client.edit_user(user_id, phone, "客户端改名用户", sex=0, role_group_id=5, status=1)
        self.validator.assert_status_code(edit, 200)
        self.assert_api_success(edit.json())

        status = self.client.change_user_status(user_id, 0)
        self.validator.assert_status_code(status, 200)
        self.assert_api_success(status.json())

        delete = self.client.delete_user(user_id)
        self.validator.assert_status_code(delete, 200)
        self.assert_api_success(delete.json())
