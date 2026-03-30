---
name: gen-osc-report
description: 使用 om-metrics MCP 工具生成 MindIE/MindSpeed/MindSDK(mindseriessdk)/MindCluster/MindStudio/vLLM/PTA/Triton/Tilelang 等社区的运营质量月度报告和环比分析。当用户要求生成 Mind*/vLLM/PTA/Triton/Tilelang 等社区的月报、质量报告、运营报告、环比报告时，必须使用此技能。也支持自定义社区列表。
argument-hint: [community1 community2 ...] (默认: mindie mindspeed mindseriessdk mindcluster mindstudio vllm pta triton tilelang)
---

# 生成社区运营质量月度报告

使用 om-metrics MCP 工具为 `$ARGUMENTS`（若为空则默认 `mindie mindspeed mindseriessdk mindcluster mindstudio vllm pta triton tilelang`）生成月度运营质量报告。

---

## 第一步：确定统计周期

根据**今天的日期**自动计算三个时间段：

```
今天 = 当前日期（如 2026-03-27）

上月 (last)   = 今天的上一个自然月，为主报告期
              示例：3月 → 上月 = 2月（2026-02-01 ～ 2026-02-28）

上上月 (prev) = 上月的上一个自然月，为环比基准
              示例：3月 → 上上月 = 1月（2026-01-01 ～ 2026-01-31）

当月 (curr)  = 本月1日到今天，为补充报告期
              示例：当月 = 3月（2026-03-01 ～ 今天）
```

计算各时间点的毫秒时间戳（UTC）：
- `last_start_ms`：上月1日 00:00:00 UTC
- `last_end_ms`：上月末日 23:59:59 UTC
- `last_lastday_ms`：上月末日 00:00:00 UTC（用于单时间点接口）
- `prev_start_ms`：上上月1日 00:00:00 UTC
- `prev_end_ms`：上上月末日 23:59:59 UTC
- `prev_lastday_ms`：上上月末日 00:00:00 UTC
- `curr_start_ms`：本月1日 00:00:00 UTC
- `curr_end_ms`：今天 00:00:00 UTC（或当前时刻）

报告保存路径：`reports/{YYYYMM}/` 其中 YYYYMM 为今天的年月（如 `202603`）

---

## 第二步：对每个社区并行查询所有指标

对每个社区，调用以下 MCP 工具（**工具名由路径拼接，前缀为 `get_`**）。查询三个时间段（`last`、`prev`、`curr`），以便生成主报告（last vs prev 环比）和当月补充报告（curr vs last 环比）。

### 工具调用列表（10个工具 × 3个时间段）

**① 贡献指标** `get_stats_contribute`
- 参数：`community`, `interval="month"`, `start`, `end`
- 提取字段：`activate_user`（活跃开发者数）、`merged_prs`（合入PR数）、`issues`（提交Issue数）
- 从返回的列表中找到 `month_date` 前缀匹配目标月份的条目

**② 有效评论数** `get_stats_valid_comment`
- 参数：`community`, `interval="month"`, `start`, `end`
- 提取字段：`comments`（有效Review总数）、`avg_comments`（每PR平均Review数）

**③ 项目集成引用度** `get_stats_itegration`
- 参数：`community`（无时间参数，返回汇总值）
- 提取字段：`count`（适配/集成/引用项目总数）

**④ TOP开发者留存率** `get_stats_user_retention`
- 参数：`community`, `date`（传入 `last_lastday_ms` 查上月，`prev_lastday_ms` 查上上月，`curr_end_ms` 查当月）
- 提取字段：`ratio`（留存率，百分比）

**⑤ YTD下载量** `get_stats_year_download`
- 参数：`community`, `date`（传入 `last_lastday_ms`/`prev_lastday_ms`/`curr_end_ms`）
- 提取字段：`download`（年初至该时间点的累计下载量，万次）

**⑥ Issue指标** `get_stats_issue`
- 参数：`community`, `date`（传入 `last_lastday_ms`/`prev_lastday_ms`/`curr_end_ms`）
- 提取字段：`issues`（Issue提交数）、`avg_first_reply_time`、`median_first_reply_time`、`avg_close_time`、`median_closed_time`（单位：天）

