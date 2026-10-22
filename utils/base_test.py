"""
base_test.py - 通用测试基类
=============================
所有模块测试类的基类，提供通用的 setup、login、断言、数据库记录等功能。
各模块只需实现特有的工厂方法。
"""

import time
import uuid
import random

import pytest

from api_clients.jeecgboot_client import JeecgBootClient
from utils.validator import ResponseValidator


class BaseTest:
    _module_name = "unknown"
    _module_desc = "未知模块"
    _skip_auto_login = False

    @pytest.fixture(autouse=True)
    def setup(self, config, execution_id, db_helper, pg_cleanup, request):
        """自动初始化客户端、验证器并登录"""
        self.client = JeecgBootClient(base_url=config["base_url"])
        self.validator = ResponseValidator()
        self.config = config
        self.execution_id = execution_id
        self.db_helper = db_helper
        self.pg_cleanup = pg_cleanup
        self._created_ids = []
        self._business_rows = []
        self._module_id = None
        self._test_name = request.node.name
        if not self._skip_auto_login:
            token = self.login()
            self.client.set_token(token)

    def teardown_method(self):
        """清理测试创建的接口数据与自造业务数据"""
        for table, row_id in getattr(self, "_business_rows", []):
            try:
                self.delete_business_row(table, row_id)
            except Exception as e:
                import logging
                logging.warning(f"Failed to cleanup business row {table}#{row_id}: {e}")
        self._business_rows = []
        for item_id in getattr(self, "_created_ids", []):
            try:
                self._delete_test_data(item_id)
            except Exception as e:
                if self.db_helper:
                    try:
                        self.db_helper.save_test_log(
                            execution_id=self.execution_id,
                            level="WARNING",
                            message=f"Failed to cleanup test data id={item_id}: {e}",
                            module=getattr(self, '_module_name', 'unknown'),
                            case_name=getattr(self, '_test_name', 'unknown'),
                        )
                    except Exception as log_e:
                        import logging
                        logging.warning(f"Failed to log cleanup failure for id={item_id}: {log_e}")

    def _log_test_data_created(self, item_id, item_name=None):
        """记录测试数据创建日志"""
        if self.db_helper:
            try:
                self.db_helper.save_test_log(
                    execution_id=self.execution_id,
                    level="INFO",
                    message=f"Test data created: id={item_id}, name={item_name}",
                    module=getattr(self, '_module_name', 'unknown'),
                    case_name=getattr(self, '_test_name', 'unknown'),
                )
            except Exception as log_e:
                import logging
                logging.warning(f"Failed to log test data creation for id={item_id}: {log_e}")

    def _delete_test_data(self, item_id):
        """删除测试数据，由子类实现具体删除逻辑"""
        pass

    # ==================== 业务库数据操作（165 PostgreSQL） ====================

    def register_business_row(self, table, row_id):
        """登记自造的业务数据行，teardown 时自动物理删除"""
        if not hasattr(self, "_business_rows"):
            self._business_rows = []
        self._business_rows.append((table, row_id))
        return row_id

    def insert_business_row(self, table, data, return_id=True):
        """向业务库插入一行数据并登记清理

        Args:
            table: 表名
            data: 字段字典
            return_id: 是否返回自增 id

        Returns:
            插入行的 id（return_id 为 False 时返回影响行数）
        """
        pg_helper = self._get_pg_helper()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        if return_id:
            sql += " RETURNING id"
        result = pg_helper.execute(sql, tuple(data.values()))
        row_id = result if not return_id else pg_helper.fetch_one(
            f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1"
        )
        if return_id:
            row_id = row_id["id"] if isinstance(row_id, dict) else row_id
            self.register_business_row(table, row_id)
        return row_id

    def update_business_row(self, table, row_id, data):
        """更新业务库中的一行数据"""
        pg_helper = self._get_pg_helper()
        sets = ", ".join(f"{k} = %s" for k in data)
        pg_helper.execute(f"UPDATE {table} SET {sets} WHERE id = %s", tuple(data.values()) + (row_id,))
        return row_id

    def delete_business_row(self, table, row_id):
        """物理删除业务库中的一行数据"""
        pg_helper = self._get_pg_helper()
        return pg_helper.execute(f"DELETE FROM {table} WHERE id = %s", (row_id,))

    def fetch_business_row(self, table, where_sql, params=None):
        """按条件查询业务库中的一行数据"""
        pg_helper = self._get_pg_helper()
        return pg_helper.fetch_one(f"SELECT * FROM {table} WHERE {where_sql}", params)

    def assert_api_success(self, data):
        """断言业务响应成功（统一走 validator）"""
        return self.validator.assert_biz_success(data)

    def assert_api_failure(self, data, expected_code=None):
        """断言业务响应失败（统一走 validator）"""
        return self.validator.assert_biz_failure(data, expected_code)

    def login(self, username=None, password=None, login_type=None, web_type=None):
        """执行登录并返回 Token"""
        response = self.client.login(
            username=username or self.config["username"],
            password=password or self.config["password"],
            login_type=login_type if login_type is not None else self.config.get("login_type", 1),
            web_type=web_type if web_type is not None else self.config.get("web_type", 0),
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") in ("0", "00"), f"Login failed: {data}"
        return data.get("data", {}).get("token")

    def assert_login_success(self, data):
        """断言登录成功"""
        self.assert_api_success(data)
        assert data.get("data", {}).get("token"), "Token is missing in response"

    def assert_login_failure(self, data, expected_code=None):
        """断言登录失败"""
        self.assert_api_failure(data, expected_code)

    def assert_save_success(self, data, message=None):
        """断言操作成功"""
        self.assert_api_success(data)
        if message:
            assert data.get("message") == message, f"Unexpected message: {data.get('message')}"

    def assert_response_time(self, response, max_duration_ms=500):
        """断言接口响应时间不超过阈值"""
        duration_ms = response.elapsed.total_seconds() * 1000
        assert duration_ms <= max_duration_ms, \
            f"Response too slow: {duration_ms:.0f}ms > {max_duration_ms}ms"
        return duration_ms

    def skip_if_empty(self, records, message="查询结果为空，跳过测试"):
        """如果 records 为空，跳过当前测试"""
        if not records:
            pytest.skip(message)

    def assert_save_failure(self, data, expected_code=None):
        """断言操作失败"""
        self.assert_api_failure(data, expected_code)

    def _get_module_id(self, module_name, module_desc=""):
        """获取或创建模块ID"""
        if self._module_id is None and self.db_helper:
            self._module_id = self.db_helper.save_test_module(module_name, module_desc)
        return self._module_id

    def _save_test_result(self, case_name, status, duration_ms=None, error_message=None,
                          request_data=None, response_data=None, assertion_details=None, module_name=None, module_desc=""):
        """保存测试结果到数据库（163 MySQL）"""
        if not self.db_helper:
            return
        module_id = self._get_module_id(module_name or self._module_name, module_desc)
        if not module_id:
            return
        case_id = self.db_helper.save_test_case(
            module_id=module_id,
            case_name=case_name,
            case_desc="",
            priority="P1"
        )
        self.db_helper.save_test_result(
            case_id=case_id,
            execution_id=self.execution_id,
            status=status,
            duration_ms=duration_ms,
            error_message=error_message,
            request_data=request_data,
            response_data=response_data,
            assertion_details=assertion_details,
            environment="test"
        )

    def _record_test_result(self, case_name, response, start_time=None, module_name=None, module_desc=""):
        """记录测试结果，自动判断成功/失败"""
        import time
        duration_ms = int((time.time() - start_time) * 1000) if start_time else None
        data = response.json() if response.status_code == 200 else {}
        status = "passed" if data.get("code") in ("0", "00") else "failed"
        self._save_test_result(
            case_name=case_name,
            status=status,
            duration_ms=duration_ms,
            error_message=data.get("message") if status == "failed" else None,
            response_data=str(data),
            module_name=module_name,
            module_desc=module_desc
        )

    def _unique_real_name(self):
        """生成唯一的真实姓名"""
        return f"测试用户{int(time.time())}"

    def _unique_user_name(self):
        """生成唯一的用户名（174开头的11位手机号）"""
        suffix = random.randint(10000000, 99999999)
        return f"174{suffix}"

    def _unique_item_name(self):
        """生成唯一的服务项目名称"""
        suffix = random.randint(1000, 9999)
        return f"Test{suffix}"

    def _create_service_item(self, item_name=None, billing_method=1):
        """新增服务项目并通过分页查询获取项目ID

        Returns:
            (item_id, item_name) 元组
        """
        item_name = item_name or self._unique_item_name()
        return self._create_and_get_id(
            create_fn=lambda: self.client.add_service_item(
                item_name=item_name,
                billing_method=billing_method,
                subtitle="TestSubtitle",
                item_desc="TestDescription",
            ),
            query_fn=lambda: self.client.page_service_items(page_num=1, page_size=10, item_name=item_name),
            match_key="itemName",
            match_value=item_name,
        )

    def _get_pg_helper(self):
        """获取 PostgreSQL 数据库助手实例（单例）"""
        if not hasattr(self, "_pg_helper_instance"):
            from config import PG_CONFIG
            from utils.db_helper import DatabaseHelper
            self._pg_helper_instance = DatabaseHelper(PG_CONFIG)
        return self._pg_helper_instance

    def _get_existing_service_item(self, display_only=True):
        """获取一个已存在的服务项目"""
        if display_only:
            resp = self.client.list_display_service_items(is_display=1)
        else:
            resp = self.client.list_display_service_items()
        self.validator.assert_status_code(resp, 200)
        data = resp.json()
        self.assert_save_success(data)
        items = data.get("data", [])
        assert items, "No service items found"
        return items[0]["id"], items[0]["itemName"]

    def _create_and_get_id(self, create_fn, query_fn, match_key, match_value, id_key="id"):
        """通用创建并获取ID方法

        Args:
            create_fn: 创建函数（无参数），返回 Response
            query_fn: 查询函数（无参数），返回 Response
            match_key: 匹配字段名（如 "userName", "itemName", "roleName"）
            match_value: 匹配值
            id_key: ID 字段名，默认 "id"

        Returns:
            (item_id, match_value) 元组
        """
        response = create_fn()
        self.validator.assert_status_code(response, 200)
        data = response.json()
        self.assert_save_success(data)

        page_resp = query_fn()
        self.validator.assert_status_code(page_resp, 200)
        page_data = page_resp.json()
        records = page_data.get("data", {}).get("records", [])
        item_id = None
        for record in records:
            if record.get(match_key) == match_value:
                item_id = record.get(id_key)
                break
        assert item_id, f"Item not found after creation: {page_data}"
        self._created_ids.append(item_id)
        self._log_test_data_created(item_id, match_value)
        return item_id, match_value
