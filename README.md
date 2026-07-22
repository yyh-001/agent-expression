<p align="center">
  <img src="assets/cover.jpg" alt="表情包 Skill — agent-expression" width="100%" />
</p>

<p align="center">
  <strong>让 Agent 看懂表情包：找得到、存得下、发得出。</strong>
</p>

<p align="center">
  <a href="./SKILL.md"><img src="https://img.shields.io/badge/Skill-agent--expression-amber?style=flat-square" alt="Skill" /></a>
  <img src="https://img.shields.io/badge/Host-agnostic-informational?style=flat-square" alt="Host agnostic" />
  <img src="https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="OS" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python" />
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT" /></a>
</p>

---

聊天 Agent 斗图最容易翻车的三件事：

- 手写假路径  
- `ls | shuf` 乱抽  
- 发完就忘，下次搜不到  

**agent-expression** 是一套本地表情包管线：索引 → 检索 → 只返回真实绝对路径。  
不绑定 Hermes / Cursor / 某一框架——只要能跑 shell、能发本地图，就能接。

本仓库是 **Skill + CLI**，不附带图片素材。

---

## 一行安装

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash
```

**Windows（PowerShell）**

```powershell
irm https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.ps1 | iex
```

需已安装 [Git for Windows](https://git-scm.com/download/win) 与 Python 3.10+（`python` / `py`）。

默认：**一份内容**装到 `~/.agent-expression/skill/`（Windows：`%USERPROFILE%\.agent-expression\skill\`），并链到主流 Agent / IDE：

| 路径 | 覆盖 |
|------|------|
| `~/.agents/skills/agent-expression` | 跨工具（Codex / Cursor 等） |
| `~/.cursor/skills/agent-expression` | Cursor |
| `~/.claude/skills/agent-expression` | Claude Code |
| `~/.codex/skills/agent-expression` | Codex 兼容路径 |
| `~/.hermes/skills/media/agent-expression` | 若已装 Hermes |

```bash
# macOS/Linux：当前仓库 / 单宿主
curl -fsSL …/install.sh | bash -s -- --project
curl -fsSL …/install.sh | bash -s -- --cursor
```

```powershell
# Windows
irm …/install.ps1 -OutFile $env:TEMP\ae-install.ps1
powershell -ExecutionPolicy Bypass -File $env:TEMP\ae-install.ps1 -Project
powershell -ExecutionPolicy Bypass -File $env:TEMP\ae-install.ps1 -Cursor
```

完整宿主说明（含 Windows）：[references/hosts.md](./references/hosts.md)

## 装完三步

```bash
# 1) 放图包到 memes/<tag>/
#    推荐：https://github.com/anka-afk/astrbot-meme-pack-official-01

# 2) 建索引（不用 API）—— Windows 可用 python / py -3
python3 ~/.agent-expression/skill/scripts/index-memes.py --sync-only
# Windows 示例：
#   py -3 %USERPROFILE%\.agent-expression\skill\scripts\index-memes.py --sync-only

# 3) 搜一张
python3 ~/.agent-expression/skill/scripts/search-meme.py "无语" --pick
```

Agent 拿到路径后交给宿主发图。例如支持 `MEDIA:` 的网关：

```text
行吧你赢了
MEDIA:/abs/path/to/meme.jpg
```

其它宿主怎么贴图 → [references/hosts.md](./references/hosts.md)

---

## 它做什么

| 能力 | 说明 |
|------|------|
| **语义搜图** | 口语 query；有向量更准，没有则 FTS 关键词 |
| **识图入库** | 用户丢来一张图 → 分类 + caption → 下次可搜 |
| **真实路径发出** | stdout 只出真实文件路径；禁止瞎编、禁止乱抽 |

可选加强（需要 API key，见 [.env.example](./.env.example)）：

```bash
python3 scripts/index-memes.py --workers 2   # 视觉写 caption
python3 scripts/embed-memes.py               # 向量检索
```

---

## 日常命令

```bash
python3 scripts/search-meme.py "想下班" --pick -v   # 检索
python3 scripts/pick-meme.py shy                    # 按标签随机
python3 scripts/classify-and-add-meme.py ./x.gif    # 识图入库
python3 scripts/add-meme.py happy ./x.gif           # 指定标签入库
```

数据根目录可用环境变量覆盖：`MEME_PACK` / `MEME_HOME` / `MEME_PACK_ID`（仍兼容 `HERMES_*`）。

---

## 给模型的三条铁律

完整约定在 [**SKILL.md**](./SKILL.md)。

1. 只用脚本（或宿主原生工具）返回的绝对路径  
2. 不手写路径，不 `ls|shuf|find` 自己挑图  
3. 搜失败就回文字，别硬发  

---

## 接到你的 Agent

一行安装后，Cursor / Claude Code / Codex / Hermes 等会自动发现同名 Skill。发图方式见 [hosts](./references/hosts.md)。

| 你在用 | 怎么接 |
|--------|--------|
| Cursor / Claude / Codex | 用户级 skill 已链好；对话里提「发个表情包」或 `/agent-expression` |
| [Hermes](https://github.com/NousResearch/hermes-agent) | 同上；可选 [`hermes-tools/`](./hermes-tools/) 原生工具 |
| 任意能跑 shell 的 Agent | 执行 `scripts/`，发返回的绝对路径 |
| 自建 bot | `subprocess(search-meme.py --pick)` → `send_image(path)` |

```text
agent-expression/
  SKILL.md         Agent 说明书（通用）
  scripts/         检索 · 索引 · 入库 · 嵌入
  hermes-tools/    可选 Hermes 适配
  references/      schema · 标签 · 宿主约定
  assets/cover.jpg
```

---

## License

代码与文档 [MIT](./LICENSE)。  
表情包版权归各自作者；推荐图包 [astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)。
