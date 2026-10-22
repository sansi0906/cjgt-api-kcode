"""
test_base.py - OCR 识别测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "ocr_module"
    _module_desc = "OCR 识别模块"

    api_paths = {
        "platform_lic": "/platform/ocr/lic",
        "platform_id_card_front": "/platform/ocr/idCardFront",
        "platform_id_card_back": "/platform/ocr/idCardBack",
        "platform_identify": "/platform/ocr/identify",
        "api_lic": "/api/ocr/lic",
        "api_id_card_front": "/api/ocr/idCardFront",
        "api_id_card_back": "/api/ocr/idCardBack",
        "api_identify": "/api/ocr/identify",
    }
