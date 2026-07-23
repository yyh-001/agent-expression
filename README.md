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
**主打 [Hermes](https://github.com/NousResearch/hermes-agent) · [OpenClaw](https://docs.openclaw.ai/tools/skills)（龙虾）· Codex**；其它能跑 shell 的 Agent 也能接。

本仓库是 **Skill + CLI + 精简预置图包**（`packs/official-001/`，约 **2.5MB / 52 张**，含 caption 与 embedding，开箱可搜）。完整上游包可自行扩容；图片版权见包内 `CREDITS.md`。

想顺便换一套聊天搭子人设？可另装人格 Skill **[suki](https://github.com/yyh-001/suki)**（本仓不含人设，两者独立、可选搭配）。

交流 / 反馈：**QQ 群 [993579665](https://qm.qq.com/q/7AD2g70HqS)**（[点击加入](https://qm.qq.com/q/7AD2g70HqS)）

---

## 推荐平台：Hermes · OpenClaw · Codex

| 平台 | 安装 | 发图 |
|------|------|------|
| **Hermes** | `curl …/install.sh \| bash -s -- --hermes` | `--host hermes` → `MEDIA:/abs/path`；可选 [`hermes-tools/`](./hermes-tools/) |
| **OpenClaw** | `openclaw skills install @yyh-001/agent-expression` + 图包见下 | `search-meme.py --pick` → `send_image(path)` |
| **Codex** | `curl …/install.sh \| bash -s -- --codex` | `--host codex` → Markdown 本地图；`--json` 结构化 |

OpenClaw / ClawHub / SkillHub 商店包**不含**完整图包；要开箱可搜请再跑 `install.sh` 或 `openclaw skills install git:yyh-001/agent-expression@main`。

### Hermes

因含预置图包，请用安装脚本链到 `~/.hermes/skills/media/agent-expression/`，**不要**只 `hermes skills install` 一个 `SKILL.md` URL。

```bash
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash -s -- --hermes
```

发图示例：

```text
行吧你赢了
MEDIA:/abs/path/to/meme.jpg
```

### OpenClaw（龙虾）

装完**新开一轮会话**才会加载 Skill。

```bash
openclaw skills install @yyh-001/agent-expression
openclaw skills install @yyh-001/agent-expression --global   # 本机共用

# 要预置图包（约 2.5MB）：
openclaw skills install git:yyh-001/agent-expression@main
# 或：
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash
```

### Codex

```bash
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash -s -- --codex
```

在新任务里让 Skill 执行：

```bash
python3 ~/.codex/skills/agent-expression/scripts/search-meme.py \
  "无语" --pick --host codex
```

成功时 stdout 为一行 `![alt](</abs/path>)`；机器可读用 `--json`。客户端不渲染本地图时只回文字。

---

## 一行安装（通用）

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash
```

**Windows（PowerShell）**

```powershell
irm https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.ps1 | iex
```

需已安装 [Git for Windows](https://git-scm.com/download/win) 与 Python 3.10+（`python` / `py`）。

默认 clone 到 `~/.agent-expression/skill/`，并链到上述三大平台路径（若目录已存在则一并链接 OpenClaw）：

| 路径 | 平台 |
|------|------|
| `~/.hermes/skills/media/agent-expression` | Hermes |
| `~/.openclaw/skills/agent-expression` | OpenClaw（若已装） |
| `~/.codex/skills/agent-expression` | Codex |
| `~/.agents/skills/agent-expression` | Codex 跨工具标准 |

```bash
curl -fsSL …/install.sh | bash -s -- --hermes    # 仅 Hermes
curl -fsSL …/install.sh | bash -s -- --codex     # 仅 Codex
curl -fsSL …/install.sh | bash -s -- --openclaw  # 仅 OpenClaw
```

完整约定：[references/hosts.md](./references/hosts.md)

### 国内分发（SkillHub / ClawHub）

| 来源 | 有什么 | 图包 |
|------|--------|------|
| **GitHub / `install.sh`** | Skill + 脚本 + 精简 `packs/`（约 2.5MB） | 已含 |
| **ClawHub / OpenClaw `@yyh-001/…`** | Skill + 脚本 | 再跑 `install.sh` 或 Git 装整仓 |
| **腾讯 SkillHub** | Skill + 脚本 | 同上 |

```bash
# SkillHub
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
skillhub install agent-expression --dir ~/.openclaw/skills   # 或 ~/.hermes/skills 等

# ClawHub
clawhub install agent-expression
```

网页：[clawhub.ai](https://clawhub.ai) / [skillhub.cn](https://www.skillhub.cn/) 搜 `agent-expression`。

## 装完即用

```bash
# 安装脚本会把 packs/official-001（图 + index.db + 向量）拷到本地 meme-packs/
python3 ~/.agent-expression/skill/scripts/search-meme.py "无语" --pick
# Hermes：加 --host hermes
# Codex：  加 --host codex
```

只有你改了图或换了 embedding 模型时，才需要：

```bash
python3 …/scripts/index-memes.py --sync-only
python3 …/scripts/embed-memes.py
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

| 平台 | 要点 |
|------|------|
| **[Hermes](https://github.com/NousResearch/hermes-agent)** | `install.sh --hermes`；`--host hermes` 或 `hermes-tools/` |
| **OpenClaw** | `@yyh-001/agent-expression`；图包用 Git / `install.sh` |
| **Codex** | `install.sh --codex`；`--host codex` / `--json` |
| 损友人设（可选） | 另装 [suki](https://github.com/yyh-001/suki) |
| 其它 / 自建 bot | `search-meme.py --pick` → 平台 `send_image` API |

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
