"""
collect_test_bugs.py - 从当前测试结果收集 Bug 并生成 Bug 清单
==============================================================
读取 pytest 的 junitxml 输出或 allure 结果，提取失败用例，
生成按模块分组的 Bug 清单 Markdown 文件。
"""

import json
import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

REPORTS_DIR = "reports"
BUG_LISTS_DIR = os.path.join(REPORTS_DIR, "bug_lists")


def run_tests_and_collect():
    """运行测试并收集失败用例"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    junitxml_path = os.path.join(REPORTS_DIR, f"junit_{timestamp}.xml")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "test_cases",
        f"--junitxml={junitxml_path}",
        "-v", "--tb=short", "--no-header", "-p", "no:cacheprovider",
    ]
    
    print(f"Running tests: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    return junitxml_path, timestamp


def parse_junit_xml(xml_path):
    """解析 JUnit XML 报告，提取失败用例"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    failures = []
    for testcase in root.iter("testcase"):
        failure = testcase.find("failure")
        error = testcase.find("error")
        skipped = testcase.find("skipped")
        
        if failure is not None or error is not None:
            classname = testcase.get("classname", "")
            name = testcase.get("name", "")
            time = testcase.get("time", "")
            
            message = ""
            if failure is not None:
                message = failure.get("message", "")
            elif error is not None:
                message = error.get("message", "")
            
            failures.append({
                "classname": classname,
                "name": name,
                "message": message,
                "time": time,
            })
    
    return failures


def module_from_classname(classname):
    """从类名提取模块名"""
    if "service_provider" in classname:
        return "服务商模块"
    elif "service_item" in classname:
        return "服务项目模块"
    elif "pricing" in classname:
        return "定价模块"
    elif "knowledge_base" in classname:
        return "知识库模块"
    elif "contact_config" in classname or "agreement" in classname or "contract" in classname:
        return "合同服务配置模块"
    elif "business_scope" in classname:
        return "经营范围模块"
    elif "login" in classname or "logout" in classname:
        return "登录模块"
    elif "user" in classname:
        return "平台用户模块"
    elif "role" in classname:
        return "角色管理模块"
    elif "security" in classname:
        return "安全测试"
    elif "boundary" in classname:
        return "边界值模块"
    elif "exception" in classname:
        return "异常场景模块"
    elif "worker_sign" in classname or "gongrenle" in classname:
        return "工人入驻签署模块"
    elif "token_expiration" in classname:
        return "Token 过期模块"
    else:
        return "其他"


def generate_bug_list(failures, timestamp):
    """生成 Bug 清单 Markdown"""
    os.makedirs(BUG_LISTS_DIR, exist_ok=True)
    
    modules = {}
    for item in failures:
        module = module_from_classname(item["classname"])
        if module not in modules:
            modules[module] = []
        modules[module].append(item)
    
    md = []
    md.append("# Bug List")
    md.append("")
    md.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"测试数据 UUID: f4f44ea8-6713-4c96-9782-a06c2fa3d51d")
    md.append("")
    md.append("---")
    md.append("")
    
    bug_count = 0
    
    for module_name, bugs in modules.items():
        if not bugs:
            continue
        
        md.append(f"## {module_name}")
        md.append("")
        
        for bug in bugs:
            bug_count += 1
            md.append(f"### Bug {bug_count}: {bug['name']}")
            md.append("")
            md.append("| 项目 | 内容 |")
            md.append("|------|------|")
            md.append(f"| **测试类** | {bug['classname']} |")
            md.append(f"| **测试用例** | {bug['name']} |")
            md.append(f"| **错误信息** | {bug['message']} |")
            md.append(f"| **执行时间** | {bug['time']}s |")
            md.append("")
            md.append("---")
            md.append("")
    
    md.append("## Bug 统计")
    md.append("")
    md.append("| 模块 | Bug 数量 |")
    md.append("|------|----------|")
    for module_name, bugs in modules.items():
        if bugs:
            md.append(f"| {module_name} | {len(bugs)} |")
    md.append(f"| **总计** | **{bug_count}** |")
    md.append("")
    
    content = '\n'.join(md)
    output_path = os.path.join(BUG_LISTS_DIR, f"bug_list_{timestamp}.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated bug list with {bug_count} bugs")
    print(f"Saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    xml_path, timestamp = run_tests_and_collect()
    failures = parse_junit_xml(xml_path)
    generate_bug_list(failures, timestamp)
