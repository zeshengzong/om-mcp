from datetime import datetime
from mcp.server.fastmcp import FastMCP
from lib.http import post, extract_data


def _date_to_ms(date_str: str) -> int:
    """将 YYYY-MM-DD 字符串转换为毫秒时间戳。"""
    dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return int(dt.timestamp() * 1000)


def _build_time_body(start_date: str, end_date: str) -> dict:
    """将日期字符串转为毫秒时间戳并放入 body。未指定时默认近一年。"""
    now = datetime.utcnow()
    default_end = int(now.timestamp() * 1000)
    default_start = int(now.replace(year=now.year - 1).timestamp() * 1000)
    body = {
        "start": _date_to_ms(start_date) if start_date else default_start,
        "end": _date_to_ms(end_date) if end_date else default_end,
    }
    return body


def _fmt_page(data: dict, item_formatter, label: str) -> str:
    """通用分页结果格式化。"""
    if not isinstance(data, dict):
        return f"暂无{label}数据"
    items = data.get("list", [])
    total = data.get("total_count", len(items))
    total_page = data.get("total_page", 1)
    lines = [f"{label}（共 {total} 条，{total_page} 页）："]
    for item in items:
        lines.append(item_formatter(item))
    return "\n".join(lines)


def register(mcp: FastMCP):

    # ── 论坛 ──────────────────────────────────────────────────────────────

    @mcp.tool()
    async def get_forum_detail(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        title: str = "",
        desc: str = "created_at",
    ) -> str:
        """获取论坛帖子详情分页列表。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            title: 标题关键字（可选）
            desc: 降序字段，默认 created_at
        """
        body = _build_time_body(start_date, end_date)
        if community:
            body["community"] = community.lower()
        if title:
            body["title"] = title
        if desc:
            body["desc"] = desc

        result = await post("/query/forum/detail/page", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无论坛详情数据"

        def fmt(item):
            return (
                f"  [{item.get('created_at', 'N/A')[:10]}] "
                f"{item.get('title', 'N/A')} — "
                f"回复 {item.get('reply_count', 0)}，浏览 {item.get('view_count', 0)}"
            )

        return _fmt_page(data, fmt, "论坛帖子详情")

    # ── Issue ──────────────────────────────────────────────────────────────

    @mcp.tool()
    async def get_issues_agg_page(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        group_dim: str = "repo",
        namespace: str = "",
        repo_path: str = "",
        issue_type: str = "",
        source: str = "",
        private: str = "false",
        asc: str = "",
        desc: str = "",
    ) -> str:
        """获取 Issue 汇总分页统计，支持按仓库/SIG/命名空间等维度分组。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            group_dim: 分组维度，如 repo/sig/namespace/sub_community，默认 repo
            namespace: 命名空间筛选（可选）
            repo_path: 仓库路径筛选（可选）
            issue_type: Issue 类型筛选（可选）
            source: 来源平台（可选）
            private: 是否私仓，true/false，默认 false
            asc: 升序字段（可选），如 one_day_response_ratio
            desc: 降序字段（可选），如 open_count
        """
        body = _build_time_body(start_date, end_date)
        body.update({
            "group_dim": group_dim,
            "community": community.lower() if community else "",
            "issue_type": issue_type,
            "issue_type_list": [],
            "namespace": namespace,
            "repo_path": repo_path,
            "source": source,
            "internalList": [],
            "private": private,
            "asc": asc,
            "desc": desc,
        })

        result = await post("/query/issues/agg", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无 Issue 汇总数据"

        def fmt(item):
            return (
                f"  [{item.get('repo_path', item.get('sig_name', item.get('namespace', 'N/A')))}] "
                f"总数 {item.get('total_count', 0)}，开启 {item.get('open_count', 0)}，"
                f"关闭率 {item.get('closed_ratio', 'N/A')}，"
                f"平均响应 {item.get('avg_first_reply_time', 'N/A')} 天"
            )

        return _fmt_page(data, fmt, f"Issue 汇总（按 {group_dim} 分组）")

    @mcp.tool()
    async def get_issues_detail(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        namespace: str = "",
        repo_path: str = "",
        title: str = "",
        state: str = "",
        issue_type: str = "",
        priority: str = "",
        page_num: int = 1,
        page_size: int = 20,
    ) -> str:
        """获取 Issue 详情分页列表。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            namespace: 命名空间（可选）
            repo_path: 仓库路径（可选）
            title: 标题关键字（可选）
            state: 状态（open/closed，可选）
            issue_type: Issue 类型（可选）
            priority: 优先级（可选）
            page_num: 页码，默认 1
            page_size: 每页数量，默认 20
        """
        body = _build_time_body(start_date, end_date)
        body.update({"pageNum": page_num, "pageSize": page_size})
        if community:
            body["community"] = community.lower()
        if namespace:
            body["namespace"] = namespace
        if repo_path:
            body["repo_path"] = repo_path
        if title:
            body["title"] = title
        if state:
            body["state"] = state
        if issue_type:
            body["issue_type"] = issue_type
        if priority:
            body["priority"] = priority

        result = await post("/query/issues/detail", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无 Issue 详情数据"

        def fmt(item):
            return (
                f"  #{item.get('issue_number', 'N/A')} [{item.get('state', 'N/A')}] "
                f"{item.get('title', 'N/A')[:60]} "
                f"— {item.get('repo_path', 'N/A')} "
                f"— {item.get('created_at', 'N/A')}"
            )

        return _fmt_page(data, fmt, "Issue 详情")

    @mcp.tool()
    async def get_issue_ref_pr(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        namespace: str = "",
        repo_path: str = "",
        sig_group: str = "",
        pr_state: str = "",
        issue_state: str = "",
        pr_number: str = "",
        issue_number: str = "",
    ) -> str:
        """获取 Issue 关联 PR 信息，查看 Issue 和 PR 的关联关系。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            namespace: 命名空间（可选）
            repo_path: 仓库路径（可选）
            sig_group: SIG 组（可选）
            pr_state: PR 状态（open/merged/closed，可选）
            issue_state: Issue 状态（open/closed，可选）
            pr_number: PR 编号（可选）
            issue_number: Issue 编号（可选）
        """
        body = _build_time_body(start_date, end_date)
        if community:
            body["community"] = community.lower()
        if namespace:
            body["namespace"] = namespace
        if repo_path:
            body["repo_path"] = repo_path
        if sig_group:
            body["sig_group"] = sig_group
        if pr_state:
            body["pr_state"] = pr_state
        if issue_state:
            body["issue_state"] = issue_state
        if pr_number:
            body["pr_number"] = pr_number
        if issue_number:
            body["issue_number"] = issue_number

        result = await post("/query/issue/ref/pr", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无 Issue 关联 PR 数据"

        def fmt(item):
            return (
                f"  Issue #{item.get('issue_number', 'N/A')} [{item.get('issue_state', 'N/A')}] "
                f"← PR #{item.get('pr_number', 'N/A')} [{item.get('pr_state', 'N/A')}] "
                f"— {item.get('repo_path', 'N/A')}"
            )

        return _fmt_page(data, fmt, "Issue 关联 PR")

    # ── PR ────────────────────────────────────────────────────────────────

    @mcp.tool()
    async def get_prs_agg_page(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        group_dim: str = "repo",
        namespace: str = "",
        repo: str = "",
        pr_type: str = "",
        private: str = "",
        desc: str = "open_count",
    ) -> str:
        """获取 PR 汇总分页统计，支持按仓库/SIG/命名空间等维度分组。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            group_dim: 分组维度，如 repo/sig/namespace，默认 repo
            namespace: 命名空间筛选（可选）
            repo: 仓库名称（可选）
            pr_type: PR 类型（可选）
            private: 是否私仓，true/false（可选）
            desc: 降序字段，默认 open_count
        """
        body = _build_time_body(start_date, end_date)
        body["group_dim"] = group_dim
        if community:
            body["community"] = community.lower()
        if namespace:
            body["namespace"] = namespace
        if repo:
            body["repo"] = repo
        if pr_type:
            body["pr_type"] = pr_type
        if private:
            body["private"] = private
        if desc:
            body["desc"] = desc

        result = await post("/query/prs/agg", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无 PR 汇总数据"

        def fmt(item):
            return (
                f"  [{item.get('repo_path', item.get('sig_name', item.get('namespace', 'N/A')))}] "
                f"总数 {item.get('total_count', 0)}，开启 {item.get('open_count', 0)}，"
                f"合并率 {item.get('merged_ratio', 'N/A')}，"
                f"平均响应 {item.get('avg_first_reply_time', 'N/A')} 天"
            )

        return _fmt_page(data, fmt, f"PR 汇总（按 {group_dim} 分组）")

    @mcp.tool()
    async def get_prs_detail(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        namespace: str = "",
        repo_path: str = "",
        title: str = "",
        state: str = "",
        page_num: int = 1,
        page_size: int = 20,
    ) -> str:
        """获取 PR 详情分页列表。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            namespace: 命名空间（可选）
            repo_path: 仓库路径（可选）
            title: 标题关键字（可选）
            state: 状态（open/merged/closed，可选）
            page_num: 页码，默认 1
            page_size: 每页数量，默认 20
        """
        body = _build_time_body(start_date, end_date)
        body.update({"pageNum": page_num, "pageSize": page_size})
        if community:
            body["community"] = community.lower()
        if namespace:
            body["namespace"] = namespace
        if repo_path:
            body["repo_path"] = repo_path
        if title:
            body["title"] = title
        if state:
            body["state"] = state

        result = await post("/query/prs/detail", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无 PR 详情数据"

        def fmt(item):
            return (
                f"  #{item.get('pr_number', 'N/A')} [{item.get('state', 'N/A')}] "
                f"{item.get('title', 'N/A')[:60]} "
                f"— {item.get('repo_path', 'N/A')} "
                f"— {item.get('created_at', 'N/A')}"
            )

        return _fmt_page(data, fmt, "PR 详情")

    # ── 贡献 ───────────────────────────────────────────────────────────────

    @mcp.tool()
    async def get_contributes_topn(
        community: str = "",
        start_date: str = "",
        end_date: str = "",
        event: str = "pr",
        metric: str = "company_type",
        topn: int = 10,
        private: str = "false",
        org_list: str = "",
    ) -> str:
        """获取贡献 TopN 汇总排名，支持按组织/仓库/SIG/开发者维度统计。

        Args:
            community: 社区名称（可选）
            start_date: 开始日期，格式 YYYY-MM-DD（可选）
            end_date: 结束日期，格式 YYYY-MM-DD（可选）
            event: 贡献类型，pr/issue/comment/addcode，默认 pr
            metric: 统计维度，company_type/company/sig/repo/user，默认 company_type
            topn: TopN 数量，默认 10
            private: 是否包含私仓，true/false，默认 false
            org_list: 逗号分隔的命名空间/组织列表（可选）
        """
        body = _build_time_body(start_date, end_date)
        body.update({
            "event": event,
            "metric": metric,
            "topn": topn,
            "private": private,
        })
        if community:
            body["community"] = community.lower()
        if org_list:
            body["orgList"] = [o.strip() for o in org_list.split(",") if o.strip()]

        result = await post("/query/contributes/topn/total", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无贡献 TopN 数据"

        items = data if isinstance(data, list) else data.get("list", [])
        count_field = f"{event}_total" if event in ("pr", "issue", "comment", "addcode") else "pr_total"
        dim_field_map = {
            "company_type": "company_type",
            "company": "company",
            "sig": "sig_name",
            "repo": "repo_path",
            "user": "user_level",
        }
        dim_field = dim_field_map.get(metric, metric)

        lines = [f"贡献 Top{topn}（维度：{metric}，类型：{event}）："]
        for i, item in enumerate(items, 1):
            rank = item.get("row_num", i)
            dim_val = item.get(dim_field, "N/A")
            count = item.get(count_field, item.get("pr_total", 0))
            total = item.get("total_count", "N/A")
            lines.append(f"  {rank}. {dim_val} — {count}（全量：{total}）")

        return "\n".join(lines)

    # ── 筛选 ───────────────────────────────────────────────────────────────

    @mcp.tool()
    async def get_filter_options(community: str = "", tab: str = "") -> str:
        """获取社区数据筛选条件（如 SIG 列表、仓库列表、标签等）。

        Args:
            community: 社区名称（可选）
            tab: 标签页标识，如 issue/pr/repo 等（可选）
        """
        body = {}
        if community:
            body["community"] = community.lower()
        if tab:
            body["tab"] = tab

        result = await post("/query/filter", body)
        if result.get("code") != 1:
            return f"API 错误：{result.get('message', '未知错误')}"
        data = extract_data(result)
        if not data:
            return "暂无筛选条件数据"

        if isinstance(data, dict):
            lines = [f"筛选条件（社区：{community or '全部'}，标签页：{tab or '全部'}）："]
            for key, val in data.items():
                if isinstance(val, list):
                    lines.append(f"  {key}：{', '.join(str(v) for v in val[:10])}"
                                 + ("..." if len(val) > 10 else ""))
                else:
                    lines.append(f"  {key}：{val}")
            return "\n".join(lines)

        return f"筛选条件：{data}"
