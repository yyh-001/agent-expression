---
name: agent-expression
description: >
  Local meme/sticker pack for chat agents: search by mood (vector+FTS),
  vision ingest, emit real absolute image paths only. Never invent paths or ls|shuf.
  Use when sending stickers/memes, learning user images into a pack, or wiring
  MEDIA:/path delivery on Hermes, Cursor, Claude Code, OpenClaw, or any shell-capable agent.
version: 2.1.0
author: yyh-001
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [meme, expression, sticker, media, gif]
  category: media
---

# Agent Expression

通用本地表情包 Skill：索引 → 检索 → 真实绝对路径发出。不绑定某一 Agent 运行时。

## 给模型的硬规则

1. **禁止手写图片路径**（不准猜文件名、不准漏 `memes/`）。
2. **禁止** `ls|shuf`、`find`、自己扫目录挑图。
3. 发图 → 先跑检索脚本（或宿主原生工具）；入库 → 用入库脚本。
4. 失败 → 只回文字。
5. 输出：**绝对路径**；宿主若支持 `MEDIA:`，正文后单独一行 `MEDIA:/abs/path`。

投递格式因宿主而异，见 [references/hosts.md](references/hosts.md)。

## 路径约定（通用）

```text
$MEME_HOME/meme-packs/<pack-id>/
  memes/<tag>/*.png|gif|…
  index.db
  manifest.json   # 可选
```

| 变量 | 作用 |
|------|------|
| `MEME_PACK` | 包根目录（最高优先） |
| `MEME_PACK_ID` | 默认 `official-001` |
| `MEME_HOME` / `AGENT_EXPRESSION_HOME` | 数据根；默认有 `~/.hermes/meme-packs` 则沿用，否则 `~/.agent-expression` |

兼容别名：`HERMES_MEME_PACK` / `HERMES_MEME_PACK_ID` / `HERMES_HOME`。

推荐图包：[astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01) → `memes/<tag>/`。

## CLI（任意能跑 shell 的 Agent）

```bash
# 索引文件进 SQLite
python3 scripts/index-memes.py --sync-only

# 可选：视觉 caption / 向量（需 API）
python3 scripts/index-memes.py --workers 2
python3 scripts/embed-memes.py

# 检索：stdout 一行绝对路径
python3 scripts/search-meme.py "无语 摸鱼" --pick
python3 scripts/pick-meme.py shy

# 入库
python3 scripts/classify-and-add-meme.py /path/or/url
python3 scripts/add-meme.py happy /path/or/url
```

Agent 用法示例：

```text
行吧你赢了
MEDIA:/absolute/path/to/meme.png
```

（无 `MEDIA:` 的宿主：把路径交给平台发图 API / 附件接口。）

## 检索

1. **向量优先**（已 `embed-memes.py`）：口语 query 更稳。
2. **FTS/LIKE 降级**：caption / keywords / tag。
3. 可选 `--tag sigh` 限分类。

## 配置

复制 [.env.example](.env.example) 到 `$MEME_HOME/.env`（或 skill 根目录 `.env`）：

| 需求 | 变量 |
|------|------|
| 仅关键词 | 无需 key，`--sync-only` 即可 |
| 语义检索 | `ZHIPU_API_KEY` 或 `EMBEDDING_API_KEY` |
| 识图入库 / caption | `VISION_API_KEY` / `OPENAI_API_KEY` / `ARK_API_KEY` + 可选 `VISION_BASE_URL` |

## 何时发

发：闲聊、庆祝、吐槽、用户要图。  
不发：真生气/求助/严肃；刚发过；拿不准。

## 宿主适配

一行安装默认多宿主链接（Cursor / Claude Code / Codex / Agents / Hermes）。

- 路径与发图约定（含 **Windows**）：[references/hosts.md](references/hosts.md)
- Windows：`install.ps1`；macOS/Linux：`install.sh`
- Hermes 可选原生工具：[hermes-tools/](hermes-tools/)
- 契约：脚本返回真实绝对路径；`MEDIA:` 仅部分网关需要。临时目录用系统 TEMP（跨平台）。

## License

MIT。图片版权归素材来源；本 skill 不附带图包。
