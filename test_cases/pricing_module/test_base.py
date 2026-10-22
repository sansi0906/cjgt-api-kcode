"""
test_base.py - 服务定价配置管理测试基类
"""

from utils.module_base import DataDrivenApiTestBase


class TestBase(DataDrivenApiTestBase):
    _module_name = "pricing_module"
    _module_desc = "服务定价配置管理模块"

    api_paths = {
        "tree": "/platform/pricing/tree",
        "tree_by_areas": "/platform/pricing/treeByAreas",
        "update_pricing": "/platform/pricing/updatePricing",
        "import": "/platform/pricing/import",
    }

    TABLE = "cjgt_service_pricing"

    # 存在定价数据的服务项目与区域路径（省-市-区）
    SERVICE_ITEM_ID = 289
    AREA_CODES = ["130000000000", "130500000000", "130534000000"]

    def _area_path(self):
        """按编码查询区域路径（AreaItemDto 结构）"""
        pg_helper = self._get_pg_helper()
        rows = pg_helper.fetch_all(
            "SELECT area_code, area_name, level FROM cjgt_area_info WHERE area_code = ANY(%s) ORDER BY area_code",
            (self.AREA_CODES,),
        )
        by_code = {r["area_code"]: r for r in rows}
        return [
            {"code": code, "name": by_code[code]["area_name"], "level": by_code[code]["level"]}
            for code in self.AREA_CODES if code in by_code
        ]

    def _pricing_row(self):
        """查询目标服务项目 + 区域的定价记录"""
        return self.fetch_business_row(
            self.TABLE, "service_item_id = %s AND area_code = %s", (self.SERVICE_ITEM_ID, self.AREA_CODES[-1])
        )

    def _ctx(self):
        return {
            "area_path": self._area_path(),
            "service_item_id": self.SERVICE_ITEM_ID,
        }
