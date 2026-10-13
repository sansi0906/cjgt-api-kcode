import json
from datetime import datetime

with open('bug_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Group by module
modules = {}
for item in results:
    module = item['module']
    if module not in modules:
        modules[module] = []
    modules[module].append(item)

# Generate markdown
md = []
md.append("# Bug List per Module - 2026-08-14")
md.append("")
md.append("生成时间: 2026-08-14")
md.append("测试数据 UUID: f4f44ea8-6713-4c96-9782-a06c2fa3d51d")
md.append("")
md.append("---")
md.append("")

bug_count = 0

for module_name, bugs in modules.items():
    md.append(f"## {module_name}")
    md.append("")
    
    for bug in bugs:
        bug_count += 1
        md.append(f"### Bug {bug_count}: {bug['name']}")
        md.append("")
        md.append("| 项目 | 内容 |")
        md.append("|------|------|")
        md.append(f"| **请求地址** | {bug['url']} |")
        md.append(f"| **入参** | `{bug['params']}` |")
        
        response_str = json.dumps(bug['response'], ensure_ascii=False)
        md.append(f"| **出参** | `{response_str}` |")
        
        resp = bug['response']
        if resp.get('code') in ('00', '0'):
            desc = "后端未做校验，返回成功"
        elif resp.get('code') == '01000009':
            desc = "返回用户状态无效错误"
        elif resp.get('code') == '01000006':
            desc = "返回参数错误"
        elif resp.get('code') == '03':
            desc = "返回资源不存在错误"
        elif resp.get('code') == '02':
            desc = "返回系统异常"
        else:
            desc = "后端返回异常"
        
        md.append(f"| **Bug描述** | {desc} |")
        md.append("")
        
        # Interface verification
        md.append("**接口验证**:")
        md.append(f"- 请求方法: POST")
        md.append(f"- 请求路径: {bug['url']}")
        md.append(f"- 实际响应码: {resp.get('code')}")
        md.append(f"- 实际响应消息: {resp.get('message', 'N/A')}")
        md.append("")
        md.append("---")
        md.append("")

# Summary
md.append("## Bug 统计")
md.append("")
md.append("| 模块 | Bug 数量 |")
md.append("|------|----------|")
total = 0
for module_name, bugs in modules.items():
    md.append(f"| {module_name} | {len(bugs)} |")
    total += len(bugs)
md.append(f"| **总计** | **{total}** |")
md.append("")

content = '\n'.join(md)
with open('reports/bug_lists/bug_list_per_module_20260814.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Generated bug list with {total} bugs")
print("Saved to: reports/bug_lists/bug_list_per_module_20260814.md")
