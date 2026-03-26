#!/usr/bin/env python3
"""
社区运营质量周报/月报生成脚本

Usage: python3 gen_report.py [--period month|week] community1 community2 ...
Output:
- 月报: reports/{community}_community_quality_monthly_{YYYYMM}.md
- 周报: reports/{community}_community_quality_weekly_{YYYY}W{WW}.md
"""
import argparse
import asyncio
import httpx
import json
import sys
import os
from datetime import datetime, timedelta, timezone
from calendar import monthrange

BASE_URL = "https://datastat.osinfra.cn/server"
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))


# ─── 时间段计算 ───────────────────────────────────────────────────────────────

def fmt_date(dt: datetime) -> str:
    return f"{dt.year}年{dt.month}月{dt.day}日"


def start_of_day_ms(dt: datetime) -> int:
    return int(dt.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)

def month_range_ms(year: int, month: int):
    """返回某年月的首日00:00:00和末日23:59:59的毫秒时间戳（UTC）。"""
    _, last_day = monthrange(year, month)
    start = int(datetime(year, month, 1, tzinfo=timezone.utc).timestamp() * 1000)
    end = int(datetime(year, month, last_day, 23, 59, 59, tzinfo=timezone.utc).timestamp() * 1000)
    return start, end


def month_last_day_ms(year: int, month: int):
    """返回某年月末日00:00:00的毫秒时间戳（UTC）。用于单时间点 API。"""
    _, last_day = monthrange(year, month)
    return int(datetime(year, month, last_day, tzinfo=timezone.utc).timestamp() * 1000)


def week_range_ms(year: int, week: int):
    """返回某 ISO 周的周一00:00:00和周日23:59:59的毫秒时间戳（UTC）。"""
    start_dt = datetime.fromisocalendar(year, week, 1).replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisocalendar(year, week, 7).replace(
        hour=23, minute=59, second=59, microsecond=0, tzinfo=timezone.utc
    )
    return int(start_dt.timestamp() * 1000), int(end_dt.timestamp() * 1000)


def week_last_day_ms(year: int, week: int):
    """返回某 ISO 周周日00:00:00的毫秒时间戳（UTC）。用于单时间点 API。"""
    sunday = datetime.fromisocalendar(year, week, 7).replace(tzinfo=timezone.utc)
    return int(sunday.timestamp() * 1000)


def build_month_period(year: int, month: int, start: int, end: int) -> dict:
    last_day = monthrange(year, month)[1]
    return {
        "mode": "month",
        "year": year,
        "month": month,
        "start": start,
        "end": end,
        "last_day_ms": month_last_day_ms(year, month),
        "label": f"{month}月",
        "range_label": f"{year}年{month}月1日 ～ {year}年{month}月{last_day}日",
        "match_prefix": f"{year}-{month:02d}",
    }


def build_week_period(year: int, week: int, start: int, end: int) -> dict:
    start_dt = datetime.fromtimestamp(start / 1000, tz=timezone.utc)
    end_dt = datetime.fromtimestamp(end / 1000, tz=timezone.utc)
    sunday_dt = datetime.fromisocalendar(year, week, 7).replace(tzinfo=timezone.utc)
    return {
        "mode": "week",
        "year": year,
        "week": week,
        "start": start,
        "end": end,
        "last_day_ms": int(sunday_dt.timestamp() * 1000),
        "label": f"{year}年W{week:02d}周",
        "range_label": f"{fmt_date(start_dt)} ～ {fmt_date(end_dt)}",
        "match_tokens": [
            f"{year}-W{week:02d}",
            f"{year}W{week:02d}",
            f"{year}-{week:02d}",
            start_dt.strftime("%Y-%m-%d"),
            end_dt.strftime("%Y-%m-%d"),
        ],
    }


def get_period_text(mode: str) -> dict:
    if mode == "week":
        return {
            "report_title": "周度报告",
            "supplement_title": "本周补充报告",
            "current_desc": "本周截至当前时间",
            "partial_desc": "本周部分数据",
            "full_desc": "周末完整数据",
            "steady_text": "连续两周",
            "comparison_desc": "上上周",
            "period_compare_label": "周度环比",
        }
    return {
        "report_title": "月度报告",
        "supplement_title": "月度补充报告",
        "current_desc": "当月截至今日",
        "partial_desc": "当月部分数据",
        "full_desc": "月末完整数据",
        "steady_text": "连续两月",
        "comparison_desc": "上上自然月",
        "period_compare_label": "月度环比",
    }


def get_periods(mode: str = "month"):
    """根据周期模式自动推算 prev / last / curr 三个统计窗口。"""
    today = datetime.now(timezone.utc)
    texts = get_period_text(mode)

    if mode == "week":
        current_iso = today.isocalendar()
        current_week_start = datetime.fromisocalendar(current_iso.year, current_iso.week, 1).replace(tzinfo=timezone.utc)

        last_anchor = current_week_start - timedelta(days=1)
        prev_anchor = current_week_start - timedelta(days=8)

        last_iso = last_anchor.isocalendar()
        prev_iso = prev_anchor.isocalendar()

        prev_start, prev_end = week_range_ms(prev_iso.year, prev_iso.week)
        last_start, last_end = week_range_ms(last_iso.year, last_iso.week)

        curr_start = int(current_week_start.timestamp() * 1000)
        curr_end = int(today.timestamp() * 1000)
        curr_period = {
            "mode": "week",
            "year": current_iso.year,
            "week": current_iso.week,
            "start": curr_start,
            "end": curr_end,
            "label": f"{current_iso.year}年W{current_iso.week:02d}周",
            "range_label": f"{fmt_date(current_week_start)} ～ {fmt_date(today)}",
            "match_tokens": [
                f"{current_iso.year}-W{current_iso.week:02d}",
                f"{current_iso.year}W{current_iso.week:02d}",
                current_week_start.strftime("%Y-%m-%d"),
                today.strftime("%Y-%m-%d"),
            ],
            "cutoff_label": fmt_date(today),
        }

        return {
            "mode": mode,
            "texts": texts,
            "prev": build_week_period(prev_iso.year, prev_iso.week, prev_start, prev_end),
            "last": build_week_period(last_iso.year, last_iso.week, last_start, last_end),
            "curr": curr_period,
            "report_id": f"{last_iso.year}W{last_iso.week:02d}",
            "report_label": f"{last_iso.year}年W{last_iso.week:02d}周",
            "gen_date": today.strftime("%Y-%m-%d"),
        }

    def prev_month(y, m):
        return (y, m - 1) if m > 1 else (y - 1, 12)

    last_y, last_m = prev_month(today.year, today.month)
    prev_y, prev_m = prev_month(last_y, last_m)

    prev_start, prev_end = month_range_ms(prev_y, prev_m)
    last_start, last_end = month_range_ms(last_y, last_m)
    curr_start = int(datetime(today.year, today.month, 1, tzinfo=timezone.utc).timestamp() * 1000)
    curr_end = int(today.timestamp() * 1000)

    return {
        "mode": mode,
        "texts": texts,
        "prev": build_month_period(prev_y, prev_m, prev_start, prev_end),
        "last": build_month_period(last_y, last_m, last_start, last_end),
        "curr": {
            "mode": "month",
            "year": today.year, "month": today.month, "day": today.day,
            "start": curr_start, "end": curr_end,
            "label": f"{today.month}月",
            "range_label": f"{today.year}年{today.month}月1日 ～ {today.year}年{today.month}月{today.day}日",
            "match_prefix": f"{today.year}-{today.month:02d}",
            "cutoff_label": fmt_date(today),
        },
        "report_id": f"{today.year}{today.month:02d}",
        "gen_date": today.strftime("%Y-%m-%d"),
        "report_label": f"{today.year}年{today.month}月",
    }


