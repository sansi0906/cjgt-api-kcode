"""
validator.py - 响应验证工具
=============================
提供常用的 API 响应断言方法
简化测试代码中的验证逻辑
"""


class BizCode:
    """业务返回码常量（/sys/login 等接口通用）"""

    SUCCESS = ("0", "00")
    ACCESS_DENIED = "01000003"        # 访问无权限-拦截
    TOKEN_INVALID = "01000005"        # 用户信息获取失败，请重新登录
    USER_INVALID = "01000009"         # 用户不存在或状态失效
    SMS_CODE_REQUIRED = "01000010"    # 短信验证码不能为空
    PASSWORD_ERROR = "01000011"       # 密码错误
    UNSUPPORTED_LOGIN = "01000014"    # 不支持的登录方式
    SYSTEM_BUSY = "02"                # 系统繁忙，请稍后再试


class ResponseValidator:
    @staticmethod
    def assert_status_code(response, expected_code=200):
        """断言 HTTP 状态码是否符合预期

        Args:
            response: requests.Response 对象
            expected_code: 预期的状态码，默认 200

        Raises:
            AssertionError: 状态码不匹配时抛出，包含实际响应体前 500 字符
        """
        assert response.status_code == expected_code, (
            f"Expected status {expected_code}, got {response.status_code}. "
            f"Body: {response.text[:500]}"
        )

    @staticmethod
    def assert_json_key(response, key):
        """断言响应 JSON 中是否包含指定键

        Args:
            response: requests.Response 对象
            key: 需要检查的键名

        Returns:
            解析后的 JSON 数据字典

        Raises:
            AssertionError: 键不存在时抛出
        """
        data = response.json()
        assert key in data, f"Key '{key}' not found in response: {data}"
        return data

    @staticmethod
    def assert_response_time(response, max_ms=5000):
        """断言响应时间是否在允许范围内

        Args:
            response: requests.Response 对象
            max_ms: 最大允许响应时间（毫秒），默认 5000ms

        Raises:
            AssertionError: 响应时间超限时抛出
        """
        assert response.elapsed.total_seconds() * 1000 < max_ms, (
            f"Response time {response.elapsed.total_seconds() * 1000:.0f}ms "
            f"exceeds limit {max_ms}ms"
        )

    @staticmethod
    def assert_biz_success(data):
        """断言业务码为成功"""
        assert data.get("code") in BizCode.SUCCESS, f"Expected success, got: {data}"
        return data

    @staticmethod
    def assert_biz_failure(data, expected_code=None):
        """断言业务码为失败，可校验具体错误码"""
        assert data.get("code") not in BizCode.SUCCESS, f"Expected failure but got success: {data}"
        if expected_code:
            assert data.get("code") == expected_code, (
                f"Expected code {expected_code}, got: {data.get('code')} ({data.get('message')})"
            )
        return data

    @staticmethod
    def assert_biz_code(data, expected_code):
        """断言业务码等于指定值"""
        assert data.get("code") == expected_code, (
            f"Expected code {expected_code}, got: {data.get('code')} ({data.get('message')})"
        )
        return data
