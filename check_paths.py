import os
import re

test_files = [
    'test_cases/service_item_module/test_service_item.py',
    'test_cases/contract_service_config_module/test_contact_config.py',
    'test_cases/pricing_module/test_pricing.py',
    'test_cases/knowledge_base_module/test_knowledge_base.py',
    'test_cases/service_provider_module/test_service_provider.py',
    'test_cases/platform_user_module/test_user_change_status.py',
    'test_cases/platform_user_module/test_user_delete.py',
    'test_cases/login_module/test_logout.py',
    'test_cases/boundary_values/test_boundary_values.py',
]

for filepath in test_files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f'\n=== {filepath} ===')
        for i, line in enumerate(lines, 1):
            if '/platform/' in line or '/sys/' in line:
                paths = re.findall(r'["\'](/[^"\']+)["\']', line)
                if paths:
                    print(f'  Line {i}: {paths[0]}')
