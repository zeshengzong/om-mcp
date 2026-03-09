#!/usr/bin/env python3
"""
MCP 工具测试脚本
模拟真实 PPT 制作场景，构造问题并调用各 MCP 工具验证返回结果。
"""
import asyncio
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 直接 import 各 tool 模块中的函数（绕过 MCP 框架，直接调用底层 async 函数）
from lib.http import get, post, extract_data, API_BASE_URL


# ─── 直接复用各工具的业务逻辑 ────────────────────────────────────────────────

async def tool_get_community_list():
    result = await post("/community/list")
    data = result.get("data", [])
    return f"共 {len(data)} 个社区：" + ", ".join(data)

async def tool_get_metric_dict():
    result = await get("/dict/metric")
    data = extract_data(result)
    return "\n".join([f"  [{m['name']}] {m['name_zh']} — {m.get('areasofuse_zh','')}" for m in (data or [])])

async def tool_get_project_hotspot():
    result = await post("/project/hotspot")
    data = extract_data(result)
    if not data:
        return "（数据库暂无数据）"
    return "\n".join([f"  {r['repo_name']} 更新于 {r['updated_at']}" for r in data])

async def tool_get_project_active():
    result = await post("/project/active")
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = extract_data(result) or {}
    return f"总仓库 {data.get('total_repos')}，活跃 {data.get('active_repos')}，非活跃 {data.get('inactive_repos')}"

async def tool_get_project_topn_company_pr():
    result = await post("/project/topn/company/pr")
    data = extract_data(result)
    return "\n".join([f"  {i+1}. {d['company']} {d['count']} PR ({d['percentage']}%)" for i, d in enumerate(data or [])])

async def tool_get_project_topn_user_pr():
    result = await post("/project/topn/user/pr")
    data = extract_data(result)
    return "\n".join([f"  {i+1}. {d['name']}({d['user']}) {d['count']} PR [{d['company']}]" for i, d in enumerate(data or [])])

async def tool_get_issues_aggregate(community=""):
    body = {}
    if community:
        body["community"] = community
    result = await post("/query/issues/agg", body)
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = extract_data(result) or {}
    return (f"总数 {data.get('total_count')}，开启 {data.get('open_count')}，关闭 {data.get('closed_count')}，"
            f"关闭率 {data.get('closed_ratio')}，平均响应 {data.get('avg_first_reply_time')} 天")

async def tool_get_issues_by_sig(community=""):
    body = {}
    if community:
        body["community"] = community
    result = await post("/query/issues/agg/sig", body)
    data = extract_data(result)
    sig_list = data.get("list", []) if isinstance(data, dict) else []
    return "\n".join([f"  [{s['sig_name']}] {s['count']} issues，关闭率 {s['closed_ratio']}" for s in sig_list])

async def tool_get_prs_aggregate(community=""):
    body = {}
    if community:
        body["community"] = community
    result = await post("/query/prs/agg", body)
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = extract_data(result) or {}
    return (f"总数 {data.get('total_count')}，开启 {data.get('open_count')}，合并 {data.get('merged_count')}，"
            f"合并率 {data.get('merged_ratio')}，关闭率 {data.get('closed_ratio')}")

async def tool_get_prs_by_sig(community=""):
    body = {}
    if community:
        body["community"] = community
    result = await post("/query/prs/agg/sig", body)
    data = extract_data(result)
    sig_list = data.get("list", []) if isinstance(data, dict) else []
    return "\n".join([f"  [{s['sig_name']}] {s['count']} PRs，关闭率 {s['closed_ratio']}" for s in sig_list])

async def tool_get_repo_user_list(community="", page=1):
    body = {"page": page, "page_size": 10}
    if community:
        body["community"] = community
    result = await post("/query/repo/user/page", body)
    data = extract_data(result)
    user_list = data.get("list", []) if isinstance(data, dict) else []
    return "\n".join([f"  {u['user_name']}({u['user_login']}) PR:{u['pr_count']} Issue:{u['issue_count']}" for u in user_list])

async def tool_get_cla_stats(community="openubmc", start_time="", end_time=""):
    body = {"community": community}
    if start_time:
        body["start_time"] = start_time
    if end_time:
        body["end_time"] = end_time
    result = await post("/cla/stats", body)
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = result.get("data") or {}
    return f"总计 {data.get('total')}，企业 {data.get('enterprise')}，个人 {data.get('individual')}"

async def tool_get_cla_trend(community="openubmc", interval="month"):
    result = await post("/cla/trend", {"community": community, "interval": interval})
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = result.get("data") or []
    return "\n".join([f"  {d['date']}：总 {d['total']}，企业 {d['enterprise']}，个人 {d['individual']}" for d in data])

