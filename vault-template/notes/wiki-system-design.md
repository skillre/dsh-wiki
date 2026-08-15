---
title: Wiki 系统设计：DSH + Obsidian
aliases: [wiki 设计, DSH wiki, 知识库架构]
tags: [wiki, dsh, obsidian, knowledge-management, karpathy]
status: published
mocs: ["[[MOC-Wiki-System]]"]
related: ["[[llm-knowledge-base]]"]
created: 2026-08-14
updated: 2026-08-14
source: ""
---

# Wiki 系统设计：DSH + Obsidian

> 本 wiki 是"卡帕西路线"的个人知识库：LLM（DSH agent）负责编译与维护，人类负责选材、审核与提问。本文是体系的第一篇笔记，定义结构与分工。

## 核心理念

**单一事实源 = Markdown vault（git 版本化）；DSH agent 是"采写/维护/检索大脑"，Obsidian 是"人类读写界面"；两者之间不引入数据库，只靠文件系统 + 书面约定解耦。**

理念谱系（详见 [[llm-knowledge-base]]）：

| 设计元素 | 理念来源 |
|---|---|
| LLM 编译 + 维护 markdown wiki | Karpathy LLM Knowledge Bases（内核） |
| 原子笔记 + 双向链接 | Zettelkasten / 常青笔记 |
| mocs/ 主题枢纽 | LYT（Map of Content） |
| inbox/ 收集流 | PARA 的收集箱（简化） |
| frontmatter 契约 | 轻量本体（弱本体论） |
| 生命周期 + git 审计 | 对 LLM 输出的信任边界 |

**刻意不做**：严格本体论（类层次/推理）、纯 Karpathy 全托管（无审核）、RAG/向量库（500 篇内不需要）。

## 目录结构

```
<vault>/
├── inbox/        agent 草稿区（status: draft）——信任边界
├── notes/        正式笔记（status: published / evergreen）
├── mocs/         MOC 主题导航（分类从这里生长）
├── sources/      素材与引用（只读区，ingest 取料）
├── templates/    frontmatter 模板
├── attachments/  二进制附件
├── .wiki/        agent 私有状态（索引、巡检报告）
└── .dsh/         DSH 配置（preset 定义，随库走）
```

## 笔记生命周期

```
inbox (draft) → 人工审核 → notes (published) → 长期稳定 → evergreen
                                         ↘ 过时/废弃 → archived（git 历史可回滚）
```

- **文件夹按状态分，不按主题分**：主题结构由 mocs/ + tags + related 链接承担，文件夹永远不会需要重新规划。
- **防冗余铁律**：写之前先检索——已有类似笔记就扩写，不新建。这是 `wiki-conventions` skill 的第一条。

## 分工

| 谁 | 做什么 |
|---|---|
| 人类 | 选材、审核 inbox → notes、提问、每周花 10 分钟看巡检报告 |
| DSH agent | ingest（研究→草稿）、write（扩写/双向链接）、maintain（断链/孤儿/冗余巡检）、digest（周报）、search（本地优先检索） |
| git | 审计、回滚、同步 |

## 使用入口

- **Obsidian**：读写笔记的地方（编辑/审核/Graph/Dataview）
- **DSH**：在 DSH Web GUI 里"选择工作区"添加 <vault>，新建会话即获得 vault 沙箱围栏
- **schedule**：每周自动巡检 + 摘要，报告推送到 wiki 会话

## 长期维护策略

- 微整理（日常）：写完挂 MOC、补 related
- 周期整理（每周自动）：maintain 报告 + digest 摘要，人类只做判断题
- 规模路线：<500 篇 grep+MOC 够用 → 500+ 上 `.wiki/index.json` 索引 → 更大再考虑向量检索
