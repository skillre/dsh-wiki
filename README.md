# DSH Wiki Kit

基于 **DeepSeek Harness (DSH) + Obsidian** 的个人知识库体系，源自 [Karpathy LLM Knowledge Bases](https://community.tmpdir.org/t/llm-knowledge-bases/1685) 理念：LLM 负责编译与维护，人类负责选材、审核与提问。

**单一事实源 = Markdown vault（git 版本化）**。不引入数据库，只靠文件系统 + 书面约定解耦。

## 包含什么

```
vault/                          ← 可移植的 Obsidian vault 模板
├── .dsh/
│   ├── skills/                 ← 5 个 wiki skills（project 级，仅本 vault 会话可见）
│   │   ├── wiki-conventions/   ← 书面约定：frontmatter/命名/链接/防冗余铁律
│   │   ├── wiki-ingest/        ← 素材 → 草稿（研究编译）
│   │   ├── wiki-write/         ← 扩写/新建 + promote（审核通过自动发布）
│   │   ├── wiki-maintain/      ← 巡检：断链/孤儿/重复/过期/MOC 平衡
│   │   └── wiki-digest/        ← 周报：变化汇总 + 可执行建议
│   └── scripts/
│       ├── gen-index.py        ← L2 检索索引生成（.wiki/index.json）
│       └── maintain.py         ← 健康检查脚本（产出 .wiki/reports/）
├── inbox/  notes/  mocs/  sources/  templates/  attachments/  .wiki/
└── notes/wiki-system-design.md ← 体系说明（示例笔记，可删）
```

## 快速开始（模板方式，推荐）

```sh
git clone <你的仓库地址> my-wiki
cd my-wiki
git init && git add -A && git commit -m "init from dsh-wiki-kit"   # 若 clone 已含 git 可跳过
```

1. **Obsidian**：`Open folder as vault` 打开 `my-wiki`；设置里把附件路径设为 `attachments`、新建文件位置设为 `inbox`（可选但推荐）。
2. **DSH**：在 Web GUI 点**"选择工作区"** → 添加 `my-wiki` → 选中 → 新建会话。该会话自动获得：
   - vault 沙箱围栏（agent 只能读写 vault 内）
   - 5 个 wiki skills（project 级发现，其他会话不可见）
3. **开用**：丢素材/链接给 agent → 它起草到 `inbox/` → 你看 → 说"通过" → 自动 promote 到 `notes/`。

脚本默认用 `~/wiki` 作为 vault；vault 在别处时：

```sh
export WIKI_VAULT=/path/to/my-wiki
python3 .dsh/scripts/gen-index.py
python3 .dsh/scripts/maintain.py
```

## 可选：DSH bundle 安装（适合已有 profile 的用户）

见 `bundle/README.md`——把 wiki 能力注册进任意 profile（含 schedule 定时能力）。

## 设计要点

- **文件夹按生命周期分，不按主题分**：主题结构由 `mocs/`（MOC 导航页）+ tags + `related` 链接承担，永不重新规划目录。
- **防冗余铁律**：写之前先检索，已有就扩写不新建。
- **人机分工**：agent 只写 `inbox/` + `.wiki/`；正式区只读；每步 git commit 审计。
- **维护自动化**：`wiki-maintain` 脚本化巡检 + `wiki-digest` 周报 + schedule 每周提醒。

## 许可

MIT。skills/scripts/模板随意使用、修改、再分发。
