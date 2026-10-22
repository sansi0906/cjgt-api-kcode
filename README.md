# cjgt-api-kcode - Python API Testing Framework

基于 pytest + requests + allure 的自动化接口测试框架，支持 JeecgBoot 业务系统的全量接口测试。

## 环境要求

- Python >= 3.8
- pip install -r requirements.txt

## 快速开始

```bash
# 1. 复制配置模板并填入实际值
cp .env.example .env
# 编辑 .env 填入数据库密码、API地址、测试账号等敏感信息

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行全部测试
python -m pytest -v --tb=short

# 4. 运行冒烟测试
python -m pytest -m smoke -v --tb=short

# 5. 运行特定模块
python -m pytest test_cases/login_module/ -v --tb=short

# 6. 生成 Allure 报告
python run_tests.py
```

## 测试标记

| 标记 | 说明 | 使用场景 |
|------|------|----------|
| `@pytest.mark.smoke` | 冒烟测试 | 核心流程快速验证 |
| `@pytest.mark.regression` | 回归测试 | 全量业务场景 |
| `@pytest.mark.slow` | 慢速测试 | 包含等待或大量数据处理 |
| `@pytest.mark.backend_bug` | 后端缺陷 | 预期失败但后端返回成功 |

## 项目结构

```
├── .env.example                   # 环境变量配置模板（复制为 .env 使用）
├── .gitignore                     # Git 忽略规则（含敏感文件）
├── config.example.py              # 配置文件模板
├── config.py                      # 全局配置（从 .env 读取，不提交）
├── conftest.py                    # pytest 全局固件
├── pytest.ini                     # pytest 配置（标记、路径等）
├── requirements.txt               # 依赖包
├── README.md                      # 项目说明
├── run_tests.py                   # 运行测试并生成 Allure 报告
├── api_clients/                   # API 客户端
│   ├── __init__.py
│   ├── base_client.py             # 基础 HTTP 客户端
│   └── jeecgboot_client.py        # 业务 API 客户端
├── utils/                         # 工具类
│   ├── __init__.py
│   ├── token_manager.py           # Token 管理（自动刷新）
│   ├── db_helper.py               # 163 MySQL 数据库操作
│   ├── pg_cleanup.py              # 165 PostgreSQL 清理工具
│   ├── cleanup_pricing.py         # service_item/pricing 手动清理
│   ├── init_db_data.py            # 初始化测试数据
│   ├── base_test.py               # 通用测试基类
│   ├── validator.py               # 响应验证器
│   ├── data_driver.py             # 数据驱动工具
│   ├── factories.py               # 测试数据工厂
│   └── area_helper.py             # 行政区域辅助
├── test_cases/                    # 测试用例
│   ├── __init__.py
│   ├── login_module/              # 登录模块
│   ├── platform_user_module/      # 平台用户管理
│   ├── role_management_module/    # 角色管理
│   ├── service_item_module/       # 服务项目配置
│   ├── service_provider_module/   # 服务商管理
│   ├── pricing_module/            # 服务定价配置
│   ├── contract_service_config_module/  # 合同服务配置
│   ├── knowledge_base_module/     # 知识库管理
│   ├── tax_type_config_module/    # 税费类型配置
│   ├── token_expiration/          # Token 过期测试
│   ├── boundary_values/           # 边界值测试
│   └── test_api_definitions_data.py
├── data/                          # 测试数据
│   ├── api_definitions.yaml       # API 定义数据
│   ├── login_data.example.json    # 登录测试数据模板
│   └── 服务定价数据.xlsx          # 服务定价测试数据
├── plugins/                       # pytest 插件
│   └── request_capture_plugin.py  # 请求捕获插件
├── scripts/                       # 辅助脚本
│   └── remove_redundant_login.py
├── pages/                         # Page Object（预留）
├── archive/                       # 归档的测试模块
├── olddir/                        # 旧版脚本归档
└── reports/                       # 测试报告（不提交）
```

## 模块覆盖

| 模块 | 接口数 | 用例数 | 状态 |
|------|--------|--------|------|
| 登录模块 | 3 | 28 | ✅ |
| 平台用户管理 | 7 | 30 | ✅ |
| 角色管理 | 9 | 31 | ✅ |
| 服务项目配置 | 5 | 27 | ✅ |
| 服务商管理 | 7 | 26 | ✅ |
| 服务定价配置 | 4 | 11 | ✅ |
| 合同服务配置 | 5 | 16 | ✅ |
| 用户协议管理 | 4 | 12 | ✅ |
| 经营范围配置 | 5 | 12 | ✅ |
| 税种配置管理 | 4 | 11 | ✅ |
| 知识库管理 | 6 | 21 | ✅ |
| 菜单管理 | 7 | 14 | ✅ |
| 公共接口（区域/用户信息/首页） | 3 | 6 | ✅ |
| 合同管理 | 1 | 3 | ✅ |
| 服务工单管理 | 5 | 11 | ✅ |
| 订单管理 | 4 | 8 | ✅ |
| 超级个体档案管理 | 4 | 7 | ✅ |
| 超级个体入驻 | 7 | 9 | ✅ |
| 文件管理 | 7 | 7 | ✅ |
| OCR识别 | 8 | 15 | ✅ |
| open-api | 1 | 1 | ✅ |
| **合计** | **106** | **306** | - |

