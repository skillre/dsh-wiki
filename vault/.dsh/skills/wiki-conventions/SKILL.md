---
name: wiki-conventions
description: 'Use when creating, editing, organizing, or maintaining notes in the Obsidian wiki vault at <vault> — defines the vault written contract (frontmatter schema, naming, wikilinks, MOC attachment, lifecycle, redundancy rules, write permissions, git commit discipline). All other wiki-* skills reference this contract.'
---

# Wiki Vault 约定（<vault>）

本 skill 是 vault 的"接口协议"。任何对 `<vault>` 的读改写都必须遵守；其他 wiki-* skills 以本文为准。

## 0. 权限边界（最重要）

- **可写**：`<vault>/inbox/`（新建草稿）、`<vault>/.wiki/`（索引与报告）、`<vault>/.dsh/`（配置）。
- **只读**：`notes/`、`mocs/`、`sources/`、`templates/`、`attachments/`——除非用户明确授权修改。
- 每次修改后必须 `git add -A && git commit`，message 说明"哪篇笔记、改了什么"（git 是唯一审计日志）。
- 修改前先 `git status` 确认目标文件没有未提交的人类改动（避免双写冲突）。

## 1. 目录结构

| 目录 | 作用 | 权限 |
|---|---|---|
| `inbox/` | agent 草稿区（status: draft） | agent 可写 |
| `notes/` | 正式笔记（published / evergreen） | agent 只读 |
| `mocs/` | MOC 主题导航（`MOC-主题.md`） | agent 只读 |
| `sources/` | 素材与引用（ingest 取料处） | agent 只读 |
| `templates/` | frontmatter 模板 | agent 只读 |
| `attachments/` | 二进制附件 | agent 只读 |
| `.wiki/` | 索引、巡检报告、中间草稿 | agent 可写 |
| `.dsh/` | DSH 配置 | agent 可写 |

**文件夹按生命周期分，不按主题分**：主题结构由 MOC + tags + related 链接承担，永远不需要重新规划文件夹。

## 2. 命名规范

- 文件名一律**英文 kebab-case slug**（如 `llm-knowledge-base.md`），中文标题放 frontmatter `title`。
- MOC 命名：`MOC-<英文slug>.md`（如 `MOC-Wiki-System.md`）。
- 禁止中文/空格/大写文件名（agent 生成 `[[wikilink]]` 时 ASCII 文件名零出错率）。

## 3. Frontmatter schema（强制）

```yaml
---
title: 中文标题
aliases: [别名]
tags: [全小写-kebab-case, 3-5个]
status: draft | published | evergreen | archived
mocs: ["[[MOC-XX]]"]
related: ["[[note-a]]", "[[note-b]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: 来源URL或出处
---
```

- `status`：draft（inbox）→ published（正式）→ evergreen（长期稳定）→ archived（废弃，不删除）。
- `mocs` 至少挂一个 MOC；`related` 写显式关联（双向：改 A 时同步补 B 的 related）。

## 4. 链接规范

- 一律 `[[wikilink]]`（按文件名解析）；带别名 `[[page|显示文本]]`。
- 新笔记至少 2 个出链（挂 MOC 算一个）。
- 不制造断链：链接目标必须是已存在文件，或明确标注"待创建"。

## 5. 防冗余铁律（写之前必做）

1. **先检索**：`grep`/`glob` 全库 + 读相关 MOC，确认没有已覆盖该主题的笔记。
2. 已有类似笔记 → **扩写它**（补章节、更新 related），绝不新建重复笔记。
3. 只有真正的新主题才新建文件，且必须挂 MOC。

## 6. 标签规范

- 全小写 kebab-case，英文优先，每篇 3-5 个。
- 例：`wiki`, `dsh`, `knowledge-management`, `ai-agent`。
- 不建同义标签（如 `ai` 与 `AI` 并存）。

## 7. 内容质量

- 首行 `> 一句话摘要`。
- 定义用引用块，结构用标题层级，关键信息加粗。
- 观点标注来源；不确定的内容标记"⚠️ 待验证"。
- 新草稿完成时自检：frontmatter 完整？≥2 出链？挂了 MOC？无断链？

## 8. 检索策略（wiki-search 使用）

- 本地优先：先 `grep` 标题/全文，再看 MOC 导航，最后读全文。
- 本地不足时才 `web_search` / `web_fetch` 兜底（结果作为 ingest 素材，不直接当结论）。
