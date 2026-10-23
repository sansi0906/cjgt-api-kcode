"""
factories.py - 统一测试数据工厂
====================================
提供各模块测试数据的统一创建方法，减少测试间重复代码。
"""

import time
import random


class UserFactory:
    """平台用户测试数据工厂"""

    @staticmethod
    def build(user_id=None, user_name=None, real_name=None, sex=1, role_group_id=5, status=1):
        """构建平台用户数据"""
        return {
            "id": user_id,
            "userName": user_name or f"174{random.randint(10000000, 99999999)}",
            "realName": real_name or f"测试用户{int(time.time())}",
            "sex": sex,
            "roleGroupId": role_group_id,
            "status": status,
        }

    @staticmethod
    def build_save_payload(**overrides):
        """构建保存用户请求体（不含 id）"""
        payload = UserFactory.build(**overrides)
        payload.pop("id", None)
        return payload

    @staticmethod
    def build_edit_payload(user_id, **overrides):
        """构建编辑用户请求体（含 id）"""
        payload = UserFactory.build(user_id=user_id, **overrides)
        return payload

    @staticmethod
    def build_save_params(**overrides):
        """构建保存用户请求参数（蛇形命名，可直接传给 save_platform_user(**params)）"""
        payload = UserFactory.build(**overrides)
        payload.pop("id", None)
        return {
            "user_name": payload.pop("userName"),
            "real_name": payload.pop("realName"),
            "sex": payload.pop("sex"),
            "role_group_id": payload.pop("roleGroupId"),
            "status": payload.pop("status"),
        }


class BusinessScopeFactory:
    """经营范围测试数据工厂"""

    @staticmethod
    def build(scope_id=None, scope_name=None, remark=None, is_enabled=1):
        """构建经营范围数据"""
        return {
            "id": scope_id,
            "scopeName": scope_name or f"Scope{int(time.time() * 1000) % 100000}",
            "remark": remark or "TestRemark",
            "isEnabled": is_enabled,
        }

    @staticmethod
    def build_add_payload(**overrides):
        """构建新增经营范围请求体"""
        scope_name = overrides.pop("scopeName", None) or overrides.pop("scope_name", None)
        remark = overrides.pop("remark", None)
        payload = BusinessScopeFactory.build(scope_name=scope_name, remark=remark)
        return payload

    @staticmethod
    def build_add_params(**overrides):
        """构建新增经营范围请求参数（驼峰键，可直接用于 create_by_api）"""
        return BusinessScopeFactory.build_add_payload(**overrides)

    @staticmethod
    def build_edit_payload(scope_id, **overrides):
        """构建编辑经营范围请求体"""
        payload = BusinessScopeFactory.build(scope_id=scope_id, **overrides)
        payload.pop("isEnabled", None)
        return payload


class KnowledgeBaseFactory:
    """知识库测试数据工厂"""

    @staticmethod
    def build(
        knowledge_id=None,
        title=None,
        content=None,
        consult_type=1,
        display_position=None,
        applicable_area=None,
        status=1,
    ):
        """构建知识库数据"""
        return {
            "id": knowledge_id,
            "title": title or f"KB{int(time.time() * 1000) % 100000}",
            "content": content or "TestContent",
            "consultType": consult_type,
            "displayPosition": display_position or [0, 1],
            "applicableArea": applicable_area or [
                {"code": "110119000000", "name": "延庆区", "level": "county"}
            ],
            "status": status,
        }

    @staticmethod
    def build_save_payload(**overrides):
        """构建保存知识库请求体（不含 id），支持驼峰键别名"""
        camel_to_snake = {
            "consultType": "consult_type",
            "displayPosition": "display_position",
            "applicableArea": "applicable_area",
        }
        mapped = {}
        for k, v in overrides.items():
            mapped[camel_to_snake.get(k, k)] = v
        payload = KnowledgeBaseFactory.build(**mapped)
        payload.pop("id", None)
        return payload

    @staticmethod
    def build_edit_payload(knowledge_id, **overrides):
        """构建编辑知识库请求体"""
        payload = KnowledgeBaseFactory.build(knowledge_id=knowledge_id, **overrides)
        return payload


