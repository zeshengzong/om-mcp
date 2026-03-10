# OM-MCP 项目开发规范

## 项目概述

本项目是基于 FastMCP 框架的 MCP (Model Context Protocol) 服务，用于查询开源社区的各类指标数据。

## 技术栈

- **语言**: Python 3.x
- **框架**: FastMCP (`mcp.server.fastmcp`)
- **HTTP 客户端**: httpx (异步)
- **Base URL**: `https://datastat.osinfra.cn/server`

## 项目结构

```
om-mcp/
├── server.py              # 入口文件，注册所有工具模块
├── lib/
│   └── http.py           # HTTP 请求封装
├── tools/
│   ├── health.py         # 社区健康度
│   ├── common.py         # list_communities
│   ├── server_apis.py    # get_community_list, get_metric_dict
│   ├── query_apis.py     # get_issues_aggregate, get_prs_aggregate
│   ├── cla_apis.py       # 空文件（接口已废弃）
│   ├── project_apis.py   # 空文件（接口已废弃）
│   └── general_apis.py   # 通用查询 API（8个有效接口）
├── test/
│   └── api_test_results.md   # 接口测试结果
├── API_LIST.md           # 接口列表文档（13个有效接口）
└── CLAUDE.md             # 本文件
```

## 代码文件逻辑说明

### server.py
入口文件。导入并注册所有 tool 模块：
```python
import tools.health as health        # → health.register(mcp)
import tools.common as common        # → common.register(mcp)
import tools.server_apis as server_apis  # → server_apis.register(mcp)
import tools.query_apis as query_apis    # → query_apis.register(mcp)
import tools.project_apis as project_apis  # → project_apis.register(mcp)
import tools.general_apis as general_apis  # → general_apis.register(mcp)
```
注意：`cla_apis.py` 未在 server.py 中注册。

### lib/http.py
HTTP 请求封装，提供三个核心函数：
- `get(path, params)` — 异步 GET 请求
- `post(path, body)` — 异步 POST 请求（JSON body）
- `extract_data(result)` — 兼容单/双层嵌套的 data 提取

### tools/health.py
**接口**: `get_community_health(community, date="")`
- 查询社区健康度综合评分及各子指标
- 使用 `COMMUNITY_MAP` 做社区名称映射（支持别名）
- HTTP: POST `/community/health`

### tools/common.py
**接口**: `list_communities()`
- 返回所有支持查询的社区名称列表
- 数据来源：health.py 中的 `COMMUNITY_MAP`

### tools/server_apis.py
**接口**:
- `get_community_list()` — POST `/community/list`，返回所有社区列表
- `get_metric_dict()` — GET `/dict/metric`，返回指标字典（120+ 条）

### tools/query_apis.py
**接口**:
- `get_issues_aggregate(community, start_time, end_time, interval)` — POST `/query/issues/agg`
- `get_prs_aggregate(community, start_time, end_time, interval)` — POST `/query/prs/agg`
- 时间参数使用毫秒时间戳，内部用 `_date_to_ms()` 转换

### tools/general_apis.py
含 3 个辅助函数（不暴露为工具）：
- `_date_to_ms(date_str)` — YYYY-MM-DD → 毫秒时间戳
- `_build_time_body(start_date, end_date)` — 构建含时间戳的 body dict
- `_fmt_page(data, item_formatter, label)` — 通用分页格式化

**8个 MCP 接口**:

| 接口 | HTTP 路径 |
|------|-----------|
| `get_forum_detail` | POST `/query/forum/detail/page` |
| `get_issues_agg_page` | POST `/query/issues/agg` |
| `get_issues_detail` | POST `/query/issues/detail` |
| `get_issue_ref_pr` | POST `/query/issue/ref/pr` |
| `get_prs_agg_page` | POST `/query/prs/agg` |
| `get_prs_detail` | POST `/query/prs/detail` |
| `get_contributes_topn` | POST `/query/contributes/topn/total` |
| `get_filter_options` | POST `/query/filter` |

### tools/cla_apis.py / tools/project_apis.py
均为空文件（仅含 `def register(mcp): pass`），原有接口均已废弃。

## 当前有效接口（13个）

| 接口 | 所在文件 |
|------|---------|
| `get_community_health` | tools/health.py |
| `list_communities` | tools/common.py |
| `get_community_list` | tools/server_apis.py |
| `get_metric_dict` | tools/server_apis.py |
| `get_issues_aggregate` | tools/query_apis.py |
| `get_prs_aggregate` | tools/query_apis.py |
| `get_forum_detail` | tools/general_apis.py |
| `get_issues_agg_page` | tools/general_apis.py |
| `get_issues_detail` | tools/general_apis.py |
| `get_issue_ref_pr` | tools/general_apis.py |
| `get_prs_agg_page` | tools/general_apis.py |
| `get_prs_detail` | tools/general_apis.py |
| `get_contributes_topn` | tools/general_apis.py |
| `get_filter_options` | tools/general_apis.py |

详细参数说明见 `API_LIST.md`，测试结果见 `test/api_test_results.md`。

## 开发规范

### 添加新的 MCP 工具方法

1. 在 `tools/` 下合适的模块中添加 `@mcp.tool()` 函数
2. 如果是新模块，在 `server.py` 中注册
3. 更新 `API_LIST.md` 和 `CLAUDE.md`（本文件的接口表格）
4. 测试后记录结果到 `test/api_test_results.md`

### 代码规范

```python
from lib.http import get, post, extract_data

# GET 请求
data = await get("/api/path", {"param": "value"})

# POST 请求
data = await post("/api/path", {"param": "value"})

# 提取数据（自动处理双层嵌套）
result = extract_data(data)

# 社区名称统一小写
community = community.lower()

# 时间转毫秒（general_apis.py 内部用）
from tools.general_apis import _date_to_ms
timestamp = _date_to_ms("2026-03-10")
```

### Git 提交规范

```
<type>: <subject>
```

类型: `feat`/`fix`/`docs`/`test`/`refactor`/`style`

## 常见问题

### Q: API 返回数据格式不一致怎么办？
A: 使用 `extract_data()` 函数，它会自动处理单层和双层嵌套的 data 结构。

### Q: 如何处理可选参数？
A: 使用默认值 `""`，在函数内部用 `if param:` 判断是否传入。

## 参考资料

- [FastMCP 文档](https://github.com/jlowin/fastmcp)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [项目 API 文档](./API_LIST.md)
