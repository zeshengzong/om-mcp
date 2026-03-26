---
name: gen-quality-report
description: 生成开源社区运营质量月度报告。接收一个或多个社区名称，自动查询 datastat API、计算环比指标，并将完整 Markdown 报告写入 reports/ 目录。
argument-hint: <community1> [community2 ...]
---

生成 **$ARGUMENTS** 的社区运营质量月度报告。

## 执行步骤

### 1. 解析社区列表

从 `$ARGUMENTS` 中提取社区名称（支持空格或逗号分隔）。
有效社区名称（小写）包括：
`openeuler`, `opengauss`, `openubmc`, `mindspore`, `mindie`, `mindstudio`, `mindspeed`,
`mindcluster`, `mindseriessdk`, `cann`, `cannopen`, `vllm`, `triton`, `tilelang`, `pta`,
`pytorch`, `sgl`, `verl`, `ascendnpuir`, `boostkit`, `unifiedbus`, `openfuyao`

如果输入的社区名称不在列表中，告知用户并跳过该社区。

### 2. 运行数据采集与报告生成脚本

切换到项目根目录并执行：

```bash
cd /Users/zhangcan/Documents/code/om-mcp
python3 .claude/skills/gen-quality-report/gen_report.py $ARGUMENTS
```

脚本会：
- 根据当前日期自动推算统计周期（上一自然月为主报告期，上上月为对比期，当月为补充报告期）
- 并发调用 `https://datastat.osinfra.cn/server` 的各 stats API 拉取所有指标
- 生成完整 Markdown 报告并写入 `reports/` 目录
- 在 stderr 输出进度，在 stdout 输出 JSON 结果摘要

**注意**：脚本依赖系统代理访问远程 API（已通过 `all_proxy` 环境变量配置），无需手动设置。

### 3. 向用户汇报结果

读取脚本的 JSON 输出，向用户汇报：
- 成功生成的报告文件列表（路径）
- 报告覆盖的统计周期
- 如有失败，说明失败原因

### 4. 异常处理

若脚本执行失败（非零退出码），检查原因：
- **代理不通**：提示用户检查 `all_proxy` 环境变量是否正确
- **社区名称无效**：列出 COMMUNITY_MAP 中的有效名称
- **Python 依赖缺失**：提示 `pip install httpx socksio`
- **其他错误**：显示完整错误信息并建议排查方向

---

## 报告规范参考

生成的报告遵循以下规范（已内置在脚本中，仅供参考）：

- **文件路径**：`reports/{community}_community_quality_monthly_{YYYYMM}.md`
- **统计周期**：上一自然月（例如3月生成时，统计2月数据）
- **环比对象**：上上自然月
- **补充报告**：当月截至今日的数据（附在同一文件末尾）
- **13项指标**：贡献活跃度、代码审查、适配引用度、开发者留存、下载量、Issue效率、论坛效率、版本偏差、组织多样性、搜索指数

对于 API 返回无数据的指标，报告中标注"暂无数据"并给出数据采集建议。
