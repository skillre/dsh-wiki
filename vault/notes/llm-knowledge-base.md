---
title: LLM Knowledge Bases（卡帕西理念）
aliases: [LLM 知识库, Karpathy LLM Wiki, LLM 编译式知识库]
tags: [karpathy, knowledge-management, llm, obsidian, wiki]
status: published
mocs: ["[[MOC-Wiki-System]]"]
related: ["[[wiki-system-design]]"]
created: 2026-08-14
updated: 2026-08-14
source: https://community.tmpdir.org/t/llm-knowledge-bases/1685
---

# LLM Knowledge Bases（卡帕西理念）

> Karpathy（OpenAI 创始成员、前特斯拉 AI 总监）2025 年提出的个人知识库工作流：用 LLM 把原始信息"编译"成结构化 markdown wiki，并由 LLM 持续维护。本 wiki 的体系内核即源于此。

## 核心思想

- **原始信息 = 源代码，LLM = 编译器**：网页、论文、repo 全扔进 raw 文件夹，LLM 读取、总结、编译成结构化 wiki（Karpathy 本人用 Obsidian）。
- **维护交给 LLM**："人类放弃 wiki 是因为维护成本增长快于价值；LLM 不会厌倦，不会忘记更新交叉引用，可以一次触碰 15 个文件。"
- **人类只做策展**：选素材、提问题、想清楚"这到底意味着什么"。
- **明确不搞 RAG/向量库**：就是 markdown wiki + LLM 增量编译，不依赖复杂检索管线。

## 理念谱系（本 wiki 的出处）

| 设计元素 | 理念来源 |
|---|---|
| LLM 编译 + 维护 markdown wiki | Karpathy LLM Knowledge Bases（内核） |
| 原子笔记 + 双向链接 | Zettelkasten / 常青笔记 |
| mocs/ 主题枢纽 | LYT（Map of Content） |
| inbox/ 收集流 | PARA 的收集箱（简化） |
| frontmatter 契约 | 轻量本体（弱本体论） |
| 生命周期 + git 审计 | 对 LLM 输出的信任边界 |

## 本 wiki 在其之上的修正

1. **人机审核双轨**：agent 产物只进 `inbox/`（draft），人工审核后才进 `notes/`——防幻觉污染。
2. **frontmatter 契约层**：受控字段让 Obsidian Dataview 与 agent 检索共享同一接口。
3. **周期巡检机制化**：schedule 驱动的 maintain/digest，把"整理"从自律变成机制。

## 来源

- [Karpathy 原文摘录（TMPDIR 社区）](https://community.tmpdir.org/t/llm-knowledge-bases/1685)
- [编译器类比解读（MindStudio）](https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy)
- [DAIR.ai 拆解](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)
- [实操工作流拆解（LinkedIn）](https://www.linkedin.com/posts/hamna-aslam-kahn_andrej-karpathy-shared-how-he-actually-uses-activity-7480966492063277056-6LLN)
