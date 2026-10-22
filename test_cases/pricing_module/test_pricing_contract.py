"""
test_pricing_contract.py - 服务定价配置管理接口契约校验
"""

import pytest

from .test_base import TestBase


class TestPricingContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: tree 对不存在的服务项目仍返回成功")
    @pytest.mark.backend_bug
    def test_tree_should_reject_unknown_service_item(self):
        """不存在的服务项目应校验失败"""
        response = self.client.post("/platform/pricing/tree", json={"serviceItemId": 99999999})
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json())

    @pytest.mark.xfail(reason="Backend bug: 导入服务定价 Excel 返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_import_pricing_excel(self):
        """导入服务定价 Excel（multipart 上传）"""
        import os
        excel = os.path.join("data", "服务定价数据.xlsx")
        if not os.path.exists(excel):
            pytest.skip("缺少定价导入用的 Excel 模板文件")
        with open(excel, "rb") as f:
            response = self.client.post_files(
                "/platform/pricing/import",
                files={"file": ("服务定价数据.xlsx", f,
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                data={"serviceItemId": self.SERVICE_ITEM_ID, "effectiveTime": "2027-01-01 00:00:00"},
            )
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
