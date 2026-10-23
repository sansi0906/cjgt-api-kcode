"""
test_base.py - 服务商管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase
from utils.factories import ServiceProviderFactory, UniqueValueFactory


class TestBase(DataDrivenApiTestBase):
    _module_name = "service_provider_module"
    _module_desc = "服务商管理模块"

    api_paths = {
        "save": "/platform/serverUser/save",
        "page": "/platform/serverUser/page",
        "edit": "/platform/serverUser/edit",
        "detail": "/platform/serverUser/detail",
        "delete": "/platform/serverUser/delete",
        "change_status": "/platform/serverUser/changeStatus",
        "reset_pwd": "/platform/serverUser/resetPwd",
    }

    TABLE = "cjgt_service_provider"

    OFFICE = [{"code": "120000000000", "name": "天津市", "level": "province"},
              {"code": "120100000000", "name": "天津市", "level": "city"},
              {"code": "120113000000", "name": "东丽区", "level": "county"}]

    @staticmethod
    def _unique_phone():
        """11 位手机号（后端对联系电话做数值校验，长度非法会报 01000044）"""
        return UniqueValueFactory.unique_phone()

    @staticmethod
    def _unique_company_name():
        return UniqueValueFactory.unique_company_name()

    @staticmethod
    def _unique_uscc():
        return UniqueValueFactory.unique_uscc()

    def _create_provider(self):
        """新增服务商，返回 (id, phone, company_name, uscc)"""
        phone = self._unique_phone()
        company_name = self._unique_company_name()
        uscc = self._unique_uscc()
        params = ServiceProviderFactory.build_save_payload(
            companyName=company_name,
            unifiedSocialCode=uscc,
            officeAddress=self.OFFICE,
            officeAddressDetail="自动化办公地址",
            serviceArea=self.OFFICE,
            contactPerson="自动化联系人",
            contactPhone=phone,
            serviceItems=[1],
        )
        row_id = self.create_by_api("save", params,
                                    self.TABLE, "contact_phone", phone)
        return row_id, phone, company_name, uscc

    def _ctx(self):
        row_id, phone, company_name, uscc = self._create_provider()
        return {
            "entity_id": row_id,
            "entity_phone": phone,
            "entity_name": company_name,
            "entity_uscc": uscc,
            "unique_phone": self._unique_phone(),
            "unique_company_name": self._unique_company_name(),
            "unique_uscc": self._unique_uscc(),
        }
