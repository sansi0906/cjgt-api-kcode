import re
with open('api_clients/jeecgboot_client.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all API paths
paths = re.findall(r'["\'](/[^"\']+)["\']', content)
unique_paths = sorted(set(paths))
print('=== API paths in jeecgboot_client.py ===')
for path in unique_paths:
    if '/platform/' in path or '/sys/' in path:
        print(path)
