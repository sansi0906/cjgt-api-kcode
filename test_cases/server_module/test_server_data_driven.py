"""
test_server_data_driven.py - 服务商端 /server/* 接口数据驱动测试
===============================================================
从 data/server_data.json 读取用例，复用 DataDrivenApiTestBase.run_case
进行接口分派、占位符替换、状态码与业务码断言。

占位符约定（通过 SERVER_CTX 传入 run_case）：
- ${contact_no}   客户联系编号
- ${work_order_id} 工单ID
- ${consult_id}   咨询ID
"""

import pytest
from utils.data_driver import load_param_cases

from .test_base import ProviderTestBase

CASES, IDS = load_param_cases("data/server_data.json")

# 服务商端占位符固定测试值，透传给 run_case 做 ${key} 替换
SERVER_CTX = {
    "contact_no": "CN_TEST_00000001",
    "work_order_id": 99999999,
    "consult_id": 99999999,
}


class TestServerDataDriven(ProviderTestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_server_api(self, case):
        """按数据文件中的参数执行服务商端接口测试"""
        self.run_case(case, SERVER_CTX)
