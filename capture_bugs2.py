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

# Security tests
client = get_client()

# SQL injection in knowledge title
payloads_sql = ["' OR '1'='1", "' OR 1=1 --", "'; DROP TABLE users; --", "1' UNION SELECT NULL--"]
for payload in payloads_sql:
    resp = client.save_knowledge(
        title=payload,
        content='TestContent',
        consult_type=1,
        display_position=[0, 1],
        applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
    )
    results.append({
        'name': f'SQL injection knowledge title: {payload}',
        'url': '/platform/knowledge/save',
        'params': json.dumps({
            'title': payload,
            'content': 'TestContent',
            'consultType': 1,
            'displayPosition': [0, 1],
            'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
        }),
        'response': resp.json()
    })

# XSS in knowledge title
payloads_xss_title = ["<script>alert('xss')</script>", "<img src=x onerror=alert('xss')>", "<svg onload=alert('xss')>"]
for payload in payloads_xss_title:
    resp = client.save_knowledge(
        title=payload,
        content='TestContent',
        consult_type=1,
        display_position=[0, 1],
        applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
    )
    results.append({
        'name': f'XSS knowledge title: {payload}',
        'url': '/platform/knowledge/save',
        'params': json.dumps({
            'title': payload,
            'content': 'TestContent',
            'consultType': 1,
            'displayPosition': [0, 1],
            'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
        }),
        'response': resp.json()
    })

# XSS in knowledge content
payloads_xss_content = ["<script>alert('xss')</script>", "<img src=x onerror=alert('xss')>", "<svg onload=alert('xss')>"]
for payload in payloads_xss_content:
    resp = client.save_knowledge(
        title='TestTitle',
        content=payload,
        consult_type=1,
        display_position=[0, 1],
        applicable_area=[{'code': '110119000000', 'name': '延庆区', 'level': 'county'}],
    )
    results.append({
        'name': f'XSS knowledge content: {payload}',
        'url': '/platform/knowledge/save',
        'params': json.dumps({
            'title': 'TestTitle',
            'content': payload,
            'consultType': 1,
            'displayPosition': [0, 1],
            'applicableArea': [{'code': '110119000000', 'name': '延庆区', 'level': 'county'}]
        }),
        'response': resp.json()
    })

# User status invalid (boundary_values)
client = get_client()
resp = client.post('/platform/serverUser/save', json={
    'companyName': 'TestCompany',
    'unifiedSocialCode': '91110000000000000',
    'officeAddress': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
    'serviceArea': [{'code': '110000000000', 'name': '北京市', 'level': 'province'}],
    'contactPerson': 'TestPerson',
    'contactPhone': '74955953457',
    'serviceItems': [1],
    'status': 2,
})
results.append({
    'name': 'User status invalid (2)',
    'url': '/platform/serverUser/save',
    'params': json.dumps({
        'companyName': 'TestCompany',
        'unifiedSocialCode': '91110000000000000',
        'officeAddress': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
        'serviceArea': [{'code': '110000000000', 'name': '北京市', 'level': 'province'}],
        'contactPerson': 'TestPerson',
        'contactPhone': '74955953457',
        'serviceItems': [1],
        'status': 2,
    }),
    'response': resp.json()
})

# Pricing amount zero
client = get_client()
resp = client.update_pricing(
    service_item_id=service_item_id,
    amount=0,
    area_list=[{"code": "110101000000", "level": "county", "name": "东城区"}],
)
results.append({
    'name': 'Pricing amount zero',
    'url': '/platform/pricing/update',
    'params': json.dumps({
        'serviceItemId': service_item_id,
        'amount': 0,
        'areaList': [{"code": "110101000000", "level": "county", "name": "东城区"}]
    }),
    'response': resp.json()
})

# Contact config duplicate 1:1
client = get_client()
title_1 = f'合同配置{int(time.time())}'
resp1 = client.save_contact_config(service_item_id=service_item_id, title=title_1)
results.append({
    'name': 'Contact config create (first)',
    'url': '/platform/contactConfig/save',
    'params': json.dumps({'serviceItemId': service_item_id, 'title': title_1}),
    'response': resp1.json()
})

