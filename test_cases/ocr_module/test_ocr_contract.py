"""
test_ocr_contract.py - OCR 识别接口契约校验
=============================================
1. 参数非法时应返回明确的校验错误码（当前后端直接抛系统异常 02）
2. 真实识别场景需要业务提供身份证/营业执照样本图片
"""

import pytest

from .test_base import TestBase

OCR_ENDPOINTS = [
    ("/platform/ocr/lic", "POST", {}),
    ("/platform/ocr/idCardFront", "POST", {}),
    ("/platform/ocr/idCardBack", "POST", {}),
    ("/api/ocr/lic", "POST", {}),
    ("/api/ocr/idCardFront", "POST", {}),
    ("/api/ocr/idCardBack", "POST", {}),
]


class TestOcrContract(TestBase):
    @pytest.mark.parametrize("path,method,payload", OCR_ENDPOINTS, ids=[p[0] for p in OCR_ENDPOINTS])
    @pytest.mark.xfail(reason="Backend bug: OCR 接口未做必填校验，缺参数时返回系统异常(02)")
    @pytest.mark.backend_bug
    def test_ocr_should_validate_required_params(self, path, method, payload):
        """缺少图片参数时应返回 01000006 参数校验错误"""
        response = self.client.post(path, json=payload)
        self.validator.assert_status_code(response, 200)
        self.assert_api_failure(response.json(), expected_code="01000006")

    @pytest.mark.skip(reason="OCR 识别成功场景需要业务提供真实身份证/营业执照图片素材")
    def test_ocr_lic_real_image(self):
        """营业执照识别（真实素材）"""
        pytest.fail("请在 data/ocr_samples/ 下提供真实营业执照图片后启用本用例")