## 数据库说明

### 163 MySQL（test_cjgt）- 测试框架数据

| 表 | 说明 | 自动清理 |
|----|------|----------|
| test_modules | 测试模块 | 否 |
| test_cases | 测试用例 | 否 |
| test_results | 测试结果 | 否 |
| test_data | 测试数据 | 是 |
| test_logs | 测试日志 | 是 |
| api_definitions | API 定义 | 否 |

### 165 PostgreSQL（cjgt）- 业务数据

使用 `utils/pg_cleanup.py` 按 `create_user_uuid` 清理测试数据：

```bash
# 查看待清理数据
python utils/pg_cleanup.py --dry-run

# 执行清理
python utils/pg_cleanup.py
```

## 清理数据

### 自动清理（配置开关）

在 `.env` 中配置：

```bash
# 163 MySQL 测试数据自动清理
DB_CLEANUP_AFTER_TEST=true
DB_CLEANUP_MODULES=platform_user_module,service_provider_module,...

# 165 PostgreSQL 业务数据自动清理
PG_CLEANUP_ENABLED=true
PG_CLEANUP_UUID=f4f44ea8-6713-4c96-9782-a06c2fa3d51d
```

### 手动清理

```bash
# 清理 service_item/pricing（无 delete 接口）
python utils/cleanup_pricing.py --dry-run
python utils/cleanup_pricing.py
```

## 配置说明

编辑 `.env` 文件（从 `.env.example` 复制）：

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| BASE_URL | API 服务器地址 | http://172.16.1.165:9200 |
| TEST_USERNAME | 登录用户名 | 15522719628 |
| TEST_PASSWORD | 登录密码 | ******** |
| TEST_LOGIN_TYPE | 登录类型 | 1（密码登录） |
| TEST_WEB_TYPE | 终端类型 | 0（管理后台） |
| DB_HOST | 163 MySQL 主机 | 172.16.1.163 |
| DB_PORT | 163 MySQL 端口 | 3307 |
| DB_NAME | 163 MySQL 数据库 | test_cjgt |
| DB_USER | 163 MySQL 用户 | root |
| DB_PASSWORD | 163 MySQL 密码 | ******** |
| PG_HOST | 165 PostgreSQL 主机 | 172.16.1.165 |
| PG_PORT | 165 PostgreSQL 端口 | 5432 |
| PG_NAME | 165 PostgreSQL 数据库 | cjgt |
| PG_USER | 165 PostgreSQL 用户 | postgres |
| PG_PASSWORD | 165 PostgreSQL 密码 | ******** |
| PG_CLEANUP_UUID | 清理用的 UUID | f4f44ea8-6713-4c96-9782-a06c2fa3d51d |

## 测试框架特性

- 自动登录并复用 Token
- 测试用例自动记录到 163 MySQL
- 测试数据自动清理（MySQL + PostgreSQL）
- 统一断言方法（`assert_save_success` / `assert_save_failure`）
- 支持 pytest 标记分类运行
- UTF-8 编码支持
- Allure 报告集成
- 请求/响应自动捕获

## 注意事项

1. 测试前请确认 163/165 数据库可连接
2. 155 手机号对应 UUID：`f4f44ea8-6713-4c96-9782-a06c2fa3d51d`
3. 验证码发送有 60 秒频率限制，已标记为 `@pytest.mark.slow`
4. service_item 和 pricing 模块无 delete 接口，需使用手动清理脚本
5. **敏感信息（密码、Token、数据库凭证）不应提交到版本控制**，请使用 `.env` 文件管理

## 许可证

MIT License

## Windows 终端中文乱码（UTF-8）

接口返回的中文在部分 Windows PowerShell 终端显示为乱码（如 `用户不存在或状态失效` 显示为 `�û������ڻ�״̬ʧЧ`），
这是终端代码页（默认 GBK/936）与 UTF-8 不匹配导致，**源码与接口本身无问题**。

解决方式（任选其一，建议全部执行）：

```powershell
chcp 65001                      # 切换当前终端为 UTF-8
$env:PYTHONIOENCODING = "utf-8" # Python 输出使用 UTF-8
```

也可在系统设置中勾选「Beta: Use Unicode UTF-8 for worldwide language support」。
项目 `conftest.py` 已在运行前自动执行 `sys.stdout.reconfigure(encoding="utf-8")`，
若仍显示乱码，说明是终端代码页问题，按上述方式处理即可。
