# dsh-wiki

基于 **DeepSeek Harness (DSH) + Obsidian** 的个人知识库体系（源自 [Karpathy LLM Knowledge Bases](https://community.tmpdir.org/t/llm-knowledge-bases/1685)）：LLM 负责编译与维护，人类负责选材、审核与提问。

**单一事实源 = Markdown vault（git 版本化）**，不引入数据库。

## 安装（官方 bundle 机制，推荐）

本仓库是一个 **DSH bundle**：`dsh plugin` 一条命令装进任意 profile。

```sh
# 方式 1：npm（推荐）
dsh plugin --profile <你的profile> add dsh-wiki

# 方式 2：GitHub（本仓库未发布 npm 前）
dsh plugin --profile <你的profile> add github:skillre/dsh-wiki

# 方式 3：本地 tarball（私有分发）
pnpm pack && dsh plugin --profile <你的profile> add ./dsh-wiki-0.1.0.tgz
```

验证安装（应看到 `# == dsh-wiki` 层）：

```sh
dsh --profile <你的profile> --dump-config
```

bundle 提供：**schedule 定时能力**（每周自动巡检/周报的前提）+ skills/scripts/templates 资源。

### 初始化你的 vault（一条命令，指定任意目录）

```sh
npx dsh-wiki-init ~/mywiki     # 初始化到 ~/mywiki（任意路径都行）
dsh-wiki-init                  # 省略路径 = 当前目录
```

命令把 5 个 wiki skills、巡检脚本（gen-index.py / maintain.py）、笔记模板复制到 `<vault>/.dsh/` 与 `<vault>/templates/`。
skills 通过 **project 级发现**（rank 100）只对该 vault 的会话可见——不污染全局；脚本自动定位 vault 根，零配置。

## 方式 2：模板 vault（clone 即用）

`vault-template/` 是完整的 vault 骨架 + 示例笔记：

```sh
cp -r vault-template my-wiki
```

Obsidian `Open folder as vault` 打开 → DSH GUI "选择工作区"添加 → 新建会话即获得：vault 沙箱围栏 + 5 个 wiki skills。

## 日常使用

```
① 丢：链接/PDF/一句话想法丢给 agent
② 审：agent 起草到 inbox/，你在 Obsidian 看
③ 过：说"通过" → 自动 promote 到 notes/ + 挂 MOC + git commit
④ 查：问"库里关于 X 说了什么？"
⑤ 养：说"跑一下巡检"；或让 agent 建每周提醒自动巡检+周报
```

## 包内容

```
package.json          dsh.bundle manifest
cordis.patch.yml      schedule 能力（每周提醒）
skills/               5 个 wiki skills（conventions/ingest/write/maintain/digest）
scripts/              gen-index.py + maintain.py（巡检 + L2 索引）
templates/            frontmatter 笔记模板
vault-template/       完整 vault 模板（含示例笔记）
```

## 设计要点

- 文件夹按生命周期分，不按主题分；主题结构由 `mocs/` + tags + `related` 承担
- 防冗余铁律：写之前先检索，已有就扩写不新建
- agent 只写 `inbox/` + `.wiki/`；正式区只读；每步 git commit 审计
- 维护自动化：脚本化巡检 + 周报 + schedule 每周提醒

## 许可

MIT。随意使用、修改、再分发。
