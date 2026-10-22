"""
test_base.py - 用户协议管理测试基类
"""

import uuid

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "agreement_module"
    _module_desc = "用户协议管理模块"

    api_paths = {
        "save": "/platform/agreement/save",
        "page": "/platform/agreement/page",
        "edit": "/platform/agreement/edit",
        "detail": "/platform/agreement/detail",
    }

    TABLE = "cjgt_user_agreement"

    @staticmethod
    def _unique_agreement_name():
        return "自动化协议" + str(uuid.uuid4().int % 10**6).zfill(6)

    def _backup_agreement(self, agreement_type):
        """备份并物理移除某类型协议（业务约束：每种类型仅允许一条）"""
        row = self.fetch_business_row(self.TABLE, "agreement_type = %s", (agreement_type,))
        if not row:
            return None
        self.delete_business_row(self.TABLE, row["id"])
        return dict(row)

    def _restore_agreement(self, backup):
        """恢复被移除的协议（保留原 id）"""
        if not backup:
            return
        pg_helper = self._get_pg_helper()
        pg_helper.execute(
            "INSERT INTO cjgt_user_agreement (id, agreement_name, agreement_type, agreement_content, publisher, "
            "publish_time, create_user_name, create_time, last_modify_name, last_modify_time, delete_status, "
            "create_user_uuid, last_modify_uuid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (backup["id"], backup["agreement_name"], backup["agreement_type"], backup["agreement_content"],
             backup["publisher"], backup["publish_time"], backup["create_user_name"], backup["create_time"],
             backup["last_modify_name"], backup["last_modify_time"], backup["delete_status"],
             backup["create_user_uuid"], backup["last_modify_uuid"]),
        )

    def _create_agreement(self, agreement_type=3, name=None):
        """新增协议，返回 (id, name)；会先让出该类型的占用"""
        backup = self._backup_agreement(agreement_type)
        try:
            name = name or self._unique_agreement_name()
            row_id = self.create_by_api("save", {
                "agreementName": name,
                "agreementType": agreement_type,
                "agreementContent": "自动化协议内容",
            }, self.TABLE, "agreement_name", name)
        finally:
            self._restore_agreement(backup)
        return row_id, name

    def _ctx(self, agreement_type=3, name=None):
        row_id, agreement_name = self._create_agreement(agreement_type, name)
        return {"entity_id": row_id, "entity_name": agreement_name,
                "unique_agreement_name": self._unique_agreement_name()}
