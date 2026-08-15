---
name: wiki-digest
description: 'Use when asked for a wiki weekly review, digest, or summary of recent changes in the vault at <vault> — summarizes the period (git commits, new/updated notes, pending drafts), proposes maintenance actions (merges, MOC splits, reviews), and saves the digest to .wiki/reports/.'
---

# wiki-digest：周期回顾与周报

把一段时间（默认本周）的 vault 变化汇总成可执行的回顾。**先读 wiki-conventions，再执行本流程。**

## 流程

### 1. 收集变化

- `git log --since="7 days ago" --oneline`（默认周期；用户指定其他周期则用其范围）——commit 是唯一权威变化记录。
- 列出：新增笔记、修改笔记、待审草稿（`inbox/` 当前状态）。

### 2. 阅读变化内容

- 对每篇新增/大改笔记，读全文，提取：主题、核心观点、与已有知识的关联。
- 对草稿，标注"待审核"。

### 3. 生成回顾

输出结构：

```markdown
# Wiki 周报 — YYYY-MM-DD ~ YYYY-MM-DD

## 本周变化
- 新增 N 篇：[[a]]（一句话）、[[b]]（一句话）…
- 更新 M 篇：[[c]]（改了什么）…
- 待审核草稿 K 篇：[[d]] …

## 健康度速览
（若本周未巡检：先跑 `python3 <vault>/.dsh/scripts/maintain.py`；否则直接引用 `.wiki/reports/SUMMARY.md` 的关键数字）

## 建议（按优先级）
1. 合并候选：[[x]] 与 [[y]] 主题重叠 → 建议合并
2. MOC 调整：MOC-XX 已 28 篇 → 建议拆分
3. 补链：[[z]] 是孤儿 → 建议挂到 [[MOC-XX]]
4. 待审核：inbox 里 [[d]] 请审阅

## 可执行的下一步
（等待用户拍板的判断题列表）
```

### 4. 收尾

- 存 `.wiki/reports/digest-YYYY-MM-DD.md`。
- `git add -A && git commit`，message："digest: <日期范围> 周报"。
- 在对话中呈现周报全文，请用户逐条拍板。

## 边界

- 只读 `notes/`、`mocs/`、`sources/`；只写 `.wiki/`。
- 建议必须可执行（给出具体动作和证据），不空谈"保持更新"。
