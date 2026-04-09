---
name: gen-excel-report
description: 将指定目录下的开源社区运营质量 Markdown 月度报告，整理生成 Excel 对比表。自动发现目录内所有报告文件，解析指标数据，套用报告模板样式后输出 .xlsx 文件。
argument-hint: <reports_dir> [output_name]
---

将 **$ARGUMENTS** 目录下的社区月度报告整理成 Excel 对比表。

## 执行步骤

### 1. 解析参数

从 `$ARGUMENTS` 中提取：
- `reports_dir`：包含 `*_community_quality_monthly_*.md` 文件的目录（相对于项目根目录，如 `reports/202603`）
- `output_name`（可选）：输出文件名（不含 `.xlsx`），默认为 `upstream_community_report_<dirname>`

如果 `reports_dir` 不存在或目录内没有 `.md` 报告文件，告知用户并终止。

### 2. 运行脚本

切换到项目根目录并执行：

```bash
cd /Users/zhangcan/Documents/code/om-mcp
python3 .claude/skills/gen-excel-report/gen_excel_report.py $ARGUMENTS
```

脚本会：
- 自动发现目录内所有 `*_community_quality_monthly_*.md` 文件
- 解析每份报告的主报告段落（上一自然月数据，不含当月补充报告）
- 套用 `reports/template/report-template.xlsx` 的样式（字体、颜色、边框、行高列宽）
- 生成 Excel 文件并保存至 `<reports_dir>/<output_name>.xlsx`
- 在 stderr 输出解析进度，在 stdout 输出 JSON 摘要

### 3. 向用户汇报结果

读取脚本的 JSON 输出，向用户汇报：
- 输出文件路径
- 涵盖的社区列表
- 统计周期（如 2026年02月 vs 01月）
- 如有解析失败，说明原因

### 4. 异常处理

| 错误 | 处理方式 |
|------|----------|
| 目录不存在 | 提示用户确认路径 |
| 模板文件缺失 | 提示确认 `reports/template/report-template.xlsx` 存在 |
| `openpyxl` 未安装 | 提示 `pip install openpyxl` |

---

## 输出规范

- **文件路径**：`<reports_dir>/<output_name>.xlsx`
- **Sheet 名称**：`综合指标对比`
- **列结构**：A-C 为指标标签，每个社区占 2 列（上月 / 当月）
- **颜色编码**：
  - 上月数据：灰色（参考值）
  - 当月改善：绿色加粗（活跃度上升 / 响应时长缩短）
  - 当月下降：红色加粗（活跃度下降 / 响应时长延长 / 组织数持平或下降）
- **指标范围**：13 项核心指标，与月度 Markdown 报告章节一一对应
- **无数据指标**：显示 `—`（TTFHW、CI 指标等上游社区通常无数据）
