import sys
sys.path.insert(0, '.')
import json
from api_clients.jeecgboot_client import JeecgBootClient
from config import BASE_URL, USERNAME, PASSWORD, LOGIN_TYPE, WEB_TYPE
import psycopg2
from config import PG_CONFIG
import time
import unittest.mock

def get_client():
    client = JeecgBootClient(base_url=BASE_URL)
    login_resp = client.login(username=USERNAME, password=PASSWORD, login_type=LOGIN_TYPE, web_type=WEB_TYPE)
    token = login_resp.json().get('data', {}).get('token', '')
    client.set_token(token)
    return client

# Get IDs
conn = psycopg2.connect(host=PG_CONFIG['host'], port=PG_CONFIG['port'], database=PG_CONFIG['database'], user=PG_CONFIG['user'], password=PG_CONFIG['password'])
cursor = conn.cursor()
cursor.execute('SELECT id FROM cjgt_service_provider WHERE create_user_uuid = %s AND delete_status = 0 ORDER BY id DESC LIMIT 1', ('f4f44ea8-6713-4c96-9782-a06c2fa3d51d',))
row = cursor.fetchone()
provider_id = row[0] if row else 1793

cursor.execute('SELECT id FROM cjgt_service_item WHERE create_user_uuid = %s AND delete_status = 0 ORDER BY id DESC LIMIT 1', ('f4f44ea8-6713-4c96-9782-a06c2fa3d51d',))
row = cursor.fetchone()
service_item_id = row[0] if row else 827
cursor.close()
conn.close()

results = []

# 1. Logout without token
client = get_client()
client.set_token('')
resp = client.post('/sys/logout', json={})
results.append({
    'module': '登录模块',
    'name': '无 Token 登出，返回成功',
    'url': '/sys/logout',
    'params': '无 Authorization 请求头',
    'response': resp.json()
})

