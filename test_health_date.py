#!/usr/bin/env python3
"""
测试健康度查询功能（包括日期参数）
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lib.http import get

async def test_health():
    print("=" * 70)
    print("测试健康度查询功能")
    print("=" * 70)

    # 测试1: 不带日期参数（查询最新数据）
    print("\n[测试1] 查询 openEuler 社区最新健康度")
    print("-" * 70)
    result = await get("/health/openeuler/metric", params={"mode": "general"})
    if result.get("code") == 1:
        data = result.get("data", {})
        print(f"✓ 成功")
        print(f"  数据日期: {data.get('created_at')}")
        print(f"  综合评分: {data.get('avg_score')}")
    else:
        print(f"✗ 失败: {result.get('message')}")

    # 测试2: 带日期参数
    print("\n[测试2] 查询 openEuler 社区 2026-03-05 的健康度")
    print("-" * 70)
    result = await get("/health/openeuler/metric", params={"mode": "general", "date": "2026-03-05"})
    if result.get("code") == 1:
        data = result.get("data", {})
        print(f"✓ 成功")
        print(f"  数据日期: {data.get('created_at')}")
        print(f"  综合评分: {data.get('avg_score')}")
    else:
        print(f"✗ 失败: {result.get('message')}")
        print(f"  注意: 后端 API 可能不支持 date 参数")

    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_health())
