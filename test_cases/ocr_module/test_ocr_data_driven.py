"""
test_ocr_data_driven.py - OCR 识别数据驱动测试
=================================================
说明：OCR 识别需要真实身份证/营业执照图片素材，仓库内暂无样本，
当前覆盖"图片不可用/参数非法"场景；识别成功的用例见 test_ocr_contract.py。
"""

import pytest
from utils.module_base import load_cases

from .test_base import TestBase

CASES, IDS = load_cases("data/ocr_data.json")


class TestOcr(TestBase):
    @pytest.mark.parametrize("case", CASES, ids=IDS)
    def test_ocr_api(self, case):
        """按数据文件中的参数执行 OCR 接口测试"""
        self.run_case(case, {"file_uri": "/20260101/invalid.png"})
