import json
import os
from datetime import datetime

with open('bug_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

modules = {
    '登录模块': [],
    '服务商模块': [],
    '服务项目模块': [],
    '定价模块': [],
    '知识库模块': [],
    '合同服务配置模块': [],
    '异常场景模块': [],
    '边界值模块': [],
    '平台用户模块': [],
}

module_key_map = {
    '登录模块': '登录模块',
    '服务商模块': '服务商模块',
    '服务项目模块': '服务项目模块',
    '定价模块': '定价模块',
    '知识库模块': '知识库模块',
    '合同服务配置模块': '合同服务配置模块',
    '异常场景模块': '异常场景模块',
    '边界值模块': '边界值模块',
    '平台用户模块': '平台用户模块',
}

for item in results:
    module = item.get('module', '')
    target = '其他'
    for key, value in module_key_map.items():
        if key in module:
            target = value
            break
    if target in modules:
        modules[target].append(item)

md = []
md.append("# Bug List per Module")
md.append("")
md.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
md.append("测试数据 UUID: f4f44ea8-6713-4c96-9782-a06c2fa3d51d")
md.append("")
md.append("---")
md.append("")

bug_count = 0

for module_name, bugs in modules.items():
    if not bugs:
        continue

    md.append(f"## {module_name}")
    md.append("")

    for i, bug in enumerate(bugs, 1):
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

        md.append("**接口验证**:")
        md.append(f"- 请求方法: POST")
        md.append(f"- 请求路径: {bug['url']}")
        md.append(f"- 实际响应码: {resp.get('code')}")
        md.append(f"- 实际响应消息: {resp.get('message', 'N/A')}")
        md.append("")
        md.append("---")
        md.append("")

md.append("## Bug 统计")
md.append("")
md.append("| 模块 | Bug 数量 |")
md.append("|------|----------|")
total = 0
for module_name, bugs in modules.items():
    if bugs:
        md.append(f"| {module_name} | {len(bugs)} |")
        total += len(bugs)
md.append(f"| **总计** | **{total}** |")
md.append("")

content = '\n'.join(md)
output_path = 'reports/bug_lists/bug_list_per_module_20260817.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Generated bug list with {total} bugs")
print(f"Saved to: {output_path}")
