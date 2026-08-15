---
name: wiki-maintain
description: 'Use when asked to inspect, audit, or maintain the Obsidian wiki vault at <vault> — runs the maintain.py health check (broken links, orphan notes, duplicate candidates, stale content, MOC balance, pending drafts), regenerates the .wiki/index.json search index, and summarizes the reports for human review.'
---

# wiki-maintain：巡检与索引

对 vault 做系统性健康检查，产出报告（**只报告，不擅自修改正式区**）。**先读 wiki-conventions，再执行本流程。**

## 流程

### 1. 生成索引 + 巡检报告（脚本，确定性）

```sh
python3 <vault>/.dsh/scripts/gen-index.py
python3 <vault>/.dsh/scripts/maintain.py [--stale-months N]
```

脚本产出 `.wiki/reports/`：

| 报告 | 内容 |
|---|---|
| `links.md` | 断链（wikilink 指向不存在的目标；模板占位符已排除） |
| `orphans.md` | 孤儿笔记（notes/mocs 中零入链） |
| `duplicates.md` | 重复候选（tags 重叠 ≥3 或前缀相同 + 重叠 ≥2） |
| `stale.md` | 过期内容（published/evergreen 且 updated 超 N 个月，默认 6） |
| `mocs.md` | 每个 MOC 挂载数（>30 提示拆分，=0 提示废弃） |
| `inbox.md` | 待审草稿清单 |
| `SUMMARY.md` | 汇总数字 + 优先行动项（给人看的） |

### 2. 汇报

- 向用户呈现 SUMMARY 要点（数字 + 行动项），**等用户拍板**。
- 用户授权后才执行修复（补链、合并、移动 → 走 wiki-write 流程）。

### 3. 收尾

- `git add -A && git commit`，message："maintain: <日期> 巡检报告 + 索引更新"。

## 边界

- 只写 `.wiki/`；`notes/`、`mocs/` 只读。
- 报告是"建议"不是"判决"——修复动作需用户明确授权。
- 脚本只能发现机械问题（断链/孤儿/重复/过期）；内容矛盾、质量下降需要人读报告判断。
