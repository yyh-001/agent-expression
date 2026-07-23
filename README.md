<p align="center">
  <img src="assets/cover.jpg" alt="表情包 Skill — agent-expression" width="100%" />
</p>

<p align="center">
  <strong>表情包 Agent Skill</strong> — 找得到、存得下、发得出
</p>

<p align="center">
  <a href="./SKILL.md"><img src="https://img.shields.io/badge/Skill-agent--expression-amber?style=flat-square" alt="Skill" /></a>
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-agent--expression-orange?style=flat-square" alt="ClawHub" /></a>
  <a href="https://www.skillhub.cn/"><img src="https://img.shields.io/badge/SkillHub-agent--expression-00a4ff?style=flat-square" alt="SkillHub" /></a>
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

本仓库是 **Skill + CLI + 精简预置图包**（`packs/official-001/`，约 **2.5MB / 52 张**，含 caption 与 embedding，开箱可搜）。完整上游包可自行扩容；图片版权见包内 `CREDITS.md`。

想顺便换一套聊天搭子人设？可另装人格 Skill **[suki](https://github.com/yyh-001/suki)**（本仓不含人设，两者独立、可选搭配）。

交流 / 反馈：**QQ 群 [993579665](https://qm.qq.com/q/7AD2g70HqS)**（[点击加入](https://qm.qq.com/q/7AD2g70HqS)）

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

### OpenClaw（龙虾）

[OpenClaw](https://docs.openclaw.ai/tools/skills) 推荐用内置 skills 命令或 [ClawHub](https://clawhub.ai) CLI。装完后**新开一轮会话**才会加载 Skill。

```bash
# ① 推荐：OpenClaw 从 ClawHub 安装
openclaw skills install @yyh-001/agent-expression
# 装到本机共用目录（多 agent 可见）：
openclaw skills install @yyh-001/agent-expression --global

# ② 等价：ClawHub CLI
npm i -g clawhub          # 若尚未安装
clawhub search agent-expression
clawhub install agent-expression

# ③ 要预置图包（约 2.5MB）时：从 Git 装整仓，或再跑一行安装脚本
openclaw skills install git:yyh-001/agent-expression@main
# 或：
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash
```

### 腾讯 SkillHub（国内）

国内商店：[skillhub.cn](https://www.skillhub.cn/)，可搜 `agent-expression`。

```bash
# 安装 CLI（仅 CLI）
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only

skillhub search agent-expression
skillhub install agent-expression --dir ~/.agents/skills   # 目录按你的 Agent 改
# OpenClaw 示例：
# skillhub install agent-expression --dir ~/.openclaw/skills
```

### 商店包 vs 完整图包

| 来源 | 有什么 | 搜图前还要做什么 |
|------|--------|------------------|
| **GitHub / `install.sh`** | Skill + 脚本 + 精简 `packs/`（约 2.5MB） | 一般可直接搜 |
| **ClawHub / OpenClaw `@yyh-001/…`** | Skill + 脚本 | 再跑 `install.sh`，或 `git:yyh-001/agent-expression@main` |
| **腾讯 SkillHub** | Skill + 脚本（平台不允许上传图片） | 同上，用 GitHub 拉图包 |

网页：[clawhub.ai](https://clawhub.ai) / [skillhub.cn](https://www.skillhub.cn/) 搜 `agent-expression`。

### Hermes

因仓库含预置图包，请用安装脚本（会链到 `~/.hermes/skills/media/agent-expression/`），**不要**只 `hermes skills install` 一个 `SKILL.md` URL（拉不全 `packs/`）。

```bash
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash -s -- --hermes
# 或：
git clone --depth 1 https://github.com/yyh-001/agent-expression.git \
  ~/.hermes/skills/media/agent-expression
```

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
# 安装脚本会把 packs/official-001（图 + index.db + 向量）拷到本地 meme-packs/
# 可直接搜，不必再识图 / 向量化：
python3 ~/.agent-expression/skill/scripts/search-meme.py "无语" --pick
# Windows：
#   py -3 %USERPROFILE%\.agent-expression\skill\scripts\search-meme.py "无语" --pick
```

### 在 Codex App 中验证

安装 Codex 目标并重新开启一个任务：

```bash
bash install.sh --codex
```

在新任务中输入「使用 agent-expression 给我一个无语的表情包」。Skill 会执行：

```bash
python3 ~/.codex/skills/agent-expression/scripts/search-meme.py \
  "无语" --pick --host codex
```

成功输出是一行引用真实本地文件的 Markdown 图片。结构化集成可以改用
`--json`；返回字段包括 `path`、`mime_type`、`animated`、`tag`、
`caption`、`retrieval_mode` 和 `exists`。Codex 客户端不渲染本地图片时，
Skill 会退回文字，不会假装已经发图。

只有你改了图或换了 embedding 模型时，才需要：

```bash
python3 …/scripts/index-memes.py --sync-only   # 或 --workers 做 caption
python3 …/scripts/embed-memes.py
```

Agent 拿到路径后交给宿主：

- **Cursor**：`open_resource(file:///绝对路径)` 在编辑器预览（不要 `MEDIA:`）
- **Hermes** 等网关：

```text
行吧你赢了
MEDIA:/abs/path/to/meme.jpg
```

详见 [references/hosts.md](./references/hosts.md)

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
| **OpenClaw（龙虾）** | `openclaw skills install @yyh-001/agent-expression`；要图包再 Git/`install.sh` → `send_image(path)` |
| **腾讯 SkillHub** | `skillhub install agent-expression --dir <skills目录>`；图包另用 GitHub/`install.sh` |
| Cursor | 用户级 skill 已链好；搜到图后 `open_resource(file:///…)` 预览，见 [hosts](./references/hosts.md) |
| Claude / Codex | 附件或回路径；对话里可提「发个表情包」 |
| [Hermes](https://github.com/NousResearch/hermes-agent) | 同上；可选 [`hermes-tools/`](./hermes-tools/) 原生工具 |
| 任意能跑 shell 的 Agent | 执行 `scripts/`，发返回的绝对路径 |
| 自建 bot | `subprocess(search-meme.py --pick)` → `send_image(path)` |
| 损友人设（可选） | 另装 [suki](https://github.com/yyh-001/suki)；不要把图包塞进人设仓 |

```text
agent-expression/
  SKILL.md         Agent 说明书（通用）
  scripts/         检索 · 索引 · 入库 · 嵌入
  packs/           预置图 + index.db + 向量
  hermes-tools/    可选 Hermes 适配
  references/      schema · 标签 · 宿主约定
  assets/cover.jpg
```

---

## License

- 代码与文档 [MIT](./LICENSE)。  
- 贡献者名单见 [CONTRIBUTORS.md](./CONTRIBUTORS.md)。  
- 预置图包来自 [astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)，详见 [`packs/official-001/CREDITS.md`](./packs/official-001/CREDITS.md)。
- 捆绑的 caption / embedding 仅方便开箱检索；更换模型请自行重跑脚本。
