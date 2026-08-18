---
name: wiki-git
description: 'Use when the user asks to commit, snapshot, back up, or push the wiki vault at <vault> — the vault lives on iCloud without a .git, so versioning happens in a dedicated repo (~/wiki-repo or $WIKI_REPO) via the git-snapshot.sh script.'
---

# wiki-git：快照与备份

vault 本体住在 iCloud（多端同步、无 `.git`），版本审计由独立 git 仓库承担。本 skill 定义如何执行提交/快照/推送。

## 触发

用户说：*"提交一下"*、*"做个快照"*、*"备份到 git"*、*"push"*。

## 执行

```sh
sh <vault>/.dsh/scripts/git-snapshot.sh
```

脚本做了什么：
1. 源 = 脚本所在 vault（自动定位）。
2. rsync（含新增/删除）到目标仓库：`$WIKI_REPO` 或 `~/wiki-repo`。
3. 有变更则 `git add -A && git commit`（message 带时间戳）。
4. 若配置了 remote 则 `git push`；否则只本地快照并提示。

## 边界

- 脚本只写目标仓库 `~/wiki-repo`，不动 iCloud vault 内容。
- 二进制（图片/PPT/zip）不跟踪（`.gitignore` 排除）——它们靠 iCloud 备份。
- 用户要真正 push 到远程时，需先给 `~/wiki-repo` 配 remote：
  ```sh
  cd ~/wiki-repo && git remote add origin git@github.com:<user>/wiki-backup.git
  ```
