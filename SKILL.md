---
name: agent-expression
description: >
  Use when the agent should send or learn local meme/sticker images in chat.
  Search by mood/scene (vector + FTS), vision-classify ingest, emit MEDIA: paths only.
  Never invent paths or ls|shuf.
version: 2.0.0
author: yyh-001
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meme, expression, sticker, media, gif]
    category: media
---

# Agent Expression — 本地表情包 Skill

给聊天 Agent 用的本地表情包管线：索引、语义检索、识图入库，用真实绝对路径发 `MEDIA:`。

## 能力

| 能力 | 方式 |
|------|------|
| 按情绪/场景搜图 | `search-meme.py` 或 Hermes 原生 `search_meme` |
| 识图分类入库 | `classify-and-add-meme.py` / `add_meme` |
| Caption + 向量索引 | `index-memes.py` + `embed-memes.py` |
| 按标签随机 | `pick-meme.py <tag>` |

默认包路径：`${HERMES_HOME:-~/.hermes}/meme-packs/official-001/`  
（可用环境变量 `HERMES_MEME_PACK` / `HERMES_MEME_PACK_ID` 覆盖）

推荐公开包来源：[astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)（自行下载到 `meme-packs/<id>/memes/<tag>/`）。

## 硬规则（给模型）

1. **禁止手写 `MEDIA:` 路径**（不准猜文件名、不准漏 `memes/`）。
2. **禁止** `ls|shuf`、`find`、`search_files` 自己挑图。
3. 发图 → 先检索；入库 → 用入库脚本/工具。
4. 失败 → 只发文字。
5. 格式：正文 + 单独一行 `MEDIA:/绝对路径`（不要 `[image: MEDIA:…]`）。

## 快速开始

```bash
# 1) 准备表情包目录
mkdir -p ~/.hermes/meme-packs/official-001/memes

# 2) 同步文件进 SQLite，并用视觉打 caption（需配置 vision API）
python3 scripts/index-memes.py --sync-only
python3 scripts/index-memes.py --workers 3

# 3) （可选）向量检索：配置 ZHIPU_API_KEY 后嵌入
python3 scripts/embed-memes.py

# 4) 检索
python3 scripts/search-meme.py "无语 摸鱼" --pick
python3 scripts/search-meme.py "想下班" -n 5 -v
```

成功时 stdout 为一行绝对路径，直接：

```text
摸鱼被我逮到了吧
MEDIA:/absolute/path/to/meme.png
```

## 检索说明

1. **向量优先**（若已跑 `embed-memes.py`）：用 caption 的 embedding 做余弦相似，口语化 query 也能中。
2. **FTS/LIKE 降级**：关键词匹配 `caption` / `keywords` / `tag`。
3. 可选 `--tag happy` 限定分类。

环境变量（向量）：

```bash
export ZHIPU_API_KEY=...
export ZHIPU_EMBEDDING_MODEL=embedding-3   # 默认
export ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

视觉 caption/分类（`index-memes` / `classify-and-add`）读取 Hermes `auxiliary.vision` 或：

```bash
export ARK_API_KEY=...   # 或 OPENAI_API_KEY + 兼容 base_url
```

## 入库

```bash
# 自动识图分类 + 写入
python3 scripts/classify-and-add-meme.py /path/or/url

# 指定标签
python3 scripts/add-meme.py happy /path/or/url

# 新建分类
python3 scripts/add-meme.py my_tag /path/or/url --create --desc "自定义场景"
```

入库后建议：

```bash
python3 scripts/index-memes.py --limit 20   # 补 caption
python3 scripts/embed-memes.py              # 补向量
```

## Hermes 原生工具（可选）

本仓库 `hermes-tools/` 提供 `search_meme` / `add_meme` 工具实现。安装：

1. 将本 skill 放到 `~/.hermes/skills/media/agent-expression/`
2. 将 `hermes-tools/*.py` 拷到 Hermes 的 `tools/`，并在 `toolsets.py` 的核心工具列表加入 `search_meme`、`add_meme`
3. 重启 gateway

详见 [hermes-tools/README.md](hermes-tools/README.md)。

## 何时发 / 不发（建议）

发：闲聊、庆祝、吐槽、卖萌、用户要图。  
不发：真生气/求助/严肃；短时间刚发过本地表情；拿不准。

## 目录结构

```
agent-expression/
  SKILL.md
  README.md
  scripts/           # CLI：检索 / 索引 / 入库 / 嵌入
  references/        # schema、标签说明
  hermes-tools/      # 可选 Hermes 原生工具
```

## License

MIT。表情包图片版权归各自原作者；请遵守来源仓库许可，本 skill 不附带图包。
