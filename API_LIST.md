# OM-MCP 接口列表

本文档记录所有已实现且可用的 MCP 工具接口（共 13 个）。

## 社区相关 (3个)

### get_community_health
查询指定社区的健康度指标数据。

**参数：**
- `community` (str): 社区名称，如 openEuler、MindSpore 等
- `date` (str, 可选): 查询日期，格式 YYYY-MM-DD

**返回：** 综合评分及各子指标分数

---

### list_communities
列出所有支持查询的社区名称。

**参数：** 无

**返回：** 社区名称列表（共 23 个）

---

### get_community_list
获取所有支持的开源社区列表。

**参数：** 无

**返回：** 社区详细信息列表

---

## Issue (4个)

### get_issues_aggregate
获取 Issue 聚合统计：总数、开启数、关闭数、首次响应时长、关闭时长、关闭率。

**参数：**
- `community` (str, 可选): 社区名称
- `start_time` (str, 可选): 开始时间，格式 YYYY-MM-DD
- `end_time` (str, 可选): 结束时间，格式 YYYY-MM-DD
- `interval` (str, 可选): 时间粒度，支持 day/week/month

**返回：** Issue 聚合统计数据

---

### get_issues_agg_page
获取 Issue 汇总分页统计，支持按仓库/SIG/命名空间等维度分组。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `group_dim` (str, 可选): 分组维度，如 repo/sig/namespace，默认 repo
- `namespace` (str, 可选): 命名空间筛选
- `repo_path` (str, 可选): 仓库路径筛选
- `issue_type` (str, 可选): Issue 类型筛选
- `source` (str, 可选): 来源平台
- `private` (str, 可选): 是否私仓，true/false
- `asc` (str, 可选): 升序字段
- `desc` (str, 可选): 降序字段

**返回：** Issue 汇总分页数据

---

### get_issues_detail
获取 Issue 详情分页列表。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `namespace` (str, 可选): 命名空间
- `repo_path` (str, 可选): 仓库路径
- `title` (str, 可选): 标题关键字
- `state` (str, 可选): 状态 open/closed
- `issue_type` (str, 可选): Issue 类型
- `priority` (str, 可选): 优先级
- `page_num` (int, 可选): 页码，默认 1
- `page_size` (int, 可选): 每页数量，默认 20

**返回：** Issue 详情列表

---

### get_issue_ref_pr
获取 Issue 关联 PR 信息。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `namespace` (str, 可选): 命名空间
- `repo_path` (str, 可选): 仓库路径
- `sig_group` (str, 可选): SIG 组
- `pr_state` (str, 可选): PR 状态 open/merged/closed
- `issue_state` (str, 可选): Issue 状态 open/closed
- `pr_number` (str, 可选): PR 编号
- `issue_number` (str, 可选): Issue 编号

**返回：** Issue 和 PR 的关联关系

---

## PR (3个)

### get_prs_aggregate
获取 PR 聚合统计：总数、开启数、关闭数、合并数、首次响应时长、合并率等。

**参数：**
- `community` (str, 可选): 社区名称
- `start_time` (str, 可选): 开始时间，格式 YYYY-MM-DD
- `end_time` (str, 可选): 结束时间，格式 YYYY-MM-DD
- `interval` (str, 可选): 时间粒度，支持 day/week/month

**返回：** PR 聚合统计数据

---

### get_prs_agg_page
获取 PR 汇总分页统计，支持按仓库/SIG/命名空间等维度分组。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `group_dim` (str, 可选): 分组维度，如 repo/sig/namespace，默认 repo
- `namespace` (str, 可选): 命名空间筛选
- `repo` (str, 可选): 仓库名称
- `pr_type` (str, 可选): PR 类型
- `private` (str, 可选): 是否私仓，true/false
- `desc` (str, 可选): 降序字段

**返回：** PR 汇总分页数据

---

### get_prs_detail
获取 PR 详情分页列表。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `namespace` (str, 可选): 命名空间
- `repo_path` (str, 可选): 仓库路径
- `title` (str, 可选): 标题关键字
- `state` (str, 可选): 状态 open/merged/closed
- `page_num` (int, 可选): 页码，默认 1
- `page_size` (int, 可选): 每页数量，默认 20

**返回：** PR 详情列表

---

## 论坛 (1个)

### get_forum_detail
获取论坛帖子详情分页列表。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `title` (str, 可选): 标题关键字
- `desc` (str, 可选): 降序字段，默认 created_at

**返回：** 帖子详情列表

---

## 贡献 (1个)

### get_contributes_topn
获取贡献 TopN 汇总排名，支持按组织/仓库/SIG/开发者维度统计。

**参数：**
- `community` (str, 可选): 社区名称
- `start_date` (str, 可选): 开始日期，格式 YYYY-MM-DD
- `end_date` (str, 可选): 结束日期，格式 YYYY-MM-DD
- `event` (str, 可选): 贡献类型，pr/issue/comment/addcode，默认 pr
- `metric` (str, 可选): 统计维度，company_type/company/sig/repo/user，默认 company_type
- `topn` (int, 可选): TopN 数量，默认 10
- `private` (str, 可选): 是否包含私仓，true/false，默认 false
- `org_list` (str, 可选): 逗号分隔的命名空间/组织列表

**返回：** 贡献 TopN 排名

---

## 其他 (2个)

### get_metric_dict
获取指标字典，包含所有可用指标的名称、中文名、单位和定义。

**参数：** 无

**返回：** 指标字典

---

### get_filter_options
获取社区数据筛选条件（如 SIG 列表、仓库列表、标签等）。

**参数：**
- `community` (str, 可选): 社区名称
- `tab` (str, 可选): 标签页标识，如 issue/pr/repo 等

**返回：** 筛选条件选项

---

## 更新记录

- 2026-03-10: 删除 get_cla_user_list、get_cla_trend（HTTP 404）；lib/http.py 改用标准 logging
- 2026-03-10: 删除全部失败(❌)和部分可用(⚠️)接口共 25 个，保留 13 个正常接口
