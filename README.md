<p align="center">
  <img src="assets/cover.jpg" alt="agent-expression — 表情包 Skill" width="920" />
</p>

<h1 align="center">agent-expression</h1>

<p align="center">
  <strong>让 Agent 会斗图。</strong><br/>
  本地表情包检索 · 识图入库 · 一键 <code>MEDIA:</code> 发出去
</p>

<p align="center">
  <a href="./SKILL.md"><img src="https://img.shields.io/badge/Hermes-Skill-amber?style=flat-square" alt="Hermes Skill" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT" /></a>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" alt="Python" />
</p>

---

聊天 Agent 最容易翻车的地方：瞎编图片路径、`ls|shuf` 乱抽、发不出去。

**agent-expression** 把表情包变成一条稳链路：

```text
搜得到 → 路径真 → MEDIA 发出去
学得会 → 识图分类 → 下次还能搜到
```

> 本仓库是 **Skill + 脚本**，不含表情包图片。图包请自备，或用开源包。

## 30 秒上手

```bash
# 1. 安装
hermes skills install yyh-001/agent-expression
# 或：git clone https://github.com/yyh-001/agent-expression.git ~/.hermes/skills/media/agent-expression

# 2. 放图包（示例开源包）
# https://github.com/anka-afk/astrbot-meme-pack-official-01
# → ~/.hermes/meme-packs/official-001/memes/<tag>/*

# 3. 索引 + 搜一张
cd ~/.hermes/skills/media/agent-expression
python3 scripts/index-memes.py --sync-only
python3 scripts/search-meme.py "无语" --pick
```

Agent 只贴返回路径：

```text
行吧你赢了
MEDIA:/abs/path/to/meme.png
```

## 它能干什么

| | |
|--|--|
| **搜图** | 「想下班」「得意傲娇」——关键词或语义（可选向量） |
| **入库** | 用户发来的图：识图分类 → caption → 可检索 |
| **防翻车** | 禁止手写路径，禁止 `ls\|shuf` |

可选：挂成 Hermes 原生工具 `search_meme` / `add_meme` → 见 [`hermes-tools/`](./hermes-tools/)。

## 一条命令对照

```bash
python3 scripts/search-meme.py "摸鱼" --pick -v     # 检索
python3 scripts/pick-meme.py shy                    # 按标签随机
python3 scripts/classify-and-add-meme.py ./x.gif    # 识图入库
python3 scripts/index-memes.py --workers 2          # 打 caption（需视觉 API）
python3 scripts/embed-memes.py                      # 向量化（需 ZHIPU_API_KEY）
```

## 配置（按需）

复制 [`.env.example`](./.env.example) 到 `~/.hermes/.env`：

| 你要什么 | 配什么 |
|----------|--------|
| 只关键词搜 | 不用 key，跑 `--sync-only` 即可 |
| 语义搜更准 | `ZHIPU_API_KEY` + `embed-memes.py` |
| 自动写描述 / 入库分类 | 视觉 API（`ARK_API_KEY` 或 OpenAI 兼容） |

图包路径可用 `HERMES_MEME_PACK` / `HERMES_MEME_PACK_ID` 覆盖。  
标签一览：[`references/categories.md`](./references/categories.md)

## Agent 三条铁律

完整约定在 [**SKILL.md**](./SKILL.md)。

1. 只用脚本/工具给出的绝对路径写 `MEDIA:`
2. 不手写路径，不 `ls|shuf|find`
3. 搜失败就回文字，别硬发

## 仓库结构

```text
SKILL.md          Agent 说明书
scripts/          CLI（检索 / 索引 / 入库 / 嵌入）
hermes-tools/     可选原生工具
references/       Schema & 标签
assets/cover.jpg  宣传图
```

## 常见问题

**搜不到？** 先 `index-memes.py --sync-only`；要语义再 `embed-memes.py`。  
**路径被跳过？** 必须是真实存在的绝对路径，且在 `memes/` 下。  
**入库显示 EXISTS？** 同图已存（hash 去重），直接用返回路径即可。

## License & Credits

- 代码 / 文档：[MIT](./LICENSE)
- 图包版权归素材来源，推荐 [astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01)
- 面向 [Hermes Agent](https://github.com/NousResearch/hermes-agent)
