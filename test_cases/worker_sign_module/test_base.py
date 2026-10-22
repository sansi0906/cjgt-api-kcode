"""
test_base.py - 超级个体入驻测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "worker_sign_module"
    _module_desc = "超级个体入驻模块"

    api_paths = {
        "worker_save": "/api/worker-sign/worker-save",
        "worker_info": "/api/worker-sign/worker-info",
        "worker_authorization": "/api/worker-sign/worker-authorization",
        "save": "/api/worker-sign/save",
        "station_list": "/api/worker-sign/gongrenle-station-list",
        "station_detail": "/api/worker-sign/gongrenle-station-detail",
        "gongrenle_info": "/api/worker-sign/gongrenle-info",
    }

    def _sample_station_id(self):
        """取一个已存在的驿站ID（用于站点详情查询）"""
        response = self.client.post(self.api_paths["station_list"], json={})
        self.validator.assert_status_code(response, 200)
        data = response.json().get("data") or {}
        stations = data.get("stationsList") or []
        if not stations:
            import pytest
            pytest.skip("业务库中无可用驿站数据")
        first = stations[0]
        return first.get("id") if isinstance(first, dict) else first
