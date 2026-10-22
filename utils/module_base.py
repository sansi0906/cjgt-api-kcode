"""
module_base.py - 通用数据驱动模块基类
========================================
把"数据驱动 + 分派调用 + 落库断言 + 自动清理"这套模式沉淀到框架层，
各业务模块只需声明接口路径映射与造数逻辑即可。
"""

import pytest
from utils.base_test import BaseTest
from utils.data_driver import load_param_cases


# 1x1 像素 PNG（十六进制常量，已验证后端可正常解析上传）
TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c63000100000500010d0a2db4"
    "0000000049454e44ae426082"
)


def load_cases(data_file, id_key="desc"):
    """加载数据驱动用例，返回 (cases, ids)"""
    return load_param_cases(data_file, id_key=id_key)


class DataDrivenApiTestBase(BaseTest):
    """数据驱动接口测试基类

    子类需声明：
    - api_paths: {api_key: "/path/to/api"}
    - _module_name / _module_desc
    """

    api_paths = {}

    def run_case(self, case, ctx=None):
        """按用例定义分派调用接口并断言

        Args:
            case: 单条用例数据
            ctx: 造数上下文（如 {"id": 1, "phone": "..."}），用于占位符替换
        """
        ctx = ctx or {}
        payload = {
            key: self._resolve(value, ctx)
            for key, value in (case.get("payload") or {}).items()
        }
        api = case["api"]
        assert api in self.api_paths, f"未声明接口路径: {api}"
        path = self.api_paths[api]
        if "{" in path:
            # 路径参数占位（如 /detail/{worker_user_no}）
            path = path.format(**{k: v for k, v in (ctx or {}).items() if v is not None})

        method = (case.get("method") or "POST").upper()
        if case.get("upload"):
            files, form = self._upload_payload(case)
            response = self.client.post_files(path, files=files, data=form)
        elif method == "GET":
            response = self.client.get(path, params={k: v for k, v in payload.items() if v is not None})
        else:
            response = self.client.post(path, json=payload)
        self.validator.assert_status_code(response, 200)
        if case.get("raw"):
            # 文件下载等二进制响应：仅断言状态码与响应类型
            content_type = (response.headers.get("Content-Type") or "").lower()
            if case.get("expect_content_type"):
                assert case["expect_content_type"] in content_type, \
                    f"响应类型不符: 期望 {case['expect_content_type']}, 实际 {content_type}"
            return {"status_code": response.status_code, "content_type": content_type,
                    "size": len(response.content)}

        data = response.json()

        if case.get("expect_success"):
            self.assert_api_success(data)
            self.assert_side_effect(case, payload, data, ctx)
        else:
            self.assert_api_failure(data, expected_code=case.get("expect_code"))
        return data

    def upload_content(self):
        """multipart 上传的文件内容，子类可覆写"""
        return TINY_PNG

    def _upload_payload(self, case):
        """构造 multipart 上传的 (files, form)"""
        filename = case.get("filename", "kilo_test.png")
        content_type = case.get("content_type", "image/png")
        form = {k: v for k, v in (case.get("payload") or {}).items() if v is not None}
        return {"file": (filename, self.upload_content(), content_type)}, form

    def assert_side_effect(self, case, payload, data, ctx):
        """子类可覆写：校验接口成功后的落库情况"""

    def _resolve(self, value, ctx):
        """解析占位符，支持整串占位与内嵌占位"""
        if not isinstance(value, str) or "${" not in value:
            return value
        for key, val in (ctx or {}).items():
            token = "${" + key + "}"
            if value == token:
                # 整串占位：保留原始类型（列表/数字等）
                return val
            if token in value:
                value = value.replace(token, "" if val is None else str(val))
        return value

    # ==================== 业务数据操作封装 ====================

    def create_by_api(self, api, payload, table, key_column, key_value, id_column="id"):
        """通过接口造数，并按业务主键回查 id 后登记清理"""
        response = self.client.post(self.api_paths[api], json=payload)
        self.validator.assert_status_code(response, 200)
        self.assert_api_success(response.json())
        row = self.fetch_business_row(table, f"{key_column} = %s", (key_value,))
        assert row, f"造数未落库: {table}.{key_column}={key_value}"
        self.register_business_row(table, row[id_column])
        return row[id_column]

    def entity_row(self, table, row_id, id_column="id"):
        """按主键查询业务数据行"""
        return self.fetch_business_row(table, f"{id_column} = %s", (row_id,))
