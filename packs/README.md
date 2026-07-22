# Bundled meme pack

`official-001/` 是**精简 starter**（约 2.5MB / 50 张常用标签图），方便 clone / 安装：

| File | Purpose |
|------|---------|
| `memes/<tag>/*` | Sticker images（每标签约 4 张小图） |
| `index.db` | Captions + FTS + **embedding-3 vectors**（包内相对路径） |
| `manifest.json` | Category metadata |
| `CREDITS.md` | Upstream image credits |

Install scripts copy this pack to `$MEME_HOME/meme-packs/official-001/` when missing.
Scripts also fall back to this directory if no local pack is configured.

需要更多图时，可从上游 [astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01) 自行扩容后跑 `meme_db` / embedding 入库。