# ─── API 查询 ──────────────────────────────────────────────────────────────────

async def api_get(client: httpx.AsyncClient, path: str, params: dict) -> dict:
    try:
        r = await client.get(f"{BASE_URL}{path}", params=params, timeout=20)
        return r.json()
    except Exception as e:
        return {"code": -1, "error": str(e), "data": None}


def matches_period(item: dict, period: dict) -> bool:
    if not isinstance(item, dict) or not period:
        return False

    if period.get("mode") == "month":
        prefix = period.get("match_prefix")
        if not prefix:
            return False
        for key in ("month_date", "date", "period", "stat_date", "start_date"):
            if str(item.get(key, "")).startswith(prefix):
                return True
        return False

    if period.get("mode") == "week":
        item_year = item.get("year")
        item_week = item.get("week")
        if item_year is not None and item_week is not None:
            try:
                if int(item_year) == int(period["year"]) and int(item_week) == int(period["week"]):
                    return True
            except (TypeError, ValueError):
                pass

        tokens = period.get("match_tokens", [])
        for key in ("week_date", "date", "period", "stat_date", "start_date", "range"):
            value = str(item.get(key, ""))
            if any(token in value for token in tokens):
                return True
        return False

    return False


def extract_first(resp: dict, period: dict = None):
    """从 API 响应中提取 data 列表的第一个匹配条目。"""
    data = resp.get("data") if isinstance(resp, dict) else None
    if not data:
        return None
    if isinstance(data, list):
        if period:
            for item in data:
                if matches_period(item, period):
                    return item
        return data[0] if data else None
    return data


