"""
test_server_client.py - 服务商端客户端封装方法冒烟测试
======================================================
确保 ProviderClient 各封装方法的路径与参数映射正确，
覆盖 /server/* 接口的核心方法。
"""

import pytest

from .test_base import ProviderTestBase


class TestServerClient(ProviderTestBase):
    """客户端封装方法冒烟测试"""

    def test_client_home(self):
        response = self.client.home()
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_customer_page(self):
        response = self.client.customer_page(page_num=1, page_size=10)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_customer_declare_cycles(self):
        response = self.client.customer_declare_cycles()
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_customer_declare_tax_types(self):
        response = self.client.customer_declare_tax_types()
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_customer_detail_missing_contact_no(self):
        response = self.client.customer_detail(contact_no="")
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data)

    def test_client_knowledge_consult_page(self):
        response = self.client.knowledge_consult_page(page_num=1, page_size=10)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_work_order_page(self):
        response = self.client.work_order_page(page_num=1, page_size=10)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    def test_client_work_order_accept_missing_id(self):
        response = self.client.work_order_accept(work_order_id=0)
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data)

    def test_client_work_order_reject_missing_params(self):
        response = self.client.work_order_reject(work_order_id=0, reject_reason="")
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_api_failure(data)
