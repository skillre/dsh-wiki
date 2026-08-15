---
name: wiki-ingest
description: Use when turning research material (web articles, PDFs, PPTs, notes in sources/) into wiki notes in the vault at <vault> — compiles raw material into atomic note drafts following wiki-conventions, writes drafts to inbox/ only, and commits via git.
---

# wiki-ingest：素材 → 草稿

将 `sources/` 或网络素材编译为 wiki 草稿。**先读 wiki-conventions（全部规则以它为准），再执行本流程。**

## 流程

### 1. 防冗余检索（必做）

- `grep`/`glob` 全库确认是否已有覆盖该主题的笔记；读相关 MOC。
- 已覆盖 → 改走 wiki-write 扩写，不新建。

### 2. 读取素材

- 本地素材：读 `sources/` 下对应文件（PPT/docx 先用工具提取文本）。
- 网络素材：`web_search` 定位 → `web_fetch` 抓正文。保留来源 URL。
- 素材要点：按笔记需要提取事实、数据、观点，**不照搬原文**。

### 3. 影响分析（动笔前想清楚）

- 新建哪些页面？（首次出现的概念才新建）
- 需要更新哪些已有页面？（在草稿末尾列出，用户审核后执行）
- 新页面挂哪个 MOC？related 链向谁？

### 4. 起草（写进 `inbox/`）

- 遵守 conventions 的 frontmatter schema（`status: draft`、`mocs`、`related`）。
- 结构：一句话摘要 → 背景 → 核心内容 → 与现有知识的关系 → 待办/待验证 → 来源。
- 观点标注来源；不确定内容标"⚠️ 待验证"。
- 每篇草稿是一个原子主题，不把多个主题塞进一篇。

### 5. 收尾

- `git add -A && git commit`，message 写清"ingest: <素材名> → <草稿名>"。
- 自检清单：frontmatter 完整？≥2 出链？挂了 MOC？无断链？来源已注明？

## 注意

- 只写 `inbox/` 与 `.wiki/`；`notes/`、`mocs/`、`sources/` 只读（除非用户明确授权）。
- 草稿是"编译产物"，事实性错误由人工审核兜底——不确定处必须标注，不编造。
