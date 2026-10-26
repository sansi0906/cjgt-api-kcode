"""
pg_cleanup.py - PostgreSQL 业务数据清理工具
=============================================
用于清理接口测试产生的业务数据，基于 create_user_uuid 识别。
支持多 UUID 批量清理，并可根据登录账号（用户名/手机号）动态获取 UUID。
"""

import argparse
import sys

sys.path.insert(0, ".")

import psycopg2
from config import PG_CONFIG


# 默认兜底 UUID：自动化测试专用标识
TEST_CREATOR_UUID = "f4f44ea8-6713-4c96-9782-a06c2fa3d51d"

CLEANUP_TABLES = [
    "cjgt_service_pricing_history",
    "cjgt_service_pricing_import_log",
    "cjgt_service_pricing",
    "cjgt_knowledge_base",
    "cjgt_service_provider",
    "cjgt_business_scope",
    "cjgt_service_item",
    "cjgt_contact_config",
    "cjgt_user_agreement",
    "cjgt_platform_user",
    "cjgt_sms_log",
]

CLEANUP_SQL = {
    "cjgt_service_pricing_history": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_service_pricing_import_log": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_service_pricing": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_knowledge_base": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_service_provider": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_business_scope": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_service_item": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_contact_config": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_user_agreement": "DELETE FROM {table} WHERE create_user_uuid = %s",
    "cjgt_platform_user": "DELETE FROM {table} WHERE create_user_uuid = %s AND is_super_admin != 1",
    "cjgt_sms_log": "DELETE FROM {table} WHERE LEFT(phone, 3) = '174'",
}


def get_pg_connection():
    """获取 PostgreSQL 连接（165）"""
    return psycopg2.connect(
        host=PG_CONFIG["host"],
        port=PG_CONFIG["port"],
        database=PG_CONFIG["database"],
        user=PG_CONFIG["user"],
        password=PG_CONFIG["password"],
        connect_timeout=PG_CONFIG.get("connect_timeout", 10),
    )


def fetch_uuid_by_account(conn, account_type, account_value):
    """根据登录账号从数据库查询对应的 UUID。

    Args:
        conn: PostgreSQL 连接对象
        account_type: "platform_user"（按 user_name 查）或 "service_provider"（按 contact_no 查）
        account_value: 登录账号值（用户名或手机号）

    Returns:
        UUID 字符串，未找到则返回 None
    """
    cursor = conn.cursor()
    try:
        if account_type == "platform_user":
            cursor.execute(
                "SELECT user_uuid FROM cjgt_platform_user WHERE user_name = %s",
                (account_value,),
            )
        elif account_type == "service_provider":
            cursor.execute(
                "SELECT provider_uuid FROM cjgt_service_provider WHERE contact_no = %s",
                (account_value,),
            )
        else:
            return None
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception:
        return None
    finally:
        cursor.close()


def collect_cleanup_uuids(config):
    """收集所有需要清理的 UUID。

    收集来源（优先级从高到低）：
    1. config["pg_cleanup_uuid"]：配置文件中的固定 UUID（兜底）
    2. 数据库中管理员账号的 user_uuid（按 config["username"] 查询）
    3. 数据库中服务商账号的 provider_uuid（按 config["provider_username"] 查询）

    Args:
        config: pytest conftest 的 config 字典

    Returns:
        去重后的 UUID 列表
    """
    uuids = []

    # 1. 配置文件中的固定 UUID（兜底）
    static_uuid = config.get("pg_cleanup_uuid")
    if static_uuid:
        uuids.append(static_uuid)

    # 2. 从数据库动态获取登录账号的 UUID
    conn = None
    try:
        conn = get_pg_connection()

        # 管理员账号 UUID
        admin_username = config.get("username")
        if admin_username:
            admin_uuid = fetch_uuid_by_account(conn, "platform_user", admin_username)
            if admin_uuid:
                uuids.append(admin_uuid)

        # 服务商账号 UUID
        provider_phone = config.get("provider_username")
        if provider_phone:
            provider_uuid = fetch_uuid_by_account(conn, "service_provider", provider_phone)
            if provider_uuid:
                uuids.append(provider_uuid)
    except Exception:
        # 数据库查询失败不影响清理，保留配置中的固定 UUID
        pass
    finally:
        if conn:
            conn.close()

    # 去重并保持顺序
    seen = set()
    unique_uuids = []
    for uid in uuids:
        if uid and uid not in seen:
            seen.add(uid)
            unique_uuids.append(uid)

    return unique_uuids or [TEST_CREATOR_UUID]


