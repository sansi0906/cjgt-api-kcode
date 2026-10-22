"""
test_base.py - 文件管理测试基类
"""

import os
from utils.module_base import DataDrivenApiTestBase


# 1x1 像素 PNG（十六进制常量，已验证后端可正常解析上传）
TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c63000100000500010d0a2db4"
    "0000000049454e44ae426082"
)


class TestBase(DataDrivenApiTestBase):
    _module_name = "file_module"
    _module_desc = "文件管理模块"

    api_paths = {
        "upload": "/sys/file/upload",
        "original_name": "/sys/file/original-name",
        "download": "/sys/file/download",
        "pub_original_name": "/sys/file/pub/original-name",
        "pub_download": "/sys/file/pub/download",
        "api_download": "/api/file/download",
        "api_pub_download": "/api/file/pub/download",
    }

    def _upload_sample(self):
        """上传测试文件，返回文件 uri"""
        response = self.client.post_files(
            "/sys/file/upload",
            files={"file": ("kilo_test.png", TINY_PNG, "image/png")},
        )
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        return response.json()["data"]["uri"]
