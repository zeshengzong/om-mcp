---
description: 审查并修复 om-mcp 项目 tools/ 目录下所有 API 工具文件，统一应用已知修复模式。
agent: build
---

审查并修复 om-mcp 项目中 `tools/` 目录下所有 API 工具文件，将已知问题的修复模式统一应用。

## 需要检查和修复的问题

### 1. community 参数大小写

所有传给后端的 `community` 字段必须 `.lower()`。

**错误模式：**
```python
body["community"] = community
```

**正确模式：**
```python
body["community"] = community.lower()
```

适用范围：`tools/cla_apis.py`、`tools/general_apis.py`、`tools/query_apis.py`、`tools/server_apis.py` 中所有设置 `community` 的地方。

---

### 2. general_apis.py 中的 `_build_time_body` 默认时间范围

未传日期时，不能返回空 body，必须默认近一年时间范围（毫秒时间戳）。

**错误模式：**
```python
def _build_time_body(start_date: str, end_date: str) -> dict:
    body = {}
    if start_date:
        body["start"] = _date_to_ms(start_date)
    if end_date:
        body["end"] = _date_to_ms(end_date)
    return body
```

**正确模式：**
```python
def _build_time_body(start_date: str, end_date: str) -> dict:
    now = datetime.utcnow()
    default_end = int(now.timestamp() * 1000)
    default_start = int(now.replace(year=now.year - 1).timestamp() * 1000)
    body = {
        "start": _date_to_ms(start_date) if start_date else default_start,
        "end": _date_to_ms(end_date) if end_date else default_end,
    }
    return body
```

---

### 3. 所有聚合查询接口必须使用毫秒时间戳 + 完整 body 结构

**错误模式（旧格式，发送字符串日期或空 body）：**
```python
body = {}
if start_time:
    body["start_time"] = start_time
if end_time:
    body["end_time"] = end_time
```

**正确模式（毫秒时间戳 + 默认近一年）：**
```python
now = datetime.utcnow()
body = {
    "start": _date_to_ms(start_time) if start_time else int(now.replace(year=now.year - 1).timestamp() * 1000),
    "end": _date_to_ms(end_time) if end_time else int(now.timestamp() * 1000),
    # ... 其他必填字段
}
```

各接口的完整 body 结构如下：

#### `get_issues_aggregate` → `/query/issues/agg`
```python
body = {
    "start": ..., "end": ...,
    "group_dim": "sub_community",
    "issue_type": "", "issue_type_list": [],
    "namespace": "", "repo_path": "", "source": "",
    "internalList": [], "private": "false",
    "asc": "one_day_response_ratio", "desc": "",
}
# 响应：从 data['list'][0] 提取，字段名用 count（不是 total_count）
item = data.get('list', [{}])[0] if isinstance(data, dict) else {}
```

#### `get_prs_aggregate` → `/query/prs/agg`
```python
body = {
    "start": ..., "end": ...,
    "group_dim": "", "pr_type": "",
    "namespace": "", "repo": "",
    "private": "false", "asc": "", "desc": "",
}
# 响应：从 data['list'][0] 提取，字段名用 count（不是 total_count）
item = data.get('list', [{}])[0] if isinstance(data, dict) else {}
```

#### `get_issues_by_sig` → `/query/issues/agg/sig`
```python
body = {
    "start": ..., "end": ...,
    "group_dim": "sig",
    "issue_type": "", "issue_type_list": [],
    "namespace": "", "sig_name": "", "sig_name_list": [],
    "source": "", "internalList": [],
    "private": "false", "asc": "", "desc": "count",
}
```

#### `get_prs_by_sig` → `/query/prs/agg/sig`
```python
body = {
    "start": ..., "end": ...,
    "group_dim": "sig",
    "pr_type": "", "namespace": "", "sig_name": "",
    "private": "false", "asc": "", "desc": "",
}
```

#### `get_repo_user_list` → `/query/repo/user/page`
```python
body = {
    "start": ..., "end": ...,   # 默认近一年，无需用户传入
    "namespace": "", "repo_path": "",
    "private": "false", "asc": "", "desc": "in_user_count",
    "pageNum": page, "pageSize": page_size,
}
```

#### `/project/*` 接口（`get_project_hotspot`、`get_project_repo_list`、`get_project_active`）
```python
now = datetime.utcnow()
body = {
    "start": int(now.replace(year=now.year - 1).timestamp() * 1000),
    "end": int(now.timestamp() * 1000),
}
```

---

### 4. `get_issues_agg_page` 请求体必填字段

该接口需要完整的字段，不能仅传有值的字段。使用 `body.update()` 一次性设置所有字段。

**正确模式：**
```python
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
```

同时函数签名需要增加 `asc: str = ""` 参数，`private` 默认值改为 `"false"`。

---

### 5. 废弃端点替换

以下旧端点已不可用，需替换为新的 `/query/*` 端点：

| 旧端点 | 新端点 | 说明 |
|--------|--------|------|
| `POST /project/topn/company/pr` | `POST /query/contributes/topn/total` | `get_project_topn_company_pr` |
| `POST /project/topn/company/pr`（用于计数） | `POST /query/company/detail` | `get_company_count` |

#### `get_project_topn_company_pr` 正确实现：
```python
body = {
    "start": ..., "end": ...,
    "event": "pr", "metric": "company",
    "orgList": [], "private": "false",
    "community": community.lower() if community else "",
}
result = await post("/query/contributes/topn/total", body)
# 响应字段：item.get("company")、item.get("pr_total")
```

#### `get_company_count` 正确实现：
```python
body = {
    "start": ..., "end": ...,
    "source": "", "internal": "",
    "pageNum": 1, "pageSize": 1,
    "community": community.lower() if community else "",
}
result = await post("/query/company/detail", body)
# 从 data.get("total_count") 读取企业总数
```

---

### 6. 删除废弃工具

以下工具因接口 404 已废弃，不应存在于代码中，遇到则删除：

- `get_cla_stats`（`/cla/stats` 返回 HTTP 404）

---

## 执行步骤

1. 读取 `tools/` 目录下所有 `.py` 文件
2. 逐一检查上述六类问题
3. 对有问题的文件应用修复
4. 确认 `lib/http.py` 中 `post()` 函数是否有调试日志（如无需要可询问用户是否保留）
5. 汇报修复了哪些文件的哪些位置

$ARGUMENTS
