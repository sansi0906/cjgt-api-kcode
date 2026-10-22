"""
test_worker_sign_contract.py - 超级个体入驻接口契约校验
"""

import pytest

from .test_base import TestBase


class TestWorkerSignContract(TestBase):
    @pytest.mark.xfail(reason="Backend bug: gongrenle-info 返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_gongrenle_info_should_return_data(self):
        """工人乐查询用户详情应正常返回"""
        response = self.client.get("/api/worker-sign/gongrenle-info", params={"phone": "15810299672"})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())

    @pytest.mark.xfail(reason="Backend bug: gongrenle-station-detail 返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_station_detail_should_return_data(self):
        """工人乐查询驿站详情应正常返回"""
        station_id = self._sample_station_id()
        response = self.client.get("/api/worker-sign/gongrenle-station-detail", params={"businessId": station_id})
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