async def tool_get_cla_user_list(community="openubmc", page=1, page_size=5):
    result = await post("/cla/page", {"community": community, "page": page, "pageSize": page_size})
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = result.get("data") or {}
    user_list = data.get("list", [])
    total = data.get("total", 0)
    lines = [f"共 {total} 人："]
    for u in user_list:
        lines.append(f"  {u.get('name')} ({u.get('email')}) [{u.get('sign_type')}] {u.get('company')}")
    return "\n".join(lines)

async def tool_get_ci_metrics(community=""):
    body = {}
    if community:
        body["community"] = community
    result = await post("/project/ci/metric", body)
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = extract_data(result) or {}
    return (f"总运行 {data.get('total_runs')}，成功 {data.get('success_count')}，失败 {data.get('failed_count')}，"
            f"成功率 {data.get('success_rate', 0)*100:.0f}%，平均时长 {data.get('avg_duration')} 分钟")

async def tool_get_community_health(community="openEuler"):
    """调用已有的健康度接口"""
    from tools.health import COMMUNITY_MAP, METRIC_LABELS
    key = community.strip().lower()
    api_community = COMMUNITY_MAP.get(key, community)
    result = await get(f"/health/{api_community}/metric", params={"mode": "general"})
    if result.get("code") != 1:
        return f"API 错误：{result.get('message', '未知错误')}"
    data = result.get("data")
    if not data:
        return f"社区 {api_community} 暂无健康度数据"
    avg = data.get("avg_score", "N/A")
    return f"综合健康度：{avg}/5.0，数据日期：{data.get('created_at', 'N/A')}"


# ─── 测试用例 ──────────────────────────────────────────────────────────────────

TESTS = [
    # (问题描述, 调用的工具函数, 参数kwargs)
    ("PPT需要：有哪些社区可以查询？",
     tool_get_community_list, {}),

    ("PPT需要：指标字典里有哪些衡量指标？",
     tool_get_metric_dict, {}),

    ("PPT需要：展示社区热点仓库（最近更新的项目）",
     tool_get_project_hotspot, {}),

    ("PPT需要：社区活跃项目数量概览",
     tool_get_project_active, {}),

    ("PPT需要：哪些企业 PR 贡献最多？（Top N 企业贡献排行）",
     tool_get_project_topn_company_pr, {}),

    ("PPT需要：个人开发者 PR 贡献排行榜",
     tool_get_project_topn_user_pr, {}),

    ("PPT需要：Issue 整体处理能力怎么样？（总数、关闭率、响应速度）",
     tool_get_issues_aggregate, {}),

    ("PPT需要：各 SIG 组的 Issue 分布情况",
     tool_get_issues_by_sig, {}),

    ("PPT需要：PR 整体合并情况统计",
     tool_get_prs_aggregate, {}),

    ("PPT需要：各 SIG 组的 PR 贡献分布",
     tool_get_prs_by_sig, {}),

    ("PPT需要：社区最活跃的开发者名单",
     tool_get_repo_user_list, {}),

    ("PPT需要：openubmc 社区 CLA 签署总体情况",
     tool_get_cla_stats, {"community": "openubmc"}),

    ("PPT需要：openubmc 社区 CLA 签署月度趋势",
     tool_get_cla_trend, {"community": "openubmc", "interval": "month"}),

    ("PPT需要：openubmc 社区已签署 CLA 的用户列表",
     tool_get_cla_user_list, {"community": "openubmc", "page": 1, "page_size": 5}),

    ("PPT需要：CI 持续集成质量数据（成功率、运行次数）",
     tool_get_ci_metrics, {}),

    ("PPT需要：openEuler 社区健康度综合评分",
     tool_get_community_health, {"community": "openEuler"}),

    ("PPT需要：MindSpore 社区 CLA 签署统计",
     tool_get_cla_stats, {"community": "mindspore"}),

    ("PPT需要：openEuler 社区各 SIG 的 PR 情况",
     tool_get_prs_by_sig, {"community": "openeuler"}),
]


async def run_tests():
    print("=" * 70)
    print("  MCP 工具测试报告 — om-metrics MCP Server")
    print("=" * 70)
    print(f"  远程 API：{API_BASE_URL}")
    print(f"  共 {len(TESTS)} 个测试场景\n")

    passed = 0
    failed = 0

    for i, (question, func, kwargs) in enumerate(TESTS, 1):
        print(f"{'─'*70}")
        print(f"[{i:02d}] 问题：{question}")
        print(f"      工具：{func.__name__}({', '.join(f'{k}={v!r}' for k,v in kwargs.items()) if kwargs else ''})")
        try:
            result = await func(**kwargs)
            status = "✓ 成功"
            passed += 1
        except Exception as e:
            result = f"ERROR: {e}"
            status = "✗ 失败"
            failed += 1
        print(f"      状态：{status}")
        print(f"      返回：")
        for line in result.split("\n"):
            print(f"        {line}")
        print()

    print("=" * 70)
    print(f"  测试结果：{passed} 成功 / {failed} 失败 / 共 {len(TESTS)} 项")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_tests())
