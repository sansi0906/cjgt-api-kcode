"""
data_driver.py - 数据驱动测试工具
==================================
支持从 JSON 和 YAML 文件加载测试数据
用于参数化测试，实现测试数据与测试逻辑分离

用例数据支持以下约定字段：
- name       用例标识
- desc       用例描述（作为参数化 id 展示在报告中）
- role       角色：admin（管理后台）/ provider（服务商后台），决定账号与 webType 来源
- expect_success  期望登录/操作是否成功
- expect_code     期望的业务错误码
"""

import os
import json
import yaml

ROLE_ACCOUNT_KEYS = {
    "admin": {
        "username": "username",
        "password": "password",
        "web_type": "web_type",
    },
    "provider": {
        "username": "provider_username",
        "password": "provider_password",
        "web_type": "provider_web_type",
    },
}


def load_json(path):
    """从 JSON 文件加载测试数据

    Args:
        path: JSON 文件路径

    Returns:
        解析后的 Python 对象（字典或列表）
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path):
    """从 YAML 文件加载测试数据

    Args:
        path: YAML 文件路径

    Returns:
        解析后的 Python 对象（字典或列表）
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_test_data(data_file):
    """根据文件扩展名自动选择加载方式

    Args:
        data_file: 数据文件路径（支持 .json、.yaml、.yml）

    Returns:
        解析后的测试数据

    Raises:
        ValueError: 不支持的文件格式
    """
    ext = os.path.splitext(data_file)[1].lower()
    if ext == ".json":
        return load_json(data_file)
    elif ext in (".yaml", ".yml"):
        return load_yaml(data_file)
    else:
        raise ValueError(f"Unsupported data file format: {ext}")


def load_param_cases(data_file, id_key="desc"):
    """加载数据驱动用例，返回 (cases, ids) 供 pytest.mark.parametrize 使用

    Args:
        data_file: 数据文件路径
        id_key: 用作参数化 id 的字段，默认 desc，缺失时回退 name

    Returns:
        (cases, ids) 元组
    """
    cases = load_test_data(data_file)
    ids = [case.get(id_key) or case.get("name") for case in cases]
    return cases, ids


def resolve_role_account(case, config):
    """按用例中的 role 解析账号与 webType

    Args:
        case: 单条用例数据
        config: pytest 全局配置字典（含 username/password/web_type 等）

    Returns:
        (username, password, web_type) 三元组
    """
    role = case.get("role", "admin")
    keys = ROLE_ACCOUNT_KEYS.get(role, ROLE_ACCOUNT_KEYS["admin"])
    username = config.get(keys["username"])
    password = config.get(keys["password"])
    web_type = config.get(keys["web_type"])

    if "username" in case:
        username = case["username"]
    if "password" in case:
        password = case["password"]
    if "web_type" in case:
        web_type = case["web_type"]

    return username, password, web_type


def resolve_env_value(value, env=None):
    """解析 ${ENV_NAME} 占位符，取环境变量值；无占位符时原样返回"""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        import os as _os
        source = env if env is not None else _os.environ
        return source.get(value[2:-1], value)
    return value