async def fetch_all_metrics(community: str, periods: dict) -> dict:
    """为单个社区并发拉取所有指标数据。"""
    prev = periods["prev"]
    last = periods["last"]
    curr = periods["curr"]
    interval = periods["mode"]

    async with httpx.AsyncClient(timeout=30) as client:
        async def G(path, params):
            return await api_get(client, path, params)

        # 并发请求所有 API
        tasks = {
            # 贡献活跃度
            "contribute_prev": G("/stats/contribute", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "contribute_last": G("/stats/contribute", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "contribute_curr": G("/stats/contribute", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
            # 有效 Review
            "comment_prev": G("/stats/valid/comment", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "comment_last": G("/stats/valid/comment", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "comment_curr": G("/stats/valid/comment", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
            # 领域适配引用度
            "integration": G("/stats/itegration", {"community": community}),
            # TOP 开发者留存率
            "retention_prev": G("/stats/user/retention", {"community": community, "date": prev["last_day_ms"]}),
            "retention_last": G("/stats/user/retention", {"community": community, "date": last["last_day_ms"]}),
            "retention_curr": G("/stats/user/retention", {"community": community, "date": curr["end"]}),
            # 年度累计下载量
            "download_prev": G("/stats/year/download", {"community": community, "date": prev["last_day_ms"]}),
            "download_last": G("/stats/year/download", {"community": community, "date": last["last_day_ms"]}),
            "download_curr": G("/stats/year/download", {"community": community, "date": curr["end"]}),
            # Issue 响应效率
            "issue_prev": G("/stats/issue", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "issue_last": G("/stats/issue", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "issue_curr": G("/stats/issue", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
            # 论坛响应效率
            "forum_prev": G("/stats/forum", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "forum_last": G("/stats/forum", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "forum_curr": G("/stats/forum", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
            # 版本发布偏差
            "version_prev": G("/stats/health/metric", {"community": community, "metric": "version_release", "date": prev["last_day_ms"]}),
            "version_last": G("/stats/health/metric", {"community": community, "metric": "version_release", "date": last["last_day_ms"]}),
            # 组织多样性
            "company_prev": G("/stats/company", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "company_last": G("/stats/company", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "company_curr": G("/stats/company", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
            # 搜索指数
            "influence_prev": G("/stats/influence", {"community": community, "interval": interval, "start": prev["start"], "end": prev["end"]}),
            "influence_last": G("/stats/influence", {"community": community, "interval": interval, "start": last["start"], "end": last["end"]}),
            "influence_curr": G("/stats/influence", {"community": community, "interval": interval, "start": curr["start"], "end": curr["end"]}),
        }
        results = {}
        for key, coro in tasks.items():
            results[key] = await coro

    # ── 提取关键字段 ──────────────────────────────────────────────
    def get_contribute(resp, period):
        item = extract_first(resp, period)
        if not item:
            return None
        return {
            "activate": item.get("activate_user"),
            "merged_prs": item.get("merged_prs"),
            "issues": item.get("issues"),
        }

    def get_comment(resp, period):
        if not resp or resp.get("code") != 1:
            return None
        item = extract_first(resp, period)
        if not item:
            return None
        return {
            "comments": item.get("comments"),
            "avg_comments": item.get("avg_comments"),
        }

    def get_issue(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data:
            return None
        item = data[0] if isinstance(data, list) and data else data if isinstance(data, dict) else None
        if not item:
            return None
        return {
            "count": item.get("count"),
            "avg_first_reply": item.get("avg_first_reply_time"),
            "median_first_reply": item.get("median_first_reply_time"),
            "avg_closed": item.get("avg_closed_time"),
            "median_closed": item.get("median_closed_time"),
        }

    def get_forum(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data:
            return None
        item = data[0] if isinstance(data, list) and data else data if isinstance(data, dict) else None
        if not item:
            return None
        return {
            "count": item.get("count"),
            "avg_first_reply": item.get("avg_first_reply_time"),
            "median_first_reply": item.get("median_first_reply_time"),
            "avg_closed": item.get("avg_closed_time"),
            "median_closed": item.get("median_closed_time"),
        }

    def get_company(resp, period):
        if not resp or resp.get("code") != 1:
            return None
        item = extract_first(resp, period)
        return item.get("count") if item else None

    def get_influence(resp, period):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data or not isinstance(data, list):
            return None
        item = extract_first(resp, period)
        return item.get("avg_index") if item else None

    def get_download(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data:
            return None
        if isinstance(data, dict):
            return data.get("download")
        return None

    def get_retention(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data:
            return None
        if isinstance(data, dict):
            return data.get("ratio")
        return None

    def get_version(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if not data:
            return None
        if isinstance(data, dict):
            return data.get("avg")
        return None

    def get_integration(resp):
        if not resp or resp.get("code") != 1:
            return None
        data = resp.get("data")
        if isinstance(data, dict):
            return data.get("count")
        return None

    return {
        "community": community,
        "prev": {
            "contribute": get_contribute(results["contribute_prev"], prev),
            "comment": get_comment(results["comment_prev"], prev),
            "retention": get_retention(results["retention_prev"]),
            "download": get_download(results["download_prev"]),
            "issue": get_issue(results["issue_prev"]),
            "forum": get_forum(results["forum_prev"]),
            "version": get_version(results["version_prev"]),
            "companies": get_company(results["company_prev"], prev),
            "influence": get_influence(results["influence_prev"], prev),
        },
        "last": {
            "contribute": get_contribute(results["contribute_last"], last),
            "comment": get_comment(results["comment_last"], last),
            "retention": get_retention(results["retention_last"]),
            "download": get_download(results["download_last"]),
            "issue": get_issue(results["issue_last"]),
            "forum": get_forum(results["forum_last"]),
            "version": get_version(results["version_last"]),
            "companies": get_company(results["company_last"], last),
            "influence": get_influence(results["influence_last"], last),
        },
        "curr": {
            "contribute": get_contribute(results["contribute_curr"], curr),
            "comment": get_comment(results["comment_curr"], curr),
            "retention": get_retention(results["retention_curr"]),
            "download": get_download(results["download_curr"]),
            "issue": get_issue(results["issue_curr"]),
            "forum": get_forum(results["forum_curr"]),
            "companies": get_company(results["company_curr"], curr),
            "influence": get_influence(results["influence_curr"], curr),
        },
        "integration": get_integration(results["integration"]),
    }


# ─── 格式化工具 ────────────────────────────────────────────────────────────────

def pct(new, old) -> str:
    if old is None or old == 0 or new is None:
        return "N/A"
    change = (new - old) / abs(old) * 100
    if abs(change) < 0.05:
        return "— 持平"
    arrow = "▲" if change > 0 else "▼"
    sign = "+" if change > 0 else ""
    return f"{arrow} {sign}{change:.1f}%"


def pct_improve(new, old) -> str:
    """对于越小越好的指标（响应时长），给出改善/延长标注。"""
    if old is None or old == 0 or new is None:
        return "N/A"
    change = (new - old) / abs(old) * 100
    if abs(change) < 0.05:
        return "— 持平"
    if new < old:
        return f"▲ 改善 {abs(change):.1f}%"
    return f"▼ 延长 +{abs(change):.1f}%"


def fmt(val, unit="", na="—") -> str:
    if val is None:
        return na
    if isinstance(val, float):
        return f"{val:.2f}{unit}"
    return f"{val:,}{unit}"


def download_wan(val):
    """将下载量（次）转换为万次字符串。"""
    if val is None:
        return None
    return round(val / 10000, 4)


# ─── 报告生成 ──────────────────────────────────────────────────────────────────

def gen_section_contribute(d_last, d_prev, last_lbl, prev_lbl) -> list:
    c_last = d_last.get("contribute") or {}
    c_prev = d_prev.get("contribute") or {}

    act_l = c_last.get("activate")
    pr_l  = c_last.get("merged_prs")
    iss_l = c_last.get("issues")
    act_p = c_prev.get("activate")
    pr_p  = c_prev.get("merged_prs")
    iss_p = c_prev.get("issues")

    lines = [
        "## 一、贡献活跃度", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
        f"| 活跃开发者数 | **{fmt(act_l, ' 人')}** | {fmt(act_p, ' 人')} | {pct(act_l, act_p)} |",
        f"| 合入 PR 数 | **{fmt(pr_l, ' 个')}** | {fmt(pr_p, ' 个')} | {pct(pr_l, pr_p)} |",
        f"| 提交 Issue 数 | **{fmt(iss_l, ' 个')}** | {fmt(iss_p, ' 个')} | {pct(iss_l, iss_p)} |",
        "",
    ]
    return lines


def gen_section_comment(d_last, d_prev, last_lbl, prev_lbl) -> list:
    c_last = d_last.get("comment")
    c_prev = d_prev.get("comment")

    if c_last and c_prev:
        com_l = c_last.get("comments")
        avg_l = c_last.get("avg_comments")
        com_p = c_prev.get("comments")
        avg_p = c_prev.get("avg_comments")
        rows = [
            f"| 有效 Review 总数 | **{fmt(com_l, ' 条')}** | {fmt(com_p, ' 条')} | {pct(com_l, com_p)} |",
            f"| 每 PR 平均 Review 数 | **{fmt(avg_l, ' 条')}** | {fmt(avg_p, ' 条')} | {pct(avg_l, avg_p)} |",
        ]
        commentary = f"> 有效 Review 总量对比上期变化 {pct(com_l, com_p)}，每 PR 平均 Review 数变化 {pct(avg_l, avg_p)}。"
    else:
        rows = [
            "| 有效 Review 总数 | **—** | — | 暂无数据 |",
            "| 每 PR 平均 Review 数 | **—** | — | 暂无数据 |",
        ]
        commentary = "> 暂无有效 Review 统计数据，建议建立代码审查质量监控机制。"

    return [
        "## 二、代码审查质量", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
    ] + rows + ["", commentary, ""]


def gen_section_integration(integration) -> list:
    if integration is not None:
        val_row = f"| 适配 / 集成 / 引用项目总数 | **{integration} 个** | 汇总值，无按周期拆分 |"
        note = f"> 领域主流项目适配集成引用度达 {integration} 个，汇总值无按周期拆分。"
    else:
        val_row = "| 适配 / 集成 / 引用项目总数 | **—** | 暂无数据 |"
        note = "> 暂无项目集成引用度数据，建议建立相关数据采集机制。"

    return [
        "## 三、领域主流项目适配集成引用度", "",
        "| 指标 | 数值 | 说明 |",
        "|------|:----:|------|",
        val_row, "", note, "",
    ]


def gen_section_retention(d_last, d_prev, last_lbl, prev_lbl) -> list:
    ret_l = d_last.get("retention")
    ret_p = d_prev.get("retention")

    if ret_l is not None:
        rows = [f"| TOP 开发者留存率 | **{ret_l*100:.2f}%** | {f'{ret_p*100:.2f}%' if ret_p is not None else '—'} | {pct(ret_l, ret_p)} |"]
        if ret_l >= 1.0:
            note = f"> TOP 开发者留存率保持 100%，核心贡献者全员活跃，社区骨干团队凝聚力稳定。"
        else:
            note = f"> TOP 开发者留存率为 {ret_l*100:.2f}%，需关注核心贡献者活跃度。"
    else:
        rows = ["| TOP 开发者留存率 | **—** | — | 暂无数据 |"]
        note = "> 暂无 TOP 开发者留存率数据，建议建立核心贡献者活跃度追踪机制。"

    return [
        "## 四、TOP 开发者留存", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
    ] + rows + ["", note, ""]


def gen_section_download(period_mode, d_last, d_prev, d_curr, last_lbl, prev_lbl, curr_lbl, cutoff_label) -> list:
    dl_last = d_last.get("download")
    dl_prev = d_prev.get("download")
    dl_curr = d_curr.get("download")

    if dl_last is not None and dl_prev is not None:
        w_last = download_wan(dl_last)
        w_prev = download_wan(dl_prev)
        w_curr = download_wan(dl_curr) if dl_curr is not None else None

        last_period_dl = round(w_last - w_prev, 4) if w_last is not None and w_prev is not None else None

        if period_mode == "week":
            rows = [
                f"| {last_lbl}增量下载量 | **{fmt(last_period_dl, ' 万次') if last_period_dl is not None else '—'}** | {last_lbl}YTD − {prev_lbl}YTD |",
                f"| {last_lbl}末 YTD | **{fmt(w_last, ' 万次') if w_last is not None else '—'}** | 年初累计至 {last_lbl} 周末 |",
                f"| {prev_lbl}末 YTD | {fmt(w_prev, ' 万次') if w_prev is not None else '—'} | 上一对比周期累计 |",
                f"| YTD 累计环比 | {pct(w_last, w_prev)} | {last_lbl}YTD vs {prev_lbl}YTD |",
            ]
            note = f"> {last_lbl}增量下载量 = {w_last} - {w_prev} = {last_period_dl}（万次）。"
        else:
            rows = [
                f"| {last_lbl}当月下载量 | **{fmt(last_period_dl, ' 万次') if last_period_dl is not None else '—'}** | {last_lbl}YTD − {prev_lbl}YTD |",
                f"| {prev_lbl}末 YTD | {fmt(w_prev, ' 万次') if w_prev is not None else '—'} | 截至 {prev_lbl} 末累计 |",
                f"| 月度环比 | {pct(last_period_dl, w_prev) if last_period_dl is not None and w_prev is not None else 'N/A'} | {last_lbl}当月 vs {prev_lbl}末累计基线 |",
                f"| 年初累计（{last_lbl} YTD）| **{fmt(w_last, ' 万次') if w_last is not None else '—'}** | 年初至 {last_lbl} 末累计 |",
                f"| {prev_lbl} YTD（上期累计）| {fmt(w_prev, ' 万次') if w_prev is not None else '—'} | 参考对比 |",
                f"| YTD 累计环比 | {pct(w_last, w_prev)} | {last_lbl}YTD vs {prev_lbl}YTD |",
            ]
            note = f"> {last_lbl}当月下载量 = {w_last} - {w_prev} = {last_period_dl}（万次）。"
    else:
        rows = ["| 年初至今下载量 | **—** | 暂无数据 |"]
        note = "> 暂无社区下载量数据，建议完善下载量统计机制。"

    return [
        "## 五、社区下载量（YTD）", "",
        "| 指标 | 数值 | 说明 |",
        "|------|:----:|------|",
    ] + rows + ["", note, ""]


def gen_section_issue(d_last, d_prev, last_lbl, prev_lbl) -> list:
    is_l = d_last.get("issue") or {}
    is_p = d_prev.get("issue") or {}

    cnt_l = is_l.get("count")
    afr_l = is_l.get("avg_first_reply")
    mfr_l = is_l.get("median_first_reply")
    ac_l  = is_l.get("avg_closed")
    mc_l  = is_l.get("median_closed")

    cnt_p = is_p.get("count")
    afr_p = is_p.get("avg_first_reply")
    mfr_p = is_p.get("median_first_reply")
    ac_p  = is_p.get("avg_closed")
    mc_p  = is_p.get("median_closed")

    return [
        "## 六、Issue 响应与处理效率", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
        f"| 提交 Issue 数 | **{fmt(cnt_l, ' 个')}** | {fmt(cnt_p, ' 个')} | {pct(cnt_l, cnt_p)} |",
        f"| 平均首次响应时长 | **{fmt(afr_l, ' 天')}** | {fmt(afr_p, ' 天')} | {pct_improve(afr_l, afr_p)} |",
        f"| 中位首次响应时长 | **{fmt(mfr_l, ' 天')}** | {fmt(mfr_p, ' 天')} | {pct_improve(mfr_l, mfr_p)} |",
        f"| 平均关闭时长 | **{fmt(ac_l, ' 天')}** | {fmt(ac_p, ' 天')} | {pct_improve(ac_l, ac_p)} |",
        f"| 中位关闭时长 | **{fmt(mc_l, ' 天')}** | {fmt(mc_p, ' 天')} | {pct_improve(mc_l, mc_p)} |",
        "",
    ]


def gen_section_forum(d_last, d_prev, last_lbl, prev_lbl) -> list:
    f_l = d_last.get("forum") or {}
    f_p = d_prev.get("forum") or {}

    cnt_l = f_l.get("count")
    afr_l = f_l.get("avg_first_reply")
    mfr_l = f_l.get("median_first_reply")
    ac_l  = f_l.get("avg_closed")
    mc_l  = f_l.get("median_closed")

    cnt_p = f_p.get("count")
    afr_p = f_p.get("avg_first_reply")
    mfr_p = f_p.get("median_first_reply")
    ac_p  = f_p.get("avg_closed")
    mc_p  = f_p.get("median_closed")

    if cnt_l is None and cnt_p is None:
        rows = [
            "| 新增帖子数 | **—** | — | 暂无数据 |",
            "| 平均首次响应时长 | **—** | — | — |",
            "| 中位首次响应时长 | **—** | — | — |",
            "| 平均关闭时长 | **—** | — | — |",
            "| 中位关闭时长 | **—** | — | — |",
        ]
        note = "> 暂无论坛相关统计数据，建议建立论坛运营质量监控机制。"
    else:
        rows = [
            f"| 新增帖子数 | **{fmt(cnt_l, ' 个')}** | {fmt(cnt_p, ' 个')} | {pct(cnt_l, cnt_p)} |",
            f"| 平均首次响应时长 | **{fmt(afr_l, ' 天')}** | {fmt(afr_p, ' 天')} | {pct_improve(afr_l, afr_p)} |",
            f"| 中位首次响应时长 | **{fmt(mfr_l, ' 天')}** | {fmt(mfr_p, ' 天')} | {pct_improve(mfr_l, mfr_p)} |",
            f"| 平均关闭时长 | **{fmt(ac_l, ' 天')}** | {fmt(ac_p, ' 天')} | {pct_improve(ac_l, ac_p)} |",
            f"| 中位关闭时长 | **{fmt(mc_l, ' 天')}** | {fmt(mc_p, ' 天')} | {pct_improve(mc_l, mc_p)} |",
        ]
        note = ""

    return [
        "## 七、论坛响应与处理效率", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
    ] + rows + (["", note, ""] if note else [""])


def gen_section_version(d_last, d_prev, last_lbl, prev_lbl) -> list:
    v_l = d_last.get("version")
    v_p = d_prev.get("version")

    if v_l is not None:
        row = f"| 版本发布偏差 | **{v_l:.1f} 天** | {f'{v_p:.1f} 天' if v_p is not None else '—'} | {'✅ 按时发布' if v_l == 0 else f'⚠️ 偏差 {v_l:.1f} 天'} |"
        note = f"> 版本发布偏差为 {v_l:.1f} 天，{'按计划准时发布，发布纪律优秀。' if v_l == 0 else '存在一定发布延期，建议关注版本计划执行情况。'}"
    else:
        row = "| 版本发布偏差 | **—** | — | 暂无版本发布数据 |"
        note = "> 暂无版本发布偏差统计数据，建议确认版本发布计划及数据采集情况。"

    return [
        "## 八、版本稳定发布偏差", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 说明 |",
        "|------|:-----------:|:-----------:|------|",
        row, "", note, "",
    ]


def gen_section_company(period_mode, d_last, d_prev, last_lbl, prev_lbl, steady_text) -> list:
    c_l = d_last.get("companies")
    c_p = d_prev.get("companies")

    if c_l is not None:
        row = f"| 贡献组织数 | **{c_l} 个** | {fmt(c_p, ' 个')} | {pct(c_l, c_p)} |"
        if c_l == c_p:
            note = f"> 贡献组织数{steady_text}稳定在 {c_l} 个，参与组织数量保持稳定。"
        elif c_l < c_p:
            note = f"> 贡献组织数从 {c_p} 个降至 {c_l} 个（{pct(c_l, c_p)}），需关注外部组织参与活跃度变化。"
        else:
            note = f"> 贡献组织数从 {c_p} 个增至 {c_l} 个（{pct(c_l, c_p)}），组织多样性持续提升。"
        if c_l <= 3:
            note += f"\n> 当前组织多样性水平{'极低' if c_l <= 2 else '偏低'}，建议积极拓展外部合作伙伴，推动贡献主体多元化。"
    else:
        row = "| 贡献组织数 | **—** | — | 暂无数据 |"
        note = "> 暂无贡献组织数据。"

    return [
        "## 九、社区组织多样性", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
        row, "", note, "",
    ]


def gen_section_influence(d_last, d_prev, last_lbl, prev_lbl) -> list:
    inf_l = d_last.get("influence")
    inf_p = d_prev.get("influence")

    if inf_l is not None:
        row = f"| 平均搜索指数 | **{inf_l}** | {fmt(inf_p)} | {pct(inf_l, inf_p)} |"
        note = f"> 主流平台平均搜索指数 {inf_l}，环比 {pct(inf_l, inf_p)}。"
    else:
        row = "| 平均搜索指数 | **—** | — | 暂无数据 |"
        note = "> 暂无主流平台搜索指数数据，建议建立搜索指数监控机制，跟踪社区在主流平台的搜索热度趋势。"

    return [
        "## 十、主流平台搜索指数", "",
        f"| 指标 | {last_lbl}（当期） | {prev_lbl}（上期） | 环比 |",
        "|------|:-----------:|:-----------:|:----:|",
        row, "", note, "",
    ]


def gen_summary(period_mode, community, d_last, d_prev, last_lbl, prev_lbl) -> list:
    """生成综合分析章节。"""
    c_last = d_last.get("contribute") or {}
    c_prev = d_prev.get("contribute") or {}
    is_last = d_last.get("issue") or {}
    is_prev = d_prev.get("issue") or {}

    positives = []
    concerns = []

    # Issue efficiency
    afr_l = is_last.get("avg_first_reply")
    afr_p = is_prev.get("avg_first_reply")
    ac_l = is_last.get("avg_closed")
    ac_p = is_prev.get("avg_closed")
    if afr_l is not None and afr_p is not None and afr_l < afr_p:
        v = abs((afr_l - afr_p) / afr_p * 100)
        positives.append(f"- **Issue 响应效率提升**：平均首次响应从 {afr_p:.2f} 天降至 {afr_l:.2f} 天（改善 {v:.1f}%），Issue 服务质量改善。")
    elif afr_l is not None and afr_p is not None and afr_l > afr_p:
        v = abs((afr_l - afr_p) / afr_p * 100)
        concerns.append(f"- **Issue 响应时长延长**：平均首次响应从 {afr_p:.2f} 天延长至 {afr_l:.2f} 天（+{v:.1f}%），需加强 Issue 运营资源投入。")

    # Contribution drop
    act_l = c_last.get("activate")
    act_p = c_prev.get("activate")
    pr_l = c_last.get("merged_prs")
    pr_p = c_prev.get("merged_prs")
    if act_l is not None and act_p is not None and act_l < act_p:
        v = abs((act_l - act_p) / act_p * 100)
        concerns.append(f"- **贡献活跃度回落**：活跃开发者减少 {v:.1f}%（{act_p}→{act_l}），需关注后续恢复情况。")

    # Retention
    ret_l = d_last.get("retention")
    if ret_l is not None and ret_l >= 1.0:
        positives.append("- **TOP 开发者留存率 100%**：核心贡献者全员活跃，骨干团队高度稳定。")

    # Version
    v_l = d_last.get("version")
    if v_l is not None and v_l == 0:
        positives.append("- **版本按时发布**：版本发布偏差为 0.0 天，发布纪律优秀。")
    elif v_l is not None and v_l > 0:
        concerns.append(f"- **版本发布存在偏差**：偏差 {v_l:.1f} 天，需关注版本计划执行情况。")

    # Median first reply worsened
    mfr_l = is_last.get("median_first_reply")
    mfr_p = is_prev.get("median_first_reply")
    if mfr_l is not None and mfr_p is not None and mfr_l > mfr_p and (afr_l is None or afr_l < afr_p):
        v = abs((mfr_l - mfr_p) / mfr_p * 100)
        concerns.append(f"- **Issue 中位首次响应时长延长**：从 {mfr_p:.2f} 天延长至 {mfr_l:.2f} 天（+{v:.1f}%），反映部分 Issue 响应滞后。")

    # Company
    comp_l = d_last.get("companies")
    if comp_l is not None and comp_l <= 2:
        concerns.append(f"- **组织多样性极低**：贡献组织仅 {comp_l} 个，需积极开拓外部合作。")
    elif comp_l is not None and comp_l <= 3:
        concerns.append(f"- **组织多样性偏低**：贡献组织仅 {comp_l} 个，建议积极拓展外部合作伙伴。")

    if not positives:
        positives = ["- 暂无明显正向趋势，需持续观察各项指标恢复情况。"]
    concerns.append("- **多项指标如暂无数据**：建议完善 Review 数、留存率、下载量等关键指标的数据采集机制。")

    return [
        "## 综合分析", "",
        "### 正向趋势",
    ] + positives + [
        "", "### 需要关注",
    ] + concerns + [""]


def gen_report(community_name: str, metrics: dict, periods: dict) -> str:
    """生成单个社区的完整 Markdown 报告（主报告 + 补充报告）。"""
    d_last = metrics["last"]
    d_prev = metrics["prev"]
    d_curr = metrics["curr"]
    integration = metrics.get("integration")

    last = periods["last"]
    prev = periods["prev"]
    curr = periods["curr"]
    texts = periods["texts"]
    period_mode = periods["mode"]

    last_lbl = last["label"]
    prev_lbl = prev["label"]
    curr_lbl = curr["label"]
    cutoff_label = curr["cutoff_label"]
    report_label = periods["report_label"]
    gen_date = periods["gen_date"]

    lines = []
    def S(*sections):
        for s in sections:
            lines.extend(s)
            lines.append("---")
            lines.append("")

    # ── 主报告标题 ──
    lines += [
        f"# {community_name} 社区运营质量{texts['report_title']} — {report_label}",
        "",
        f"> 统计周期：{last['range_label']}",
        f"> 环比对象：{prev['range_label']}",
        f"> 生成日期：{gen_date}",
        "",
        "---",
        "",
    ]

    # ── 十个章节 ──
    S(
        gen_section_contribute(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_comment(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_integration(integration),
        gen_section_retention(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_download(period_mode, d_last, d_prev, d_curr, last_lbl, prev_lbl, curr_lbl, cutoff_label),
        gen_section_issue(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_forum(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_version(d_last, d_prev, last_lbl, prev_lbl),
        gen_section_company(period_mode, d_last, d_prev, last_lbl, prev_lbl, texts["steady_text"]),
        gen_section_influence(d_last, d_prev, last_lbl, prev_lbl),
        gen_summary(period_mode, community_name, d_last, d_prev, last_lbl, prev_lbl),
    )

    # ── 补充报告：当月环比 ──
    lines += [
        "",
        f"# {community_name} 社区运营质量{texts['supplement_title']} — {curr_lbl}数据环比",
        "",
        f"> 统计周期：{curr['range_label']}（{texts['partial_desc']}）",
        f"> 环比对象：{last['range_label']}",
        f"> 生成日期：{gen_date}",
        "",
        "---",
        "",
    ]

    # 当月各章节（简化版，只显示有数据的部分）
    def curr_section_contribute():
        c_curr = d_curr.get("contribute") or {}
        c_last = d_last.get("contribute") or {}
        return [
            "## 一、贡献活跃度", "",
            f"| 指标 | {curr_lbl}（当期） | {last_lbl}（上期） | 环比 |",
            "|------|:-----------:|:-----------:|:----:|",
            f"| 活跃开发者数 | **{fmt(c_curr.get('activate'), ' 人')}** | {fmt(c_last.get('activate'), ' 人')} | {pct(c_curr.get('activate'), c_last.get('activate'))} |",
            f"| 合入 PR 数 | **{fmt(c_curr.get('merged_prs'), ' 个')}** | {fmt(c_last.get('merged_prs'), ' 个')} | {pct(c_curr.get('merged_prs'), c_last.get('merged_prs'))} |",
            f"| 提交 Issue 数 | **{fmt(c_curr.get('issues'), ' 个')}** | {fmt(c_last.get('issues'), ' 个')} | {pct(c_curr.get('issues'), c_last.get('issues'))} |",
            "",
        ]

    def curr_section_issue():
        is_curr = d_curr.get("issue") or {}
        is_last = d_last.get("issue") or {}
        return [
            "## 六、Issue 响应与处理效率", "",
            f"| 指标 | {curr_lbl}（当期） | {last_lbl}（上期） | 环比 |",
            "|------|:-----------:|:-----------:|:----:|",
            f"| 提交 Issue 数 | **{fmt(is_curr.get('count'), ' 个')}** | {fmt(is_last.get('count'), ' 个')} | {pct(is_curr.get('count'), is_last.get('count'))} |",
            f"| 平均首次响应时长 | **{fmt(is_curr.get('avg_first_reply'), ' 天')}** | {fmt(is_last.get('avg_first_reply'), ' 天')} | {pct_improve(is_curr.get('avg_first_reply'), is_last.get('avg_first_reply'))} |",
            f"| 中位首次响应时长 | **{fmt(is_curr.get('median_first_reply'), ' 天')}** | {fmt(is_last.get('median_first_reply'), ' 天')} | {pct_improve(is_curr.get('median_first_reply'), is_last.get('median_first_reply'))} |",
            f"| 平均关闭时长 | **{fmt(is_curr.get('avg_closed'), ' 天')}** | {fmt(is_last.get('avg_closed'), ' 天')} | {pct_improve(is_curr.get('avg_closed'), is_last.get('avg_closed'))} |",
            f"| 中位关闭时长 | **{fmt(is_curr.get('median_closed'), ' 天')}** | {fmt(is_last.get('median_closed'), ' 天')} | {pct_improve(is_curr.get('median_closed'), is_last.get('median_closed'))} |",
            "",
        ]

    # 当月补充报告章节
    for section_fn, section_data in [
        (curr_section_contribute, None),
        (lambda: gen_section_comment(d_curr, d_last, curr_lbl, last_lbl), None),
        (lambda: gen_section_integration(integration), None),
        (lambda: gen_section_retention(d_curr, d_last, curr_lbl, last_lbl), None),
        (lambda: [
            "## 五、社区下载量（YTD）", "",
            "| 指标 | 数值 | 说明 |",
            "|------|:----:|------|",
        ] + (
            [f"| 年初累计（{curr_lbl} YTD，截至 {cutoff_label}）| **{fmt(download_wan(d_curr.get('download')), ' 万次') if d_curr.get('download') is not None else '—'}** | 年初至当前统计截止时点累计 |",
             f"| {last_lbl} YTD（上期累计）| {fmt(download_wan(d_last.get('download')), ' 万次') if d_last.get('download') is not None else '—'} | 参考对比 |",
             f"| YTD 累计环比 | {pct(d_curr.get('download'), d_last.get('download'))} | {curr_lbl}YTD vs {last_lbl}YTD |"]
            if d_curr.get("download") is not None else
            [f"| 年初至今下载量（截至 {cutoff_label}）| **—** | 暂无数据 |"]
        ) + [""], None),
        (curr_section_issue, None),
        (lambda: gen_section_forum(d_curr, d_last, curr_lbl, last_lbl), None),
        (lambda: [
            "## 八、版本稳定发布偏差", "",
            f"| 指标 | {curr_lbl}（当期） | {last_lbl}（上期） | 说明 |",
            "|------|:-----------:|:-----------:|------|",
            "| 版本发布偏差 | **—** | — | 当月数据待统计 |",
            "",
        ], None),
        (lambda: gen_section_company(period_mode, d_curr, d_last, curr_lbl, last_lbl, texts["steady_text"]), None),
        (lambda: gen_section_influence(d_curr, d_last, curr_lbl, last_lbl), None),
    ]:
        lines.extend(section_fn())
        lines.append("---")
        lines.append("")

    # 当月综合分析
    c_curr = d_curr.get("contribute") or {}
    c_last_c = d_last.get("contribute") or {}
    is_curr = d_curr.get("issue") or {}
    is_last_i = d_last.get("issue") or {}

    lines += ["## 综合分析（{curr_lbl} vs {last_lbl}）".format(curr_lbl=curr_lbl, last_lbl=last_lbl), ""]
    lines += ["### 正向趋势"]

    m_pos = []
    if c_curr.get("activate") is not None and c_last_c.get("activate") is not None and c_curr["activate"] > c_last_c["activate"]:
        m_pos.append(f"- **活跃开发者数** 回升 {pct(c_curr['activate'], c_last_c['activate'])}（{c_last_c['activate']}→{c_curr['activate']}），节后活跃度持续恢复。")
    if c_curr.get("merged_prs") is not None and c_last_c.get("merged_prs") is not None and c_curr["merged_prs"] > c_last_c["merged_prs"]:
        m_pos.append(f"- **合入 PR 数** 回升 {pct(c_curr['merged_prs'], c_last_c['merged_prs'])}（{c_last_c['merged_prs']}→{c_curr['merged_prs']}），节后贡献动能持续恢复。")
    if is_curr.get("avg_first_reply") is not None and is_last_i.get("avg_first_reply") is not None and is_curr["avg_first_reply"] < is_last_i["avg_first_reply"]:
        v = abs((is_curr["avg_first_reply"] - is_last_i["avg_first_reply"]) / is_last_i["avg_first_reply"] * 100)
        m_pos.append(f"- **Issue 平均响应时长** 改善 -{v:.1f}%（{is_last_i['avg_first_reply']:.2f}→{is_curr['avg_first_reply']:.2f} 天），响应处理效率持续提升。")
    if is_curr.get("avg_closed") is not None and is_last_i.get("avg_closed") is not None and is_curr["avg_closed"] < is_last_i["avg_closed"]:
        v = abs((is_curr["avg_closed"] - is_last_i["avg_closed"]) / is_last_i["avg_closed"] * 100)
        m_pos.append(f"- **Issue 平均关闭时长** 改善 -{v:.1f}%（{is_last_i['avg_closed']:.2f}→{is_curr['avg_closed']:.2f} 天），处理效率显著提升。")

    if not m_pos:
        m_pos = [f"- 当前截至 {cutoff_label} 的数据仍需结合后续完整周期数据继续观察。"]
    lines.extend(m_pos)

    lines += ["", "### 需要关注"]
    m_neg = []
    if c_curr.get("activate") is not None and c_last_c.get("activate") is not None and c_curr["activate"] < c_last_c["activate"]:
        m_neg.append(f"- **活跃开发者数** 未回升（{c_last_c['activate']}→{c_curr['activate']}），需关注节后恢复进度。")
    if c_curr.get("merged_prs") is not None and c_last_c.get("merged_prs") is not None and c_curr["merged_prs"] < c_last_c["merged_prs"]:
        m_neg.append(f"- **合入 PR 数** 未回升（{c_last_c['merged_prs']}→{c_curr['merged_prs']}），需关注贡献活跃度的持续恢复。")
    if is_curr.get("avg_first_reply") is not None and is_last_i.get("avg_first_reply") is not None and is_curr["avg_first_reply"] > is_last_i["avg_first_reply"]:
        v = abs((is_curr["avg_first_reply"] - is_last_i["avg_first_reply"]) / is_last_i["avg_first_reply"] * 100)
        m_neg.append(f"- **Issue 平均响应时长** 延长 +{v:.1f}%（{is_last_i['avg_first_reply']:.2f}→{is_curr['avg_first_reply']:.2f} 天），需关注 Issue 积压情况。")

    if not m_neg:
        m_neg = [f"- 当前截至 {cutoff_label} 的数据整体表现平稳，后续完整周期数据将更准确反映趋势。"]
    lines.extend(m_neg)

    lines += [
        "",
        f"> **注**：{curr_lbl}数据统计周期为 {curr['range_label']}，为{texts['partial_desc']}，",
        f"> {texts['full_desc']}将在下期报告中体现，环比结论仅供参考。",
        "",
        "---",
        "",
        "*数据来源：datastat.osinfra.cn | 报告由 Claude Code 自动生成*",
    ]

    return "\n".join(lines)


# ─── 主程序 ────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="生成社区运营质量周报或月报")
    parser.add_argument("--period", choices=["month", "week"], default="month", help="统计周期，默认 month")
    parser.add_argument("communities", nargs="+", help="社区名称，支持空格或逗号分隔")
    parsed = parser.parse_args()

    # 解析社区名列表（支持逗号分隔或空格分隔）
    communities = []
    for arg in parsed.communities:
        for c in arg.replace(",", " ").split():
            c = c.strip().lower()
            if c:
                communities.append(c)

    if not communities:
        print("错误：未提供有效的社区名称", file=sys.stderr)
        sys.exit(1)

    periods = get_periods(parsed.period)
    report_id = periods["report_id"]

    print(f"统计模式：{parsed.period}", file=sys.stderr)
    print(f"报告周期：{periods['last']['range_label']}", file=sys.stderr)
    print(f"对比周期：{periods['prev']['range_label']}", file=sys.stderr)
    print(f"补充周期：{periods['curr']['range_label']}", file=sys.stderr)
    print(f"处理社区：{', '.join(communities)}", file=sys.stderr)
    print("", file=sys.stderr)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    generated = []
    failed = []

    for community in communities:
        print(f"  [{community}] 拉取数据...", file=sys.stderr)
        try:
            metrics = await fetch_all_metrics(community, periods)

            # 生成报告内容
            # 使用首字母大写作为显示名，特殊处理已知社区
            display_names = {
                "openeuler": "openEuler", "opengauss": "openGauss", "openubmc": "openUBMC",
                "mindspore": "MindSpore", "mindie": "MindIE", "mindstudio": "MindStudio",
                "mindspeed": "MindSpeed", "mindcluster": "MindCluster", "mindseriessdk": "MindSDK",
                "cann": "CANN", "cannopen": "CANNopen", "vllm": "vLLM",
                "triton": "Triton", "tilelang": "TileLang", "pta": "PTA",
                "pytorch": "PyTorch", "sgl": "SGL", "verl": "verl",
                "ascendnpuir": "AscendNPUIR", "boostkit": "BoostKit",
                "unifiedbus": "UnifiedBus", "openfuyao": "openFuyao",
            }
            display_name = display_names.get(community, community.title())

            content = gen_report(display_name, metrics, periods)

            # 保存文件
            if parsed.period == "week":
                filename = f"{community}_community_quality_weekly_{report_id}.md"
            else:
                filename = f"{community}_community_quality_monthly_{report_id}.md"
            filepath = os.path.join(REPORTS_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  [{community}] ✅ 已生成: reports/{filename}", file=sys.stderr)
            generated.append(filepath)

        except Exception as e:
            print(f"  [{community}] ❌ 失败: {e}", file=sys.stderr)
            failed.append((community, str(e)))

    print("", file=sys.stderr)
    print(f"完成：成功 {len(generated)} 个，失败 {len(failed)} 个", file=sys.stderr)

    # 向 stdout 输出结果摘要（供 Claude 读取）
    result = {
        "period": parsed.period,
        "generated": generated,
        "failed": [{"community": c, "error": e} for c, e in failed],
        "periods": {
            "last": periods["last"]["range_label"],
            "prev": periods["prev"]["range_label"],
            "curr": periods["curr"]["range_label"],
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
