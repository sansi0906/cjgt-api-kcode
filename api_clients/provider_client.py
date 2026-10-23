"""
provider_client.py - 服务商端 API 客户端
=======================================
封装服务商后台 /server/* 接口，所有路径基于 OpenAPI 规范（/v3/api-docs）。
继承 BaseClient，支持登录/登出及各业务接口的封装调用。
"""

from api_clients.base_client import BaseClient


class ProviderClient(BaseClient):
    # 服务商端登录 webType 为 1
    LOGIN_WEB_TYPE = 1

    def logout(self):
        """服务商登出"""
        token = self.token
        self.clear_token()
        return self.post("/sys/logout", headers={"token": token} if token else {})

    # ---------------- 客户管理 ----------------

    def customer_page(self, page_num=1, page_size=10, effect_month_start=None,
                      effect_month_end=None, province_area_code=None, city_area_code=None,
                      district_area_code=None, service_status=None, keyword=None):
        """客户管理列表"""
        payload = {"pageNum": page_num, "pageSize": page_size}
        payload.update(self._build_payload(
            effectMonthStart=effect_month_start,
            effectMonthEnd=effect_month_end,
            provinceAreaCode=province_area_code,
            cityAreaCode=city_area_code,
            districtAreaCode=district_area_code,
            serviceStatus=service_status,
            keyword=keyword,
        ))
        return self.post("/server/customer/page", json=payload)

    def customer_detail(self, contact_no):
        """客户详情"""
        return self.get("/server/customer/detail", params={"contactNo": contact_no})

    def customer_declare_config(self, contact_no):
        """查询客户申报配置"""
        return self.get("/server/customer/declare/config", params={"contactNo": contact_no})

    def customer_declare_config_save(self, contact_no, items):
        """保存申报配置（一个纳税年度内不可修改）"""
        return self.post("/server/customer/declare/config/save", json={
            "contactNo": contact_no,
            "items": items,
        })

    def customer_declare_cycles(self):
        """申报周期下拉列表"""
        return self.get("/server/customer/declare/cycles")

    def customer_declare_tax_types(self):
        """税种下拉列表"""
        return self.get("/server/customer/declare/taxTypes")

    def customer_license_detail(self, contact_no):
        """查看证照"""
        return self.get("/server/customer/license/detail", params={"contactNo": contact_no})

    def customer_license_upload(self, contact_no, file_uri):
        """上传/更换证照（前端已上传文件，传文件路径入库）"""
        return self.post("/server/customer/license/upload", params={
            "contactNo": contact_no,
            "fileUri": file_uri,
        })

    # ---------------- 首页 ----------------

    def home(self):
        """首页数据（待处理工单数、本月工单数、本月服务客户数、政策资讯）"""
        return self.get("/server/home")

    # ---------------- 咨询管理 ----------------

    def knowledge_consult_page(self, page_num=1, page_size=10, consult_type=None):
        """咨询列表"""
        payload = {"pageNum": page_num, "pageSize": page_size}
        if consult_type is not None:
            payload["consultType"] = consult_type
        return self.post("/server/knowledge/consult/page", json=payload)

    def knowledge_consult_detail(self, consult_id):
        """咨询详情"""
        return self.get("/server/knowledge/consult/detail", params={"id": consult_id})

    # ---------------- 工单管理 ----------------

    def work_order_page(self, page_num=1, page_size=10):
        """服务进度管理列表"""
        payload = {"pageNum": page_num, "pageSize": page_size}
        return self.post("/server/workOrder/page", json=payload)

    def work_order_detail(self, work_order_id):
        """服务进度管理详情"""
        return self.get("/server/workOrder/detail", params={"workOrderId": work_order_id})

    def work_order_accept(self, work_order_id):
        """服务商接单"""
        return self.post("/server/workOrder/accept", json={"workOrderId": work_order_id})

    def work_order_reject(self, work_order_id, reject_reason):
        """服务商拒绝接单"""
        return self.post("/server/workOrder/reject", json={
            "workOrderId": work_order_id,
            "rejectReason": reject_reason,
        })
