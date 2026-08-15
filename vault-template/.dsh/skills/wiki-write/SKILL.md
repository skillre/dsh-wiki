---
name: wiki-write
description: Use when expanding or creating wiki notes in the vault at <vault> — writes new notes per wiki-conventions, maintains bidirectional related links and MOC attachment, prefers extending existing notes over creating duplicates.
---

# wiki-write：扩写 / 新建笔记

对 vault 已有知识进行扩写、修正或新建。**先读 wiki-conventions（全部规则以它为准），再执行本流程。**

## 流程

### 1. 检索定位（必做）

- 确认目标笔记是否存在、内容现状如何；读相关 MOC 找邻居笔记。
- **已有类似笔记 → 扩写，绝不新建重复**（防冗余铁律）。

### 2. 决定操作

| 情况 | 操作 |
|---|---|
| 已有笔记需补充 | 扩写：补章节、更新 `updated`、补 related 双向链接 |
| 新主题 | 新建：挂 MOC、≥2 出链、相关邻居互链 |
| 内容过时/错误 | 修正并标注修改点；重大变更标记"⚠️ 已更新" |

### 3. 执行

- 扩写 `notes/` 已有笔记：仅在用户明确授权时可直接修改，否则把改写稿放 `inbox/` 供审核。
- 新建：一律写 `inbox/`（status: draft）。
- **双向链接纪律**：给 A 加 `related: [[B]]` 时，同步在 B 的 `related` 补上 `[[A]]`（或正文互链）。

### 4. 收尾

- `git add -A && git commit`，message 写清"write: <笔记名> +<新增内容摘要>"。
- 自检：frontmatter 完整？双向链接已补？MOC 挂载？无断链？摘要行存在？

### 5. Promote（用户审核通过后）

用户说"审核通过 / 这篇可以了 / promote"时，执行**机械 promote 流程**（用户只负责"看"，不手动移动文件或改字段）：

1. `git mv` 草稿：`inbox/<slug>.md` → `notes/<slug>.md`
2. frontmatter：`status: draft` → `published`（用户指定 evergreen 则改 evergreen）
3. 在 MOC 页（frontmatter `mocs` 指定的那个）对应小节补一行 `[[<slug>]] —— 一句话简介`
4. 若有 `related` 未互链的邻居，补双向链接
5. `git commit`，message："review: promote <slug> to notes (published)"

用户说"打回 / 要改"时：不改位置，按意见修改草稿后重新请用户看。
用户说"删了吧"时：`git rm` 删除草稿并 commit。