def cleanup_test_data(creator_uuids=None, dry_run=False):
    """清理测试数据。

    Args:
        creator_uuids: UUID 列表或单个 UUID 字符串，默认使用 TEST_CREATOR_UUID
        dry_run: 如果 True，只打印将要删除的数据，不实际删除

    Returns:
        清理结果字典，key 为表名，value 为删除行数
    """
    if creator_uuids is None:
        creator_uuids = [TEST_CREATOR_UUID]
    if isinstance(creator_uuids, str):
        creator_uuids = [creator_uuids]

    # 去重
    creator_uuids = list(dict.fromkeys(creator_uuids))

    results = {}
    total_deleted = 0

    conn = get_pg_connection()
    cursor = conn.cursor()

    try:
        for table in CLEANUP_TABLES:
            table_deleted = 0
            for creator_uuid in creator_uuids:
                sql = CLEANUP_SQL.get(
                    table, "DELETE FROM {table} WHERE create_user_uuid = %s"
                ).format(table=table)
                cursor.execute(sql, (creator_uuid,))
                table_deleted += cursor.rowcount

            results[table] = table_deleted
            total_deleted += table_deleted

            if dry_run:
                # dry_run 时重新查询实际行数
                if table == "cjgt_sms_log":
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE LEFT(phone, 3) = '174'"
                    )
                else:
                    placeholders = ", ".join(["%s"] * len(creator_uuids))
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE create_user_uuid IN ({placeholders})",
                        tuple(creator_uuids),
                    )
                actual_count = cursor.fetchone()[0]
                print(
                    f"[DRY RUN] {table}: {actual_count} rows would be deleted "
                    f"(uuids={len(creator_uuids)})"
                )
            else:
                print(
                    f"Deleted {table_deleted} rows from {table} "
                    f"(uuids={len(creator_uuids)})"
                )

        if not dry_run:
            conn.commit()
        else:
            conn.rollback()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

    return results, total_deleted


def main():
    parser = argparse.ArgumentParser(description="清理接口测试业务数据")
    parser.add_argument(
        "--uuid",
        action="append",
        default=[TEST_CREATOR_UUID],
        help=f"创建者UUID，可多次指定，默认: {TEST_CREATOR_UUID}",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="只打印，不实际删除"
    )
    parser.add_argument(
        "--list-creators", action="store_true", help="列出所有 create_user_uuid"
    )
    args = parser.parse_args()

    if args.list_creators:
        conn = get_pg_connection()
        cursor = conn.cursor()
        for table in CLEANUP_TABLES:
            try:
                cursor.execute(
                    f"SELECT DISTINCT create_user_uuid FROM {table} WHERE create_user_uuid IS NOT NULL"
                )
                rows = cursor.fetchall()
                print(f"{table}: {[r[0] for r in rows]}")
            except Exception as e:
                print(f"{table}: ERROR {e}")
        cursor.close()
        conn.close()
        return

    print(f"Cleaning test data for UUIDs: {args.uuid}")
    print(f"Dry run: {args.dry_run}")
    print("-" * 50)

    results, total = cleanup_test_data(creator_uuids=args.uuid, dry_run=args.dry_run)

    print("-" * 50)
    print("Summary:")
    for table, count in results.items():
        print(f"  {table}: {count}")
    print(f"Total: {total} rows")


if __name__ == "__main__":
    main()
