---
name: community-quality-report
description: 生成开源社区运营质量月度报告。Use when the user asks to generate a community quality monthly report, monthly trend analysis, 运营质量月报, 社区质量月度报告, 月度趋势分析, or wants the 15 community quality metrics for a given month. 触发关键词：月报、月度报告、运营质量、趋势分析、社区质量。
---

# 社区质量运营月度报告生成工作流

当用户要求生成某社区某月的运营质量月度报告 / 月度趋势分析时，按本流程执行。

## 一、确定参数

1. **社区名称**：用 `list_communities` 核实；名称需在 COMMUNITY_MAP 中。
2. **目标月份**：用户指定的报告月份（如 2026 年 3 月）。

## 二、时间戳计算（强制规则）

**禁止心算时间戳**，必须用 bash 命令计算（东八区 CST，UTC+8）：

```bash
python3 -c "
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=8))
# 月初
dt_start = datetime(YYYY, MM, 1, 0, 0, 0, tzinfo=tz)
# 月末（下月1日 - 1秒）
dt_end = datetime(YYYY, MM+1, 1, 0, 0, 0, tzinfo=tz) - timedelta(seconds=1)
print('start_ms', int(dt_start.timestamp())*1000)
print('end_ms', int(dt_end.timestamp())*1000)
"
```

### 统计周期规则

- **统计周期 = 上一个自然月**。例如 3 月报告 → 统计 2 月 1 日 ~ 2 月末。
  - 当期：目标月份的"上一个月"
  - 上期（环比对象）：目标月份的"上上个月"
- 工具仅有单个时间参数（如 `date`）时，传入**上月末 23:59:59 CST** 的毫秒时间戳。
- **下载量例外**（指标 6）：用 `get_stats_year_download` 取 YTD 累计值，需取"当月 YTD"和"上月 YTD"两个时点，相减得当月下载量，再算环比。

### 2026 年各月边界参考（CST 毫秒时间戳）

| 月份 | 月初 00:00:00 | 月末 23:59:59 |
|------|---------------|---------------|
| 1月  | 1767196800000 | 1769875199000 |
| 2月  | 1769875200000 | 1772294399000 |
| 3月  | 1772294400000 | 1774972799000 |
| 4月  | 1774972800000 | 1777564799000 |
| 5月  | 1777564800000 | 1780243199000 |

## 三、调用 15 项指标对应 MCP 工具

并行调用以提高效率。数据不可用时在报告中写"API错误：暂无数据"，**不得整节省略**。

| # | 指标 | MCP 工具 | 关键字段 |
|---|------|---------|---------|
| 1 | 当期活跃开发者数 | `get_stats_contribute` | `activate_user` |
| 2 | 合入PR个数、提交Issue个数 | `get_stats_contribute` | `merged_prs`, `issues` |
| 3 | 有效Review总数、均值 | `get_stats_valid_comment` | `comments`, `avg_comments` |
| 4 | 领域主流项目适配、集成、引用度 | `get_stats_itegration` | `count` |
| 5 | TOP开发者留存率 | `get_stats_user_retention` | `ratio` |
| 6 | YTD社区下载量 | `get_stats_year_download` | `download` |
| 7 | Issue首次响应时间（均值、中位数）（天） | `get_stats_issue` | `avg_first_reply_time`, `median_first_reply_time` |
| 8 | Issue闭环时间（均值、中位数）（天） | `get_stats_issue` | `avg_closed_time`, `median_closed_time` |
| 9 | 论坛平均首次响应时间（均值、中位数）（天） | `get_stats_forum` | `avg_first_reply_time`, `median_first_reply_time` |
| 10 | 论坛平均闭环时间（均值、中位数）（天） | `get_stats_forum` | `avg_closed_time`, `median_closed_time` |
| 11 | 版本稳定发布偏差 | `get_stats_health_metric(metric=version_release)` | `avg` |
| 12 | 社区组织多样性 | `get_stats_company` | `count` |
| 13 | 主流平台搜索指数 | `get_stats_influence` | `avg_index` |
| 14 | 社区严重缺陷数 | `get_stats_cve` | `total_count` |
| 15 | 负向事件数量 | `get_stats_negative_event` | `total_count` |

### 环比计算

- 指标 1/2/3/5/7/8/9/10/12：需同时取"当期"和"上期"两份数据计算环比（▲上升 / ▼下降百分比）。
- 指标 4/11：仅汇总值，无月度拆分，直接展示。
- 指标 6：见上方"下载量例外"规则。
- 指标 13/14/15：当期值即可。

## 四、生成报告

- 保存路径：`reports/`
- 文件命名：`{community}_community_quality_monthly_{YYYYMM}.md`
- 示例：`openeuler_community_quality_monthly_202603.md`

### 完整性检查清单（保存前逐项核对）

报告必须包含以下全部 15 个章节，数据不可用写"API错误：暂无数据"，不得省略：

1. ✅ 贡献活跃度（活跃开发者数、合入PR数、提交Issue数）
2. ✅ 代码审查质量（有效Review总数、均值）
3. ✅ 领域主流项目适配集成引用度
4. ✅ TOP开发者留存率
5. ✅ 社区下载量（YTD，含当月+YTD+月度环比+年累计环比）
6. ✅ Issue平均/中位首次响应时长（天）
7. ✅ Issue平均/中位关闭时长（天）
8. ✅ 论坛平均/中位首次响应时长（天）
9. ✅ 论坛平均/中位关闭时长（天）
10. ✅ 版本稳定发布偏差（0.0 表示按时发布）
11. ✅ 社区组织多样性（贡献组织数）
12. ✅ 主流平台搜索指数
13. ✅ 社区严重缺陷数
14. ✅ 负向事件数量
15. ✅ 综合分析（趋势小结）

### 报告头部模板

```
# {社区名} 社区运营质量月度报告 — {YYYY年M月}

> 统计周期：{当期起始} ～ {当期结束}
> 环比对象：{上期起始} ～ {上期结束}
> 生成日期：{今天}
```

每节用表格呈现"当期 / 上期 / 环比"三列，并附一句趋势解读。

## 五、执行要点

- 社区名称统一小写传入工具。
- 工具返回 `code != 1` 时记为"API错误：暂无数据"，继续其余指标，不要中断。
- 指标 11（版本发布偏差）为 0.0 表示按时发布，非异常。
- 参考已有报告样例：`reports/example_community_quality_monthly_202603.md`。
