# GrlApiTest 配置文件（模板）
# 使用时请复制为 config.py 并填入真实信息（或在 .env 中配置后由 config.py 读取）

import os
import sys

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONUTF8"] = "1"

try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(env_path)
except ImportError:
    pass

# API配置
BASE_URL = os.getenv("BASE_URL", "http://YOUR_API_HOST:PORT")
LOGIN_URL = "/sys/login"
LOGOUT_URL = "/sys/logout"

# 测试账号（管理后台）
USERNAME = os.getenv("TEST_USERNAME", "YOUR_ADMIN_PHONE")
PASSWORD = os.getenv("TEST_PASSWORD", "")
LOGIN_TYPE = int(os.getenv("TEST_LOGIN_TYPE", "1"))
WEB_TYPE = int(os.getenv("TEST_WEB_TYPE", "0"))

# 测试账号（服务商后台）
PROVIDER_USERNAME = os.getenv("TEST_PROVIDER_USERNAME", "YOUR_PROVIDER_PHONE")
PROVIDER_PASSWORD = os.getenv("TEST_PROVIDER_PASSWORD", "")
PROVIDER_WEB_TYPE = int(os.getenv("TEST_PROVIDER_WEB_TYPE", "1"))

# 已禁用账号（管理后台 / 服务商后台，status=0）
DISABLED_ADMIN_USERNAME = os.getenv("TEST_DISABLED_ADMIN_USERNAME", "YOUR_DISABLED_ADMIN_PHONE")
DISABLED_ADMIN_PASSWORD = os.getenv("TEST_DISABLED_ADMIN_PASSWORD", "")
DISABLED_PROVIDER_USERNAME = os.getenv("TEST_DISABLED_PROVIDER_USERNAME", "YOUR_DISABLED_PROVIDER_PHONE")
DISABLED_PROVIDER_PASSWORD = os.getenv("TEST_DISABLED_PROVIDER_PASSWORD", "")

# 已删除账号（delete_status=1）
DELETED_ADMIN_USERNAME = os.getenv("TEST_DELETED_ADMIN_USERNAME", "YOUR_DELETED_ADMIN_PHONE")
DELETED_ADMIN_PASSWORD = os.getenv("TEST_DELETED_ADMIN_PASSWORD", "")

# Token缓存
TOKEN_FILE = "token.json"

# Allure 报告目录
ALLURE_RESULTS_DIR = "reports/allure-results"

# MySQL数据库配置（163：测试框架数据）
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "YOUR_MYSQL_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "YOUR_DATABASE"),
    "user": os.getenv("DB_USER", "YOUR_MYSQL_USER"),
    "password": os.getenv("DB_PASSWORD", ""),
    "connect_timeout": 10,
    "db_type": "mysql",
}

# PostgreSQL数据库配置（165：被测系统业务库）
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "YOUR_PG_HOST"),
    "port": int(os.getenv("PG_PORT", "5432")),
    "database": os.getenv("PG_NAME", "YOUR_DATABASE"),
    "user": os.getenv("PG_USER", "YOUR_PG_USER"),
    "password": os.getenv("PG_PASSWORD", ""),
    "connect_timeout": 10,
    "db_type": "postgresql",
}

# 163 测试库：是否启用、是否在执行后清理测试结果
DB_ENABLED = True
DB_CLEANUP_AFTER_TEST = False
DB_CLEANUP_MODULES = []

# 165 业务库：清理由测试账号创建的数据
PG_CLEANUP_UUID = os.getenv("PG_CLEANUP_UUID", "YOUR_CLEANUP_UUID")
PG_CLEANUP_ENABLED = True
