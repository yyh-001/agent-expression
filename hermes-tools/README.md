# Hermes 原生工具（可选）

把表情检索/入库提升为模型工具列表里的一等公民，避免 Agent 用 `terminal` + `ls|shuf` 绕开。

## 文件

| 文件 | 工具名 |
|------|--------|
| `search_meme_tool.py` | `search_meme` |
| `add_meme_tool.py` | `add_meme` |

两者通过 `HERMES_HOME/skills/media/agent-expression/scripts/` 加载 `meme_db.py` / `meme_embed.py` 等。

## 安装步骤

1. Skill 本体放到：

```bash
~/.hermes/skills/media/agent-expression/
# 内含 SKILL.md + scripts/ + references/
```

2. 拷贝工具到 Hermes agent：

```bash
cp hermes-tools/search_meme_tool.py /path/to/hermes-agent/tools/
cp hermes-tools/add_meme_tool.py    /path/to/hermes-agent/tools/
```

3. 在 `toolsets.py` 的 `_HERMES_CORE_TOOLS`（或你的平台 toolset）加入：

```python
"search_meme", "add_meme",
```

并可选增加：

```python
"meme": {
    "description": "Local meme search + ingest",
    "tools": ["search_meme", "add_meme"],
    "includes": [],
},
```

4. 重启 gateway / agent 进程。

## 工具参数摘要

**search_meme**

- `query`：情绪/场景（支持口语，有向量时更稳）
- `tag`：可选分类过滤
- `pick`：默认 true，返回一条 `media_tag`

**add_meme**

- `image_path`：本地缓存路径或 URL
- `tag`：可选强制分类
- `dry_run`：只分类不写入
- `caption`：默认 true，入库时写 caption + 向量

## 注意

- 不要把 API Key 写进工具代码；用 `~/.hermes/.env`
- 本目录工具依赖本 skill 的 `scripts/`，请保持相对安装路径一致