**⑦ 论坛指标** `get_stats_forum`
- 参数：`community`, `date`（传入 `last_lastday_ms`/`prev_lastday_ms`/`curr_end_ms`）
- 提取字段：`posts`（新增帖子数）、`avg_first_reply_time`、`median_first_reply_time`、`avg_closed_time`、`median_closed_time`（单位：天）

**⑧ 健康度/版本发布偏差** `get_stats_health_metric`
- 参数：`community`, `metric="version_release"`, `date`（传入 `last_lastday_ms`/`prev_lastday_ms`/`curr_end_ms`）
- 提取字段：`avg`（版本发布偏差天数；0.0 = 按时发布，null/无数据 = 暂无）

**⑨ 组织多样性** `get_stats_company`
- 参数：`community`, `interval="month"`, `start`, `end`
- 提取字段：`count`（贡献组织数）

**⑩ 搜索指数** `get_stats_influence`
- 参数：`community`, `interval="month"`, `start`, `end`
- 提取字段：`avg_index`（主流平台平均搜索指数）

---

## 第三步：下载量特殊计算

YTD下载量需要特殊处理：
- **上月当月下载量** = `last` YTD − `prev` YTD
- **上上月当月下载量** = `prev` YTD − `prev_prev` YTD（若无则用 `prev` YTD 作为首月值）
- **月度环比** = （上月下载量 − 上上月下载量）/ 上上月下载量
- 对于当月补充报告：**当月下载量（截至今日）** = `curr` YTD − `last` YTD

---

## 第四步：生成 Markdown 报告

每个社区生成一份报告，包含**主报告**（上月 vs 上上月）和**当月补充报告**（当月截至今日 vs 上月）。

### 文件路径
`reports/{YYYYMM}/{community}_community_quality_monthly_{YYYYMM}.md`

### 报告模板

```markdown
# {社区展示名} 社区运营质量月度报告 — {YYYY}年{M}月

> 统计周期：{上月日期范围}
> 环比对象：{上上月日期范围}
> 生成日期：{今天}

---

## 一、贡献活跃度

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 活跃开发者数 | **{last.activate_user} 人** | {prev.activate_user} 人 | {环比箭头} |
| 合入 PR 数 | **{last.merged_prs} 个** | {prev.merged_prs} 个 | {环比箭头} |
| 提交 Issue 数 | **{last.issues} 个** | {prev.issues} 个 | {环比箭头} |

> {数据解读：结合季节性（如春节）、趋势分析}

---

## 二、代码审查质量

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 有效 Review 总数 | **{last.comments} 条** | {prev.comments} 条 | {环比箭头} |
| 每 PR 平均 Review 数 | **{last.avg_comments} 条** | {prev.avg_comments} 条 | {环比箭头或"— 持平"} |

> {数据解读}

---

## 三、领域主流项目适配集成引用度

| 指标 | 数值 | 说明 |
|------|:----:|------|
| 适配 / 集成 / 引用项目总数 | **{itegration.count} 个** | 汇总值，无月度拆分 |

> {数据解读}

---

## 四、TOP 开发者留存

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| TOP 开发者留存率 | **{last.ratio}%** | {prev.ratio}% | {环比或"— 持平"} |

> {数据解读}

---

## 五、社区下载量（YTD）

| 指标 | 数值 | 说明 |
|------|:----:|------|
| {上月}月当月下载量 | **{上月当月下载量} 万次** | {上月}月YTD − {上上月}月YTD |
| {上上月}月当月下载量 | {上上月当月下载量} 万次 | 参考对比 |
| 月度环比 | {环比箭头} | {上月}月当月 vs {上上月}月当月 |
| 年初累计（{上月}月 YTD）| **{last_ytd} 万次** | {年初} ～ {上月末} |
| {上上月}月 YTD（上月末累计）| {prev_ytd} 万次 | {年初} ～ {上上月末} |
| YTD 累计环比 | {环比箭头} | {上月}月YTD vs {上上月}月YTD |

> {数据解读，包含计算过程说明}

---

## 六、Issue 响应与处理效率

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 提交 Issue 数 | **{last.issues} 个** | {prev.issues} 个 | {环比箭头} |
| 平均首次响应时长 | **{last.avg_first_reply_time} 天** | {prev.avg_first_reply_time} 天 | {改善/延长方向} |
| 中位首次响应时长 | **{last.median_first_reply_time} 天** | {prev.median_first_reply_time} 天 | {改善/延长方向} |
| 平均关闭时长 | **{last.avg_close_time} 天** | {prev.avg_close_time} 天 | {改善/延长方向} |
| 中位关闭时长 | **{last.median_closed_time} 天** | {prev.median_closed_time} 天 | {改善/延长方向} |

> {数据解读：注意响应时长缩短为改善，延长为退步}

---

## 七、论坛响应与处理效率

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 新增帖子数 | **{last.posts} 个** | {prev.posts} 个 | {环比箭头} |
| 平均首次响应时长 | **{last.avg_first_reply_time} 天** | {prev.avg_first_reply_time} 天 | {改善/延长方向} |
| 中位首次响应时长 | **{last.median_first_reply_time} 天** | {prev.median_first_reply_time} 天 | {改善/延长方向} |
| 平均关闭时长 | **{last.avg_closed_time} 天** | {prev.avg_closed_time} 天 | {改善/延长方向} |
| 中位关闭时长 | **{last.median_closed_time} 天** | {prev.median_closed_time} 天 | {改善/延长方向} |

> {数据解读}

---

## 八、版本稳定发布偏差

| 指标 | {上月}月（当期） | {上上月}月（上期） | 说明 |
|------|:-----------:|:-----------:|------|
| 版本发布偏差 | **{last.avg 天 或 —}** | {prev.avg 天 或 —} | {0.0=按时发布/暂无数据} |

> {数据解读}

---

## 九、社区组织多样性

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 贡献组织数 | **{last.count} 个** | {prev.count} 个 | {环比箭头} |

> {数据解读}

---

## 十、主流平台搜索指数

| 指标 | {上月}月（当期） | {上上月}月（上期） | 环比 |
|------|:-----------:|:-----------:|:----:|
| 平均搜索指数 | **{last.avg_index}** | {prev.avg_index} | {环比箭头} |

> {数据解读}

---

## 综合分析

### 正向趋势
- {列举改善的指标，加粗关键数字，注明改善幅度}

### 需要关注
- {列举退步或需关注的指标}

---

*数据来源：datastat.osinfra.cn | 报告由 Claude Code 自动生成*
```