title_2 = f'合同配置{int(time.time()) + 1}'
resp2 = client.save_contact_config(service_item_id=service_item_id, title=title_2)
results.append({
    'name': 'Contact config duplicate 1:1',
    'url': '/platform/contactConfig/save',
    'params': json.dumps({'serviceItemId': service_item_id, 'title': title_2}),
    'response': resp2.json()
})

# Contact config pagination
client = get_client()
resp = client.page_contact_configs(page_num=1, page_size=10)
results.append({
    'name': 'Contact config pagination',
    'url': '/platform/contactConfig/pageList',
    'params': json.dumps({'pageNum': 1, 'pageSize': 10}),
    'response': resp.json()
})

# Contact config detail existing
client = get_client()
resp = client.get_contact_config_detail(config_id=999999)
results.append({
    'name': 'Contact config detail existing',
    'url': '/platform/contactConfig/detail',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# Edit contact config
client = get_client()
resp = client.post('/platform/contactConfig/edit', json={
    'id': 999999,
    'serviceItemId': service_item_id,
    'title': '测试标题',
    'content': 'TestContent',
    'priceContent': 'TestPrice'
})
results.append({
    'name': 'Edit contact config',
    'url': '/platform/contactConfig/edit',
    'params': json.dumps({
        'id': 999999,
        'serviceItemId': service_item_id,
        'title': '测试标题',
        'content': 'TestContent',
        'priceContent': 'TestPrice'
    }),
    'response': resp.json()
})

# Delete contact config
client = get_client()
resp = client.post('/platform/contactConfig/delete', json={'id': 999999})
results.append({
    'name': 'Delete contact config',
    'url': '/platform/contactConfig/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# Invalid JSON response
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
        'name': 'Invalid JSON response',
        'url': '/sys/login',
        'params': '模拟非法 JSON 响应',
        'response': {'status_code': response.status_code, 'text': response.text[:100]}
    })
except Exception as e:
    results.append({
        'name': 'Invalid JSON response',
        'url': '/sys/login',
        'params': '模拟非法 JSON 响应',
        'response': {'error': str(e)}
    })
finally:
    client.session.request = original_request

# Delete non-existing knowledge
client = get_client()
resp = client.post('/platform/knowledge/delete', json={'id': 999999})
results.append({
    'name': 'Delete non-existing knowledge',
    'url': '/platform/knowledge/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# Logout without token
client = get_client()
client.set_token('')
resp = client.post('/sys/logout', json={})
results.append({
    'name': 'Logout without token',
    'url': '/sys/logout',
    'params': '无 Authorization 请求头',
    'response': resp.json()
})

# Change status non-existing user
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': 999999, 'status': 1})
results.append({
    'name': 'Change status non-existing user',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': 999999, 'status': 1}),
    'response': resp.json()
})

# Delete non-existing user
client = get_client()
resp = client.post('/platform/serverUser/delete', json={'id': 999999})
results.append({
    'name': 'Delete non-existing user',
    'url': '/platform/serverUser/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})

# Update pricing no record
client = get_client()
resp = client.post('/platform/pricing/edit', json={
    'id': 999999,
    'serviceItemId': service_item_id,
    'areaList': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
    'amount': 100
})
results.append({
    'name': 'Update pricing no record',
    'url': '/platform/pricing/edit',
    'params': json.dumps({
        'id': 999999,
        'serviceItemId': service_item_id,
        'areaList': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
        'amount': 100
    }),
    'response': resp.json()
})

# Get pricing tree missing areaList
client = get_client()
resp = client.post('/platform/pricing/getTreeByAreas', json={'serviceItemId': 1})
results.append({
    'name': 'Get pricing tree missing areaList',
    'url': '/platform/pricing/getTreeByAreas',
    'params': json.dumps({'serviceItemId': 1}),
    'response': resp.json()
})

print(f"Total results: {len(results)}")
with open('bug_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved to bug_results.json")
