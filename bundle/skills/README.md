# .dsh/skills/

wiki 系列 skills 的**源文件**（SKILL.md 形式），随 vault 版本化。

## 加载机制（重要）

DSH 的 skill 文件系统 provider 按等级发现根目录：

| 等级 | 根 | 可见范围 |
|---|---|---|
| 100 | `<projectRoot>/.dsh/skills`（本项目） | **仅工作目录为 <vault> 的会话** |
| 200 | `<projectRoot>/.agents/skills` | 仅该项目会话 |
| 300 | `customSkillDirs`（配置） | 按配置 |
| 400 | `~/.dsh/skills` | 全局 |
| 500 | `~/.agents/skills` | 全局 |

**本目录（rank 100）是最高优先级，且只对 wiki 会话可见——不污染全局。**
因此：**不要在 `~/.agents/skills/` 里放 wiki skills 的软链**（会让所有会话看到它们）。

## 启动前提

在 **`<vault>` 目录下**执行 `dsh --profile wiki web`，本目录 skills 自动被发现加载。
