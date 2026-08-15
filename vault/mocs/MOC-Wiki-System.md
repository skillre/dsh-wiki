---
title: MOC：Wiki 系统
aliases: [Wiki 系统索引]
tags: [wiki, dsh, index]
status: published
mocs: []
related: []
created: 2026-08-14
updated: 2026-08-14
source: ""
---

# MOC：Wiki 系统

本 wiki 自身的体系与基础设施导航。

## 体系笔记

- [[wiki-system-design]] —— 系统设计总纲（结构、生命周期、分工）
- [[llm-knowledge-base]] —— 卡帕西理念与理念谱系
- 新笔记挂载到这里（例如：你的笔记 —— 一句话简介）

## 约定与配置

- `templates/note-template.md` —— frontmatter 模板
- `<vault>/.dsh/skills/wiki-conventions/SKILL.md` —— agent 操作约定（源文件）
- `<vault>/.dsh/README.md` —— DSH 配置说明
- `<vault>/.wiki/README.md` —— agent 私有状态区说明

## 使用

- 启动 wiki 专用会话：`dsh --profile wiki web`
- 在 Obsidian 中打开 `<vault>` 作为 vault