class ServiceItemFactory:
    """服务项目测试数据工厂"""

    @staticmethod
    def build(item_id=None, item_name=None, billing_method=1, subtitle=None, item_desc=None, is_display=1):
        """构建服务项目数据"""
        return {
            "id": item_id,
            "itemName": item_name or f"Item{int(time.time() * 1000) % 100000}",
            "billingMethod": billing_method,
            "subtitle": subtitle or "TestSubtitle",
            "itemDesc": item_desc or "TestDesc",
            "isDisplay": is_display,
        }

    @staticmethod
    def build_add_payload(**overrides):
        """构建新增服务项目请求体"""
        payload = ServiceItemFactory.build(**overrides)
        payload.pop("id", None)
        payload.pop("isDisplay", None)
        return payload

    @staticmethod
    def build_edit_payload(item_id, **overrides):
        """构建编辑服务项目请求体"""
        payload = ServiceItemFactory.build(item_id=item_id, **overrides)
        return payload

    @staticmethod
    def build_add_params(**overrides):
        """构建新增服务项目请求参数（蛇形命名，可直接传给 add_service_item(**params)）"""
        item_code = overrides.pop("item_code", None)
        payload = ServiceItemFactory.build(**overrides)
        return {
            "item_name": payload.pop("itemName"),
            "billing_method": payload.pop("billingMethod"),
            "subtitle": payload.pop("subtitle"),
            "icon_url": None,
            "item_desc": payload.pop("itemDesc"),
            "item_code": item_code,
        }


class ServiceProviderFactory:
    """服务商测试数据工厂"""

    @staticmethod
    def build(
        provider_id=None,
        company_name=None,
        unified_social_code=None,
        office_address=None,
        service_area=None,
        contact_person=None,
        contact_phone=None,
        service_items=None,
        status=1,
    ):
        """构建服务商数据"""
        return {
            "id": provider_id,
            "companyName": company_name or f"测试服务商-{int(time.time())}",
            "unifiedSocialCode": unified_social_code or f"9119{int(time.time()) % 1000000000000:012d}",
            "officeAddress": office_address or [{"code": "110101000000", "name": "东城区", "level": "county"}],
            "serviceArea": service_area or [{"code": "110000000000", "name": "北京市", "level": "province"}],
            "contactPerson": contact_person or "TestPerson",
            "contactPhone": contact_phone or "74955953457",
            "serviceItems": service_items or [1],
            "status": status,
        }

    @staticmethod
    def build_save_payload(**overrides):
        """构建保存服务商请求体（不含 id），支持驼峰键别名映射"""
        camel_to_snake = {
            "companyName": "company_name",
            "unifiedSocialCode": "unified_social_code",
            "officeAddress": "office_address",
            "serviceArea": "service_area",
            "contactPerson": "contact_person",
            "contactPhone": "contact_phone",
            "serviceItems": "service_items",
        }
        build_kwargs = {}
        extra = {}
        for k, v in overrides.items():
            if k in camel_to_snake:
                build_kwargs[camel_to_snake[k]] = v
            else:
                extra[k] = v
        payload = ServiceProviderFactory.build(**build_kwargs)
        payload.pop("id", None)
        payload.update(extra)
        return payload

    @staticmethod
    def build_edit_payload(provider_id, **overrides):
        """构建编辑服务商请求体"""
        payload = ServiceProviderFactory.build(provider_id=provider_id, **overrides)
        return payload


class PricingFactory:
    """定价测试数据工厂"""

    @staticmethod
    def build(service_item_id, amount=100.0, area_list=None):
        """构建定价更新请求体"""
        return {
            "serviceItemId": service_item_id,
            "amount": amount,
            "areaList": area_list or [{"code": "110101000000", "level": "county", "name": "东城区"}],
        }

    @staticmethod
    def build_tree_query(service_item_id):
        """构建定价树查询请求体"""
        return {"serviceItemId": service_item_id}

    @staticmethod
    def build_area_tree_query(service_item_id, area_list=None):
        """构建区域定价树查询请求体"""
        return {
            "serviceItemId": service_item_id,
            "areaList": area_list or [{"code": "110101000000", "level": "county", "name": "东城区"}],
        }

    @staticmethod
    def build_update_payload(service_item_id=None, pending_amount=None, area_list=None, effective_time=None):
        """构建更新定价请求体（驼峰键，可直接用于 JSON 发送）"""
        return {
            "serviceItemId": service_item_id or 289,
            "pendingAmount": pending_amount if pending_amount is not None else 888.0,
            "areaList": area_list or [{"code": "110101000000", "level": "county", "name": "东城区"}],
            "effectiveTime": effective_time,
        }
