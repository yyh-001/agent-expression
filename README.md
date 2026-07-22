# agent-expression

本地表情包 Skill：为 [Hermes Agent](https://hermes-agent.nousresearch.com/)（及其它聊天 Agent）提供 **检索 → 发图 → 识图入库** 完整管线。

支持 FTS 关键词检索，以及可选的向量语义检索（智谱 `embedding-3`）。  
**本仓库不包含表情包图片**，请自备图包或使用开源素材。

[SKILL.md](./SKILL.md) · [MIT License](./LICENSE)

---

## Features

- **语义 / 关键词搜图**：口语化 query（如「想下班」「无语摸鱼」）→ 返回真实绝对路径
- **识图入库**：视觉自动分类到 `happy` / `shy` / `sigh`…，写 caption，并可嵌入向量
- **防瞎编路径**：约定只用脚本/工具输出的路径写 `MEDIA:`，禁止 `ls|shuf`
- **CLI 可独立跑**：不依赖 Hermes 也能索引与检索
- **可选 Hermes 原生工具**：`search_meme` / `add_meme`（见 [`hermes-tools/`](./hermes-tools/)）

## How it works

```text
meme-packs/<id>/memes/<tag>/*.png|gif
        │
        ▼
 index-memes.py  ──►  SQLite (caption + FTS5)
        │
        ▼
 embed-memes.py  ──►  meme_embeddings（可选）
        │
        ▼
 search-meme.py / search_meme  ──►  MEDIA:/abs/path
```

入库路径：`classify-and-add-meme.py` / `add_meme` → 写入文件 + 索引（+ 向量）。

## Directory layout

```text
agent-expression/
├── SKILL.md                 # Agent 行为约定（Hermes skill 入口）
├── README.md                # 本文件
├── LICENSE
├── .env.example
├── scripts/                 # CLI
│   ├── search-meme.py
│   ├── pick-meme.py
│   ├── add-meme.py
│   ├── classify-and-add-meme.py
│   ├── index-memes.py
│   ├── embed-memes.py
│   ├── meme_db.py
│   └── meme_embed.py
├── references/              # Schema / 标签说明
└── hermes-tools/            # 可选：Hermes 原生工具实现
```

## Requirements

| 用途 | 依赖 |
|------|------|
| 基础索引 / FTS 检索 | Python 3.10+、标准库 + 本地 SQLite |
| 向量检索（可选） | `numpy`；`ZHIPU_API_KEY`（智谱 embedding-3） |
| Caption / 自动分类（可选） | OpenAI 兼容视觉 API（如火山 Ark / OpenAI） |

密钥放在环境变量或 `${HERMES_HOME:-~/.hermes}/.env`，**不要提交到 Git**。参见 [`.env.example`](./.env.example)。

## Install

### Hermes（推荐）

```bash
hermes skills install yyh-001/agent-expression
# 或聊天里：/skills install yyh-001/agent-expression
```

安装后 skill 通常位于：

```text
~/.hermes/skills/media/agent-expression/
```

### 手动

```bash
git clone https://github.com/yyh-001/agent-expression.git \
  ~/.hermes/skills/media/agent-expression
```

## Prepare a meme pack

默认路径：

```text
~/.hermes/meme-packs/official-001/memes/<tag>/*.png|jpg|gif|webp
```

推荐开源包：[astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)

```bash
mkdir -p ~/.hermes/meme-packs/official-001
# 将上游仓库内容放到 official-001/，保证存在 memes/<tag>/ 结构
```

可用环境变量覆盖：

| 变量 | 说明 |
|------|------|
| `HERMES_HOME` | 默认 `~/.hermes` |
| `HERMES_MEME_PACK_ID` | 默认 `official-001` |
| `HERMES_MEME_PACK` | 直接指定 pack 根目录 |

标签说明见 [`references/categories.md`](./references/categories.md)。

## Quick start

```bash
cd ~/.hermes/skills/media/agent-expression   # 或本仓库根目录

# 1. 同步文件路径进 SQLite
python3 scripts/index-memes.py --sync-only

# 2. （可选）视觉打 caption —— 需要 vision API
python3 scripts/index-memes.py --workers 2

# 3. （可选）向量嵌入 —— 需要 ZHIPU_API_KEY
python3 scripts/embed-memes.py
python3 scripts/embed-memes.py --stats

# 4. 检索
python3 scripts/search-meme.py "无语 摸鱼" --pick -v
python3 scripts/search-meme.py "想下班" -n 5 -v
python3 scripts/pick-meme.py shy          # 按标签随机
python3 scripts/search-meme.py --stats
```

Agent 发图时只使用脚本 stdout 中的绝对路径：

```text
摸鱼被我逮到了吧
MEDIA:/absolute/path/to/meme.png
```

## Configuration

| 变量 | 用途 | 默认 |
|------|------|------|
| `ZHIPU_API_KEY` | 向量 embedding | （空则仅 FTS） |
| `ZHIPU_EMBEDDING_MODEL` | 模型名 | `embedding-3` |
| `ZHIPU_BASE_URL` | API 根路径 | `https://open.bigmodel.cn/api/paas/v4` |
| `ARK_API_KEY` / `OPENAI_API_KEY` | 视觉 caption / 分类 | — |

Hermes 用户也可在 `config.yaml` → `auxiliary.vision` 配置视觉端点。

## Agent rules（摘要）

完整约定见 **[SKILL.md](./SKILL.md)**。核心：

1. **禁止**手写 / 猜测 `MEDIA:` 路径  
2. **禁止** `ls|shuf|find` 自己挑图  
3. 发图 → `search-meme.py` / `search_meme`  
4. 入库 → `classify-and-add-meme.py` / `add_meme`  
5. 失败 → 只回文字  

```bash
# 入库示例
python3 scripts/classify-and-add-meme.py /path/or/url
python3 scripts/add-meme.py happy /path/or/url
```

## Optional: Hermes native tools

把检索/入库挂进模型工具列表（比 terminal 跑脚本更稳）：

1. Skill 装到 `~/.hermes/skills/media/agent-expression/`
2. 拷贝 `hermes-tools/*.py` → Hermes `tools/`
3. 在 `toolsets.py` 加入 `search_meme`、`add_meme`
4. 重启 gateway

细节：[hermes-tools/README.md](./hermes-tools/README.md)

## Pitfalls

| 现象 | 处理 |
|------|------|
| `search-meme` 报 index not found | 先跑 `index-memes.py --sync-only` |
| 向量不生效 / 仍走 FTS | 检查 `ZHIPU_API_KEY`，并跑 `embed-memes.py --stats` |
| caption 为空、检索很差 | 配置 vision API 后跑 `index-memes.py` |
| 手写路径被网关跳过 | 只用脚本返回的绝对路径；目录需含 `memes/` |
| 入库 `EXISTS` | 同内容已存在（hash 去重），可直接用返回路径 |

## Credits

- 表情包素材建议来源：[anka-afk/astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)（请遵守其许可）
- 面向 [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill 体系

## License

本仓库代码与文档为 [MIT](./LICENSE)。  
**图片素材版权归原作者 / 来源仓库**，本项目不附带、不授权图包内容。
