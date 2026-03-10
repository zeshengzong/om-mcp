# MCP 接口测试结果

测试时间：2026-03-10
测试社区：openEuler（除特殊说明外）

说明：
- ✅ 通过：接口正常返回数据

---

## 社区相关

### get_community_health ✅
**测试问题**：openEuler 社区 2026-03-01 的健康度如何？
**调用参数**：community=openEuler, date=2026-03-01
**返回结果**：
```
社区：openeuler
数据日期：2026-03-01
综合健康度评分：4.24 / 5.0

各指标评分（1-5分）及原始值：
  - 社区影响力(NSS)：5 分（原始值：0.69）
  - 下载量：5 分（原始值：6308471）
  - Issue关闭率：3 分（原始值：0.7651163）
  - 认证：4 分（原始值：5）
  - 首次响应：5 分（原始值：0.78729165）
  - 杠杆率：5 分（原始值：2.5136857）
  - 技术影响力：4 分（原始值：562.0）
  - 版本发布：5 分（原始值：0.0）
  - 大象系数：4 分（原始值：4）
  - 有效维护：5 分（原始值：0.93181366）
  - 贡献多样性：5 分（原始值：63）
  - 贡献者互动：1 分（原始值：1.0）
```

---

### list_communities ✅
**测试问题**：列出所有支持查询的社区
**调用参数**：无
**返回结果**：
```
支持查询的社区列表（共 23 个）：
ascendnpuir, boostkit, cann, cannopen, mindcluster, mindie,
mindseriessdk, mindspeed, mindspore, mindstudio, openeuler,
openfuyao, opengauss, opensource, openubmc, pta, pytorch,
sgl, tilelang, triton, unifiedbus, verl, vllm
```

---

### get_community_list ✅
**测试问题**：获取所有社区列表
**调用参数**：无
**返回结果**：共 23 个社区（含 openEuler、openGauss、MindSpore 等）

---

## Issue

### get_issues_aggregate ✅
**测试问题**：openEuler 社区 2026 年 Q1 的 Issue 统计情况
**调用参数**：community=openEuler, start_time=2026-01-01, end_time=2026-03-10
**返回结果**：
```
Issue 聚合统计：
  总数：4580
  开启中：2499
  已关闭：3350
  关闭率：0.4544
  平均首次响应时长：15.67 天
  平均关闭时长：20.37 天
```

---

### get_issues_agg_page ✅
**测试问题**：openEuler 社区按仓库维度的 Issue 汇总统计
**调用参数**：community=openEuler, group_dim=repo
**返回结果**：共 12010 条记录，返回前 10 条仓库 Issue 统计

---

### get_issues_detail ✅
**测试问题**：查看 openEuler 社区最近的 Issue 详情
**调用参数**：community=openEuler, page_num=1, page_size=3
**返回结果**：
```
Issue 详情（共 24400 条，8134 页）：
  #N/A [open] [任务]: 同步企业标签 — N/A — 2025-11-08 15:02:25
  #N/A [closed] openEuler项目个人数据共享授权协议 — N/A — 2025-11-27 14:26:54
  #N/A [open] epkg-autopkg是否对外可用 — N/A — 2025-07-10 16:37:38
```

---

### get_issue_ref_pr ✅
**测试问题**：查看 openEuler 社区 Issue 和 PR 的关联关系
**调用参数**：community=openEuler
**返回结果**：共 172184 条记录，返回前 10 条关联关系

---

## PR

### get_prs_aggregate ✅
**测试问题**：openEuler 社区 2026 年 Q1 的 PR 总数是多少？
**调用参数**：community=openEuler, start_time=2026-01-01, end_time=2026-03-10
**返回结果**：
```
PR 聚合统计：
  总数：16374
  开启中：1764
  已关闭：2548
  已合并：12502
  关闭率：0.8923
  平均首次响应时长：3.47 天
  平均关闭时长：4.41 天
```

---

### get_prs_agg_page ✅
**测试问题**：openEuler 社区按仓库维度的 PR 汇总统计
**调用参数**：community=openEuler, group_dim=repo
**返回结果**：
```
PR 汇总（按 repo 分组）（共 12090 条，1209 页）：
  [kernel] 开启 1069，平均响应 22.43 天
  [qemu] 开启 69，平均响应 6.78 天
  [openeuler-docker-images] 开启 54，平均响应 1.68 天
  ...
```

---

### get_prs_detail ✅
**测试问题**：查看 openEuler 社区最近的 PR 详情
**调用参数**：community=openEuler, page_num=1, page_size=3
**返回结果**：
```
PR 详情（共 71353 条，23785 页）：
  #N/A [merged] [Bugfix] Add sort demo and fix some bugs — 2025-07-17 16:48:29
  #N/A [merged] feat: add PR close command and improve project configuration — 2026-01-30 21:08:36
  #N/A [merged] feat: add PR, Issue comment and license check commands — 2026-01-31 12:51:01
```

---

## 论坛

### get_forum_detail ✅
**测试问题**：openEuler 社区论坛最新帖子列表
**调用参数**：community=openEuler
**返回结果**：
```
论坛帖子详情（共 549 条，55 页）：
  [2026-03-09] issue关联PR — 回复 0，浏览 0
  [2026-03-09] openEuler24.03安装vmwareworkstation启动时 gcc找不到 报错处理 — 回复 0，浏览 0
  [2026-03-07] 服务器全天待命，飞书Agent秒响应：OpenClaw x openEuler 容器化部署指南 — 回复 0，浏览 0
  ...
```

---

## 贡献

### get_contributes_topn ✅
**测试问题**：openEuler 社区按公司类型的 PR 贡献 Top5 排名
**调用参数**：community=openEuler, event=pr, metric=company_type, topn=5
**返回结果**：
```
贡献 Top5（维度：company_type，类型：pr）：
  1. 企业 — 23748
  2. 华为 — 13602
  3. 个人贡献者 — 12622
  4. robot — 3939
  5. 学生 — 13
```

---

## 其他

### get_metric_dict ✅
**测试问题**：获取所有可用指标的字典
**调用参数**：无
**返回结果**：返回约 120+ 个指标定义，含名称、中文名、单位、适用范围等

---

### get_filter_options ✅
**测试问题**：openEuler 社区 Issue 页面的筛选条件有哪些？
**调用参数**：community=openEuler, tab=issue
**返回结果**：返回 15 个筛选条件组合（source/namespace/internal/private 维度）

---

## 测试汇总

| 状态 | 数量 | 接口列表 |
|------|------|---------|
| ✅ 通过 | 13 | get_community_health, list_communities, get_community_list, get_issues_aggregate, get_issues_agg_page, get_issues_detail, get_issue_ref_pr, get_prs_aggregate, get_prs_agg_page, get_prs_detail, get_forum_detail, get_contributes_topn, get_metric_dict, get_filter_options |
