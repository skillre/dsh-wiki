# DSH Wiki — bundle 安装方式

把 wiki 体系装进**任意 DSH profile**（适合已有自己 profile 的用户，不想要"配置随库走"的模板 vault）。

## 安装

```sh
# 从本地目录安装（开发/分享前自测）
dsh plugin --profile <你的profile> add ./dsh-wiki

# 发布到 npm 后（或 GitHub git spec）
dsh plugin --profile <你的profile> add dsh-wiki
# 或
dsh plugin --profile <你的profile> add github:<你>/dsh-wiki
```

bundle 生效内容：**schedule 定时能力**（每周自动巡检/周报的前提）。安装后重启该 profile 的 dsh 实例即可。

## Skills 安装（bundle 不含注册，需要一步复制）

DSH 的 skills 是 SKILL.md 指令集，通过目录发现而非插件注册。把 skills 放进**你的 vault**：

```sh
# bundle 安装在 profile 的 node_modules 下：
# ~/.dsh/profiles/<你的profile>/node_modules/dsh-wiki/skills/
mkdir -p <你的vault>/.dsh/skills
cp -r ~/.dsh/profiles/<你的profile>/node_modules/dsh-wiki/skills/* <你的vault>/.dsh/skills/
```

放进 vault 的 `.dsh/skills/` 后，skills 通过 **project 级发现**（rank 100）只对该 vault 的会话可见——不污染全局。

## 脚本与模板

- `scripts/gen-index.py`、`scripts/maintain.py`：复制到 `<你的vault>/.dsh/scripts/`，用 `WIKI_VAULT` 环境变量指向你的 vault（默认 `~/wiki`）。
- `templates/note-template.md`：复制到 `<你的vault>/templates/`。

## 完整使用流程

1. 你的 vault 需要基础目录：`inbox/ notes/ mocs/ sources/ templates/ attachments/ .wiki/`（参考 kit 的 `vault/` 模板）。
2. Obsidian 打开 vault，DSH GUI 添加为工作区。
3. 在会话里让 agent 创建每周提醒："每周日跑 wiki-maintain 和 wiki-digest"。