紧接着追加当月补充报告（格式与主报告完全相同，但标题改为"补充报告 — {M}月数据环比"，时间段改为 curr vs last）。

---

## 第五步：环比格式规范

### 贡献类指标（越大越好）
- 上升：`▲ 改善 +X.X%`（绿色语义）
- 下降：`▼ -X.X%`
- 持平：`— 持平`

### 响应时长类指标（越小越好）
- 缩短（改善）：`▲ 改善 -X.X%`
- 延长（退步）：`▼ 延长 +X.X%`
- 持平：`— 持平`

### 计算公式
```
环比 = (当期 - 上期) / |上期| × 100%
```
保留一位小数，当 |差值/上期| < 0.5% 时显示"— 持平"。

---

## 第六步：无数据处理规则

| 情况 | 报告中展示 |
|------|-----------|
| API返回空/null/无数据 | `—` |
| 版本发布偏差 avg = 0.0 | `0.0 天 ✅ 按时发布` |
| 版本发布偏差无数据 | `— 暂无版本发布数据` |
| 下载量无数据 | `— 暂无下载数据` |
| 论坛无帖子 | 显示 `0 个`，时长字段显示 `—` |

---

## 社区名称展示映射

| MCP 社区名 | 报告展示名 |
|-----------|-----------|
| mindie | MindIE |
| mindspeed | MindSpeed |
| mindseriessdk | MindSDK |
| mindcluster | MindCluster |
| mindstudio | MindStudio |
| openeuler | openEuler |
| opengauss | openGauss |
| mindspore | MindSpore |
| cann | CANN |
| vllm | vLLM |

其他社区按原名首字母大写展示。

---

## 执行完成后

向用户汇报：
1. 成功生成的报告文件路径列表
2. 统计周期（主报告：X月 vs Y月）
3. 当月补充周期（Z月1日 ～ 今日）
4. 如有某社区某指标无数据，简要说明
