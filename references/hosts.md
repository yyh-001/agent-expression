# 宿主适配：Hermes · OpenClaw · Codex

本 Skill **主打** 三大平台；其它 Agent 只要能跑 shell、能发本地图，也可按同一契约接入。

核心契约：

1. 用脚本（或 `hermes-tools/`）拿到**真实存在的绝对路径**。
2. 不要手写路径、不要 `ls|shuf`。
3. 按宿主格式投递（见下）。

## 安装路径

| 平台 | 用户级 Skill 路径 | 安装 |
|------|-------------------|------|
| **Hermes** | `~/.hermes/skills/media/agent-expression/` | `install.sh --hermes` |
| **OpenClaw** | `~/.openclaw/skills/agent-expression/` | `openclaw skills install …` 或 `install.sh --openclaw` |
| **Codex** | `~/.codex/skills/…` 与 `~/.agents/skills/…` | `install.sh --codex` |
| **内容根** | `~/.agent-expression/skill/` | `install.sh` 真正 clone 的位置 |

项目级（`install.sh --project`）：`.agents/skills/agent-expression/`（Codex 跨工具）。

## Hermes

```bash
curl -fsSL …/install.sh | bash -s -- --hermes
python3 scripts/search-meme.py "无语" --pick --host hermes
```

- 正文 + 单独一行 `MEDIA:/abs/path`
- 可选原生工具：`hermes-tools/` → `search_meme` / `add_meme`
- 数据目录默认 `~/.hermes/meme-packs/`（与 `MEME_HOME` 兼容）

## OpenClaw（龙虾）

```bash
openclaw skills install @yyh-001/agent-expression
# 要预置图包：
openclaw skills install git:yyh-001/agent-expression@main
# 或 curl …/install.sh | bash
```

发图：

```text
path = subprocess(search-meme.py … --pick)
send_image(path)
```

装完**新开会话**。ClawHub / SkillHub 商店包不含 `packs/` 图片时需再拉 Git / 跑 `install.sh`。

## Codex

```bash
curl -fsSL …/install.sh | bash -s -- --codex
python3 scripts/search-meme.py "无语" --pick --host codex
```

- stdout 一行 `![alt](</abs/path>)`（真实本地路径）
- 机器可读：`--json`（含 `path` / `exists` / `retrieval_mode` 等）
- 客户端不渲染本地图 → 只回文字，不要假装已发图

## 输出约定

| 模式 | 命令 | stdout |
|------|------|--------|
| 默认 | `--pick` | 一行绝对路径 |
| Hermes | `--pick --host hermes` | `MEDIA:/abs/path` |
| Codex | `--pick --host codex` | Markdown 本地图 |
| 结构化 | `--pick --json` | JSON 对象 |

`MEDIA:` 是 Hermes 网关语法，不是通用协议。

## 其它平台

| 场景 | 做法 |
|------|------|
| **腾讯 SkillHub** | `skillhub install agent-expression --dir <skills目录>`；图包另跑 `install.sh` |
| **QQ / Telegram / 自建 bot** | `--pick` → `send_image(path)` |
| **Claude Code 等** | `--pick` → 附件或回路径；`install.sh --claude` 可单独链软链 |
| **纯文本 / 搜失败** | 只回文字 |

## Windows

| 方式 | 说明 |
|------|------|
| **推荐** | PowerShell：`irm …/install.ps1 \| iex` |
| 链接 | 目录联接 Junction；失败则复制 |
| Python | `python` 或 `py -3` |

## 数据目录

优先 `$MEME_PACK`；否则 `$MEME_HOME/meme-packs/$MEME_PACK_ID`。  
未设时：若已有 `~/.hermes/meme-packs/` 则沿用，否则 `~/.agent-expression`。  
兼容别名：`HERMES_HOME` / `HERMES_MEME_PACK*`。
