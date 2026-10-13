"""
pg_search_worker.py - 数据库全表扫描工具
============================================
扫描 PostgreSQL 中所有包含 create_user_uuid 字段的表，
查找与工人（worker）相关的测试数据，辅助判断清理逻辑是否完整。
"""

import sys
sys.path.insert(0, ".")

import psycopg2
from config import PG_CONFIG

TEST_CREATOR_UUID = "f4f44ea8-6713-4c96-9782-a06c2fa3d51d"

# 已知在清理列表中的表
KNOWN_CLEANUP_TABLES = [
    "cjgt_service_pricing_history",
    "cjgt_service_pricing_import_log",
    "cjgt_service_pricing",
    "cjgt_knowledge_base",
    "cjgt_service_provider",
    "cjgt_business_scope",
    "cjgt_service_item",
    "cjgt_platform_user",
    "cjgt_worker_base_info",
    "cjgt_worker_sign",
]

# 工人相关关键词（表名/字段名匹配）
WORKER_KEYWORDS = ["worker", "gongrenle", "工人"]


def get_pg_connection():
    """获取 PostgreSQL 连接"""
    return psycopg2.connect(
        host=PG_CONFIG["host"],
        port=PG_CONFIG["port"],
        database=PG_CONFIG["database"],
        user=PG_CONFIG["user"],
        password=PG_CONFIG["password"],
        connect_timeout=PG_CONFIG.get("connect_timeout", 10),
    )


def find_tables_with_create_user_uuid(conn):
    """查找所有包含 create_user_uuid 字段的表"""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.columns
            WHERE column_name = 'create_user_uuid'
              AND table_schema = 'public'
            ORDER BY table_name
        """)
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()


def find_tables_with_worker_keyword(conn):
    """查找表名包含 worker/gongrenle 关键词的表"""
    cursor = conn.cursor()
    try:
        conditions = []
        params = []
        for kw in WORKER_KEYWORDS:
            conditions.append("table_name ILIKE %s")
            params.append(f"%{kw}%")

        sql = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND ({' OR '.join(conditions)})
            ORDER BY table_name
        """
        cursor.execute(sql, params)
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()


def count_uuid_rows(conn, table_name, uuid):
    """统计表中指定 UUID 的数据量"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE create_user_uuid = %s", (uuid,))
        return cursor.fetchone()[0]
    except Exception as e:
        return str(e)
    finally:
        cursor.close()


def check_table_columns(conn, table_name):
    """检查表的字段信息"""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            ORDER BY ordinal_position
        """, (table_name,))
        return cursor.fetchall()
    finally:
        cursor.close()


def search_worker_data_in_all_tables(conn, uuid):
    """全表扫描：在所有含 create_user_uuid 的表中查找工人相关数据"""
    # 1. 找到所有含 create_user_uuid 的表
    tables_with_uuid = find_tables_with_create_user_uuid(conn)

    print(f"{'='*60}")
    print(f"全表扫描报告 - UUID: {uuid}")
    print(f"{'='*60}")
    print(f"\n📊 含 create_user_uuid 字段的表（共 {len(tables_with_uuid)} 张）")
    print(f"{'-'*60}")

    # 2. 统计表中数据量
    worker_related_tables = []
    for table in tables_with_uuid:
        count = count_uuid_rows(conn, table, uuid)
        in_cleanup = "✅" if table in KNOWN_CLEANUP_TABLES else "❌ 遗漏"
        is_worker = any(kw in table.lower() for kw in ["worker", "gongrenle"])

        marker = ""
        if is_worker and str(count) != "0":
            marker = " ⚠️ 工人相关"
        elif is_worker:
            marker = " 🔍 工人表"

        print(f"  {in_cleanup} {table}: {count} 条{marker}")

        if is_worker:
            worker_related_tables.append(table)

    # 3. 显示工人相关表的详情
    if worker_related_tables:
        print(f"\n{'='*60}")
        print(f"🔍 工人相关表详情")
        print(f"{'='*60}")

        for table in worker_related_tables:
            print(f"\n📋 表: {table}")
            print(f"  {'-'*50}")

            # 显示字段
            columns = check_table_columns(conn, table)
            print(f"  字段列表:")
            for col_name, col_type in columns:
                print(f"    - {col_name} ({col_type})")

            # 显示数据量
            count = count_uuid_rows(conn, table, uuid)
            in_cleanup = "✅ 已在清理列表" if table in KNOWN_CLEANUP_TABLES else "❌ 未在清理列表"
            print(f"\n  数据量: {count} 条")
            print(f"  清理状态: {in_cleanup}")

            # 如果有数据，预览一条
            if count and str(count) != "0":
                cursor = conn.cursor()
                try:
                    cursor.execute(f"SELECT * FROM {table} WHERE create_user_uuid = %s LIMIT 1", (uuid,))
                    row = cursor.fetchone()
                    col_names = [desc[0] for desc in cursor.description]
                    if row:
                        print(f"\n  数据预览 (1条):")
                        for col, val in zip(col_names, row):
                            val_str = str(val)[:80] if val else "NULL"
                            print(f"    {col}: {val_str}")
                except Exception as e:
                    print(f"    预览失败: {e}")
                finally:
                    cursor.close()

    # 4. 汇总遗漏表
    missing_tables = [t for t in tables_with_uuid if t not in KNOWN_CLEANUP_TABLES]
    if missing_tables:
        print(f"\n{'='*60}")
        print(f"⚠️ 未在清理列表中的表（共 {len(missing_tables)} 张）")
        print(f"{'='*60}")
        for table in missing_tables:
            count = count_uuid_rows(conn, table, uuid)
            is_worker = any(kw in table.lower() for kw in ["worker", "gongrenle"])
            tag = " 🔍 工人相关" if is_worker else ""
            print(f"  ❌ {table}: {count} 条{tag}")
    else:
        print(f"\n✅ 所有含 create_user_uuid 的表都已在清理列表中！")

    # 5. 查找不含 create_user_uuid 但表名含 worker 的表
    print(f"\n{'='*60}")
    print(f"🔍 表名含 worker/gongrenle 关键词的表（可能不含 create_user_uuid）")
    print(f"{'='*60}")

    worker_tables = find_tables_with_worker_keyword(conn)
    if worker_tables:
        for table in worker_tables:
            has_uuid = table in tables_with_uuid
            has_data = count_uuid_rows(conn, table, uuid) if has_uuid else "N/A"
            print(f"  📋 {table}")
            print(f"     - 含 create_user_uuid: {'是' if has_uuid else '否'}")
            print(f"     - UUID 数据量: {has_data}")

            if not has_uuid:
                columns = check_table_columns(conn, table)
                print(f"     - 字段列表（前5个）:")
                for col_name, col_type in columns[:5]:
                    print(f"       {col_name} ({col_type})")
    else:
        print(f"  未找到匹配的表")


def main():
    print("连接 PostgreSQL 数据库...")
    conn = get_pg_connection()

    try:
        search_worker_data_in_all_tables(conn, TEST_CREATOR_UUID)
    finally:
        conn.close()
        print(f"\n✅ 扫描完成")


if __name__ == "__main__":
    main()