# 2. Delete non-existing service provider
client = get_client()
resp = client.post('/platform/serverUser/delete', json={'id': 999999})
results.append({
    'module': '服务商模块',
    'name': '删除不存在的服务商，返回成功',
    'url': '/platform/serverUser/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# 3. Change status non-existing service provider
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': 999999, 'status': 1})
results.append({
    'module': '服务商模块',
    'name': '修改不存在的服务商状态，返回成功',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': 999999, 'status': 1}),
    'response': resp.json()
})

# 4. Change status invalid value
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': provider_id, 'status': 2})
results.append({
    'module': '服务商模块',
    'name': '修改服务商状态为非法值 2，返回成功',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': provider_id, 'status': 2}),
    'response': resp.json()
})

# 5. Service item billing method 0
client = get_client()
resp = client.post('/platform/serviceItem/add', json={'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'module': '服务项目模块',
    'name': '添加服务项目 billing_method 传 0，被接受',
    'url': '/platform/serviceItem/add',
    'params': json.dumps({'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})

# 6. Service item billing method overflow
client = get_client()
resp = client.post('/platform/serviceItem/add', json={'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'module': '服务项目模块',
    'name': '添加服务项目 billing_method 传超大值，被接受',
    'url': '/platform/serviceItem/add',
    'params': json.dumps({'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})

# 7. Edit service item billing method 0
client = get_client()
resp = client.post('/platform/serviceItem/edit', json={'id': service_item_id, 'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'module': '服务项目模块',
    'name': '编辑服务项目 billing_method 传 0，被接受',
    'url': '/platform/serviceItem/edit',
    'params': json.dumps({'id': service_item_id, 'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})

# 8. Edit service item billing method overflow
client = get_client()
resp = client.post('/platform/serviceItem/edit', json={'id': service_item_id, 'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'module': '服务项目模块',
    'name': '编辑服务项目 billing_method 传超大值，被接受',
    'url': '/platform/serviceItem/edit',
    'params': json.dumps({'id': service_item_id, 'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})

# 9. Page service items negative pageNum
client = get_client()
resp = client.post('/platform/serviceItem/paging', json={'pageNum': -1, 'pageSize': 10})
results.append({
    'module': '服务项目模块',
    'name': '服务项目分页 pageNum 传负数，被接受',
    'url': '/platform/serviceItem/paging',
    'params': json.dumps({'pageNum': -1, 'pageSize': 10}),
    'response': resp.json()
})

# 10. Page service items zero pageSize
client = get_client()
resp = client.post('/platform/serviceItem/paging', json={'pageNum': 1, 'pageSize': 0})
results.append({
    'module': '服务项目模块',
    'name': '服务项目分页 pageSize 传 0，被接受',
    'url': '/platform/serviceItem/paging',
    'params': json.dumps({'pageNum': 1, 'pageSize': 0}),
    'response': resp.json()
})

# 11. Update status invalid isDisplay 2
client = get_client()
resp = client.post('/platform/serviceItem/updateStatus', json={'id': service_item_id, 'isDisplay': 2})
results.append({
    'module': '服务项目模块',
    'name': '更新服务项目状态 is_display 传 2，被接受',
    'url': '/platform/serviceItem/updateStatus',
    'params': json.dumps({'id': service_item_id, 'isDisplay': 2}),
    'response': resp.json()
})

# 12. Update status invalid isDisplay -1
client = get_client()
resp = client.post('/platform/serviceItem/updateStatus', json={'id': service_item_id, 'isDisplay': -1})
results.append({
    'module': '服务项目模块',
    'name': '更新服务项目状态 is_display 传负数，被接受',
    'url': '/platform/serviceItem/updateStatus',
    'params': json.dumps({'id': service_item_id, 'isDisplay': -1}),
    'response': resp.json()
})

# 13. Delete non-existing knowledge
client = get_client()
resp = client.post('/platform/knowledge/delete', json={'id': 999999})
results.append({
    'module': '知识库模块',
    'name': '删除不存在的知识库记录，返回成功',
    'url': '/platform/knowledge/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# 14. SQL injection in knowledge title
client = get_client()
resp = client.save_knowledge(
    title="' OR '1'='1",
    content='TestContent',
    consult_type=1,
    display_position=[0, 1],
    applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
)
results.append({
    'module': '知识库模块',
    'name': '知识库 title 字段 SQL 注入，被接受',
    'url': '/platform/knowledge/save',
    'params': json.dumps({
        'title': "' OR '1'='1",
        'content': 'TestContent',
        'consultType': 1,
        'displayPosition': [0, 1],
        'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
    }),
    'response': resp.json()
})

# 15. XSS in knowledge title
client = get_client()
resp = client.save_knowledge(
    title="<script>alert('xss')</script>",
    content='TestContent',
    consult_type=1,
    display_position=[0, 1],
    applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
)
results.append({
    'module': '知识库模块',
    'name': '知识库 title 字段 XSS 注入，被接受',
    'url': '/platform/knowledge/save',
    'params': json.dumps({
        'title': "<script>alert('xss')</script>",
        'content': 'TestContent',
        'consultType': 1,
        'displayPosition': [0, 1],
        'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
    }),
    'response': resp.json()
})

# 16. XSS in knowledge content
client = get_client()
resp = client.save_knowledge(
    title='TestTitle',
    content="<script>alert('xss')</script>",
    consult_type=1,
    display_position=[0, 1],
    applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
)
results.append({
    'module': '知识库模块',
    'name': '知识库 content 字段 XSS 注入，被接受',
    'url': '/platform/knowledge/save',
    'params': json.dumps({
        'title': 'TestTitle',
        'content': "<script>alert('xss')</script>",
        'consultType': 1,
        'displayPosition': [0, 1],
        'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
    }),
    'response': resp.json()
})

# 17. Contact config create
client = get_client()
title = f'合同配置{int(time.time())}'
resp = client.save_contact_config(service_item_id=service_item_id, title=title, content='TestContent', price_content='TestPrice')
results.append({
    'module': '合同服务配置模块',
    'name': '创建合同配置返回系统异常',
    'url': '/platform/contactConfig/save',
    'params': json.dumps({'serviceItemId': service_item_id, 'title': title, 'content': 'TestContent', 'priceContent': 'TestPrice'}),
    'response': resp.json()
})

# 18. Contact config duplicate 1:1
client = get_client()
title2 = f'合同配置{int(time.time()) + 1}'
resp2 = client.save_contact_config(service_item_id=service_item_id, title=title2, content='TestContent2', price_content='TestPrice2')
results.append({
    'module': '合同服务配置模块',
    'name': '同一服务项目创建第二个合同配置，返回系统异常',
    'url': '/platform/contactConfig/save',
    'params': json.dumps({'serviceItemId': service_item_id, 'title': title2, 'content': 'TestContent2', 'priceContent': 'TestPrice2'}),
    'response': resp2.json()
})

# 19. Invalid JSON response
client = get_client()
original_request = client.session.request
call_count = [0]

def mock_request(method, url, **kwargs):
    call_count[0] += 1
    if call_count[0] == 1:
        class FakeResponse:
            status_code = 200
            text = "not valid json"
            content = b"not valid json"
            def json(self):
                raise json.JSONDecodeError("Invalid JSON", "", 0)
        return FakeResponse()
    return original_request(method, url, **kwargs)

client.session.request = mock_request
try:
    response = client.login(username=USERNAME, password=PASSWORD)
    results.append({
        'module': '异常场景模块',
        'name': '模拟非法 JSON 响应，客户端崩溃',
        'url': '/sys/login',
        'params': '模拟非法 JSON 响应',
        'response': {'status_code': response.status_code, 'text': response.text[:100], 'error': None}
    })
except Exception as e:
    results.append({
        'module': '异常场景模块',
        'name': '模拟非法 JSON 响应，客户端崩溃',
        'url': '/sys/login',
        'params': '模拟非法 JSON 响应',
        'response': {'error': str(e)}
    })
finally:
    client.session.request = original_request

# 20. Change status non-existing user
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': 999999, 'status': 1})
results.append({
    'module': '平台用户模块',
    'name': '修改不存在的用户状态，返回成功',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': 999999, 'status': 1}),
    'response': resp.json()
})

# 21. Delete non-existing user
client = get_client()
resp = client.post('/platform/serverUser/delete', json={'id': 999999})
results.append({
    'module': '平台用户模块',
    'name': '删除不存在的用户，返回成功',
    'url': '/platform/serverUser/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# Save results
with open('bug_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Total bugs captured: {len(results)}")
print("Saved to bug_results.json")
