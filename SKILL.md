---
name: agent-expression
slug: agent-expression
displayName: Agent Expression
description: "本地表情包 Skill：按心情语义/关键词搜图、识图入库，只返回真实绝对路径（禁止瞎编路径或乱抽）。Cursor 用 open_resource 预览；Hermes 用 MEDIA:/path。"
version: 2.3.0
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
3. 发图 / 预览 → 先跑检索脚本（或宿主原生工具）；入库 → 用入库脚本。
4. 失败 → 只回文字。
5. 输出：**绝对路径**；再按宿主投递（见下）。**不要**默认输出 `MEDIA:`（仅 Hermes 等网关需要）。

### 按宿主投递

| 宿主 | 做法 |
|------|------|
| **Cursor** | 拿到绝对路径后，用 MCP `open_resource` 打开 `file:///<绝对路径>` 预览；**不要**用 `MEDIA:`；**不要**只丢路径指望聊天气泡出图。若路径不在工作区 / `~/.cursor` 被拒，先拷到工作区 `.meme-preview/` 再打开。详见 [references/hosts.md](references/hosts.md)。 |
| **Hermes** | `python3 scripts/search-meme.py "<query>" --pick --host hermes` → 正文 + 单独一行 `MEDIA:/abs/path` |
| **Codex** | `python3 scripts/search-meme.py "<query>" --pick --host codex` → stdout 一行 Markdown 图片（真实本地路径）；客户端不渲染时只回文字 |
| **自建 bot** | `send_image(path)` 或平台等价 API |
| **其它** | 有附件则附文件，否则回路径 / 纯文字 |

投递格式全文见 [references/hosts.md](references/hosts.md)。

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

推荐图包已内置：`packs/official-001/`（精简 starter：约 50 张常用标签图 + caption + embedding-3，路径为包内相对路径）。  
安装脚本会部署到 `$MEME_HOME/meme-packs/official-001/`。上游完整图源见包内 `CREDITS.md`。

## CLI（任意能跑 shell 的 Agent）

```bash
# 索引文件进 SQLite
python3 scripts/index-memes.py --sync-only

# 可选：视觉 caption / 向量（需 API）
python3 scripts/index-memes.py --workers 2
python3 scripts/embed-memes.py

# 检索：stdout 一行绝对路径（或按宿主格式化）
python3 scripts/search-meme.py "无语 摸鱼" --pick
python3 scripts/search-meme.py "无语" --pick --host codex   # Codex Markdown 图片
python3 scripts/search-meme.py "无语" --pick --host hermes  # MEDIA: 行
python3 scripts/search-meme.py "无语" --pick --json         # 结构化 JSON
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
