import pytest

from .test_base import TestBase


class TestRoleClient(TestBase):
    """客户端封装方法冒烟测试，确保各封装方法的路径与参数映射正确"""

    def test_client_role_crud_flow(self):
        role_id, role_name, role_no = self._create_role()

        page = self.client.page_roles(page_num=1, page_size=5)
        self.validator.assert_status_code(page, 200)
        self.assert_api_success(page.json())

        detail = self.client.get_role_detail(role_id)
        self.validator.assert_status_code(detail, 200)
        self.assert_api_success(detail.json())

        edit = self.client.edit_role(role_id, "客户端改名角色", role_no, status=1, role_remark="客户端编辑")
        self.validator.assert_status_code(edit, 200)
        self.assert_api_success(edit.json())

        status = self.client.change_role_status(role_id, 0)
        self.validator.assert_status_code(status, 200)
        self.assert_api_success(status.json())

        menus = self.client.select_menus_by_role_id(role_id)
        self.validator.assert_status_code(menus, 200)
        self.assert_api_success(menus.json())

        assign = self.client.add_role_menu(role_id, [])
        self.validator.assert_status_code(assign, 200)
        self.assert_api_success(assign.json())

        all_roles = self.client.select_role_all()
        self.validator.assert_status_code(all_roles, 200)
        self.assert_api_success(all_roles.json())

        delete = self.client.delete_role(role_id)
        self.validator.assert_status_code(delete, 200)
        self.assert_api_success(delete.json())
