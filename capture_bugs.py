import sys
sys.path.insert(0, '.')
import json
from api_clients.jeecgboot_client import JeecgBootClient
from config import BASE_URL, USERNAME, PASSWORD, LOGIN_TYPE, WEB_TYPE
import psycopg2
from config import PG_CONFIG
import time

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
print("=== 1. Logout without token ===")
client = get_client()
client.set_token('')
resp = client.post('/sys/logout', json={})
results.append({
    'name': 'Logout without token',
    'url': '/sys/logout',
    'params': '无 Authorization 请求头',
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 2. Delete non-existing service provider
print("=== 2. Delete non-existing service provider ===")
client = get_client()
resp = client.post('/platform/serverUser/delete', json={'id': 999999})
results.append({
    'name': 'Delete non-existing service provider',
    'url': '/platform/serverUser/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 3. Change status non-existing service provider
print("=== 3. Change status non-existing service provider ===")
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': 999999, 'status': 1})
results.append({
    'name': 'Change status non-existing service provider',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': 999999, 'status': 1}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 4. Change status invalid value
print("=== 4. Change status invalid value ===")
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': provider_id, 'status': 2})
results.append({
    'name': 'Change status invalid value',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': provider_id, 'status': 2}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 5. Service item billing method 0
print("=== 5. Service item billing method 0 ===")
client = get_client()
resp = client.post('/platform/serviceItem/add', json={'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'name': 'Service item billing method 0',
    'url': '/platform/serviceItem/add',
    'params': json.dumps({'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 6. Service item billing method overflow
print("=== 6. Service item billing method overflow ===")
client = get_client()
resp = client.post('/platform/serviceItem/add', json={'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'name': 'Service item billing method overflow',
    'url': '/platform/serviceItem/add',
    'params': json.dumps({'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 7. Edit service item billing method 0
print("=== 7. Edit service item billing method 0 ===")
client = get_client()
resp = client.post('/platform/serviceItem/edit', json={'id': service_item_id, 'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'name': 'Edit service item billing method 0',
    'url': '/platform/serviceItem/edit',
    'params': json.dumps({'id': service_item_id, 'itemName': 'TestItem', 'billingMethod': 0, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 8. Edit service item billing method overflow
print("=== 8. Edit service item billing method overflow ===")
client = get_client()
resp = client.post('/platform/serviceItem/edit', json={'id': service_item_id, 'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'})
results.append({
    'name': 'Edit service item billing method overflow',
    'url': '/platform/serviceItem/edit',
    'params': json.dumps({'id': service_item_id, 'itemName': 'TestItem2', 'billingMethod': 2147483647, 'subtitle': 'Test', 'itemDesc': 'Test'}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 9. Page service items negative pageNum
print("=== 9. Page service items negative pageNum ===")
client = get_client()
resp = client.post('/platform/serviceItem/list', json={'pageNum': -1, 'pageSize': 10})
results.append({
    'name': 'Page service items negative pageNum',
    'url': '/platform/serviceItem/list',
    'params': json.dumps({'pageNum': -1, 'pageSize': 10}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 10. Page service items zero pageSize
print("=== 10. Page service items zero pageSize ===")
client = get_client()
resp = client.post('/platform/serviceItem/list', json={'pageNum': 1, 'pageSize': 0})
results.append({
    'name': 'Page service items zero pageSize',
    'url': '/platform/serviceItem/list',
    'params': json.dumps({'pageNum': 1, 'pageSize': 0}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 11. Update status invalid isDisplay 2
print("=== 11. Update status invalid isDisplay 2 ===")
client = get_client()
resp = client.post('/platform/serviceItem/updateStatus', json={'id': service_item_id, 'isDisplay': 2})
results.append({
    'name': 'Update status invalid isDisplay 2',
    'url': '/platform/serviceItem/updateStatus',
    'params': json.dumps({'id': service_item_id, 'isDisplay': 2}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 12. Update status invalid isDisplay -1
print("=== 12. Update status invalid isDisplay -1 ===")
client = get_client()
resp = client.post('/platform/serviceItem/updateStatus', json={'id': service_item_id, 'isDisplay': -1})
results.append({
    'name': 'Update status invalid isDisplay -1',
    'url': '/platform/serviceItem/updateStatus',
    'params': json.dumps({'id': service_item_id, 'isDisplay': -1}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 13. Delete non-existing service provider
print("=== 13. Delete non-existing service provider ===")
client = get_client()
resp = client.post('/platform/serverUser/delete', json={'id': 999999})
results.append({
    'name': 'Delete non-existing service provider',
    'url': '/platform/serverUser/delete',
    'params': json.dumps({'id': 999999}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 14. Change status non-existing user
print("=== 14. Change status non-existing user ===")
client = get_client()
resp = client.post('/platform/serverUser/changeStatus', json={'id': 999999, 'status': 1})
results.append({
    'name': 'Change status non-existing user',
    'url': '/platform/serverUser/changeStatus',
    'params': json.dumps({'id': 999999, 'status': 1}),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

# 15. Invalid phone format
print("=== 15. Invalid phone format ===")
client = get_client()
resp = client.post('/platform/serverUser/save', json={
    'companyName': 'TestCompany',
    'unifiedSocialCode': '91110000000000000',
    'officeAddress': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
    'serviceArea': [{'code': '110000000000', 'name': '北京市', 'level': 'province'}],
    'contactPerson': 'TestPerson',
    'contactPhone': '12345',
    'serviceItems': [1],
})
results.append({
    'name': 'Invalid phone format',
    'url': '/platform/serverUser/save',
    'params': json.dumps({
        'companyName': 'TestCompany',
        'unifiedSocialCode': '91110000000000000',
        'officeAddress': [{'code': '110101000000', 'name': '东城区', 'level': 'county'}],
        'serviceArea': [{'code': '110000000000', 'name': '北京市', 'level': 'province'}],
        'contactPerson': 'TestPerson',
        'contactPhone': '12345',
        'serviceItems': [1],
    }),
    'response': resp.json()
})
print(f'Response: {resp.json()}')
print()

print(f"Total results: {len(results)}")
with open('bug_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved to bug_results.json")
