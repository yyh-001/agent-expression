# 宿主适配（主流 Agent / IDE）

核心契约只有三条：

1. 用本 skill 的脚本（或等价工具）拿到**真实存在的绝对路径**。
2. 不要手写路径、不要 `ls|shuf`。
3. 把路径交给宿主的「发本地图 / 附件」能力。

一行安装默认会 **clone 一份 + 多宿主软链**，见根目录 `install.sh`。

## 输出约定

脚本成功时 **stdout 一行绝对路径**（`--pick`）。  
`MEDIA:/path` 只是部分聊天网关的投递语法，不是本 skill 协议。

## 安装路径一览

| 宿主 | 用户级 Skill 路径 | 说明 |
|------|-------------------|------|
| **跨工具标准** | `~/.agents/skills/agent-expression/` | Codex / Cursor 等都会扫 |
| **Cursor IDE** | `~/.cursor/skills/agent-expression/` | 也可扫 `.agents`、`.claude`、`.codex` |
| **Claude Code** | `~/.claude/skills/agent-expression/` | `/agent-expression` |
| **OpenAI Codex** | `~/.agents/skills/…` 与 `~/.codex/skills/…` | 后者为兼容路径 |
| **Hermes** | `~/.hermes/skills/media/agent-expression/` | 可选原生工具见 `hermes-tools/` |
| **规范内容根** | `~/.agent-expression/skill/` | 安装脚本真正 clone 的位置 |

项目级（`--project`）：

| 路径 |
|------|
| `.agents/skills/agent-expression/` |
| `.cursor/skills/agent-expression/` |
| `.claude/skills/agent-expression/` |

Cursor 还会自动发现 monorepo 子目录下的 `.cursor/skills/`。

## 按宿主怎么发图

### Cursor / Claude Code / Codex / VS Code 类 Agent

- 读 `SKILL.md`，执行 `scripts/search-meme.py … --pick`
- 对话支持附件时：把返回路径作为本地图片附上
- 不支持发图时：把路径写给用户，或只回文字

### Hermes

- 正文 + 单独一行 `MEDIA:/abs/path`
- 可选：`hermes-tools/` → `search_meme` / `add_meme`

### OpenClaw / QQ / Telegram / 自建 bot

```text
path = subprocess(search-meme.py … --pick)
send_image(path)
```

### 纯文本 / 无发图

搜失败或发不出去 → 只回文字。

## Windows

| 方式 | 说明 |
|------|------|
| **推荐** | PowerShell：`irm …/install.ps1 \| iex`（见 README） |
| 链接 | 优先 **目录联接 Junction**（一般无需管理员）；失败则整目录复制 |
| Python | `python` 或 `py -3`；脚本基于 `pathlib`，正反斜杠均可 |
| 临时目录 | `%TEMP%`（不再写死 `/tmp`） |
| Git Bash / WSL | 也可跑 `install.sh` |

## 数据目录

优先 `$MEME_PACK` / `%MEME_PACK%`；否则 `$MEME_HOME/meme-packs/$MEME_PACK_ID`。  
未设时：若已有 `~/.hermes/meme-packs/` 则沿用，否则 `~/.agent-expression`。

兼容别名：`HERMES_HOME` / `HERMES_MEME_PACK*`。