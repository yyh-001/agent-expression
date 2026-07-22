# agent-expression

本地表情包 Skill：给 Hermes / 其它 Agent 用的 **检索 + 识图入库 +（可选）向量语义搜**。

- 脚本可独立跑（CLI）
- 可选挂载为 Hermes 原生工具 `search_meme` / `add_meme`
- **不包含**表情包图片本体（请自备或使用开源包）

## 安装（CLI）

```bash
git clone <this-repo> ~/.hermes/skills/media/agent-expression
# 或软链
ln -s /path/to/agent-expression ~/.hermes/skills/media/agent-expression
```

准备图包目录（示例）：

```bash
mkdir -p ~/.hermes/meme-packs/official-001
# 将 memes/<tag>/*.png|jpg|gif 放进去
# 推荐来源：https://github.com/anka-afk/astrbot-meme-pack-official-01
```

索引与检索：

```bash
cd ~/.hermes/skills/media/agent-expression
python3 scripts/index-memes.py --sync-only
python3 scripts/index-memes.py --workers 2          # 需 vision API
python3 scripts/embed-memes.py                       # 可选，需 ZHIPU_API_KEY
python3 scripts/search-meme.py "无语" --pick -v
```

## 环境变量

| 变量 | 用途 |
|------|------|
| `HERMES_HOME` | 默认 `~/.hermes` |
| `HERMES_MEME_PACK` / `HERMES_MEME_PACK_ID` | 指定表情包根目录 |
| `ARK_API_KEY` / `OPENAI_API_KEY` | 视觉 caption / 分类 |
| `ZHIPU_API_KEY` | embedding-3 向量检索 |
| `ZHIPU_EMBEDDING_MODEL` | 默认 `embedding-3` |
| `ZHIPU_BASE_URL` | 默认智谱开放平台 |

密钥放在 `~/.hermes/.env` 或环境变量，**不要提交到 Git**。

## Agent 用法摘要

完整约定见 [SKILL.md](./SKILL.md)。核心：

```text
# 发图
search-meme.py "得意傲娇" --pick
→ MEDIA:/abs/path.png

# 入库
classify-and-add-meme.py /path/to/user.gif
```

禁止手写路径、禁止 `ls|shuf` 抽图。

## Hermes 原生工具

见 [hermes-tools/README.md](./hermes-tools/README.md)。

## License

MIT（代码与文档）。图片素材版权独立，请遵循来源许可。
