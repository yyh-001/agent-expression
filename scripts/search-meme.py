#!/usr/bin/env python3
"""Search local meme index by caption/keywords; print real absolute paths."""

from __future__ import annotations

import argparse
import importlib.util
import json
import mimetypes
import random
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mdb)

_core_spec = importlib.util.spec_from_file_location("search_core", _SCRIPTS / "search_core.py")
core = importlib.util.module_from_spec(_core_spec)
assert _core_spec.loader is not None
_core_spec.loader.exec_module(core)


def asset_payload(hit: dict, mode: str) -> dict:
    path = Path(hit["path"]).resolve()
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "path": str(path),
        "mime_type": mime,
        "animated": path.suffix.lower() in {".gif", ".webp"},
        "tag": hit.get("tag") or "",
        "caption": hit.get("caption") or "",
        "score": hit.get("score", 0),
        "retrieval_mode": mode,
        "exists": path.is_file(),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Search meme index. Prints absolute paths (use stdout for MEDIA:)."
    )
    p.add_argument("query", nargs="?", default="", help="Search text, e.g. 无语 摸鱼")
    p.add_argument("--pack", help="Meme pack root")
    p.add_argument("--tag", default="", help="Optional category filter, e.g. sigh")
    p.add_argument("-n", "--limit", type=int, default=5, help="Max results (default 5)")
    p.add_argument(
        "--pick",
        action="store_true",
        help="Print only one path (best match, or random among top hits)",
    )
    p.add_argument(
        "--random-among",
        type=int,
        default=3,
        help="With --pick, random among top K (default 3)",
    )
    p.add_argument("--verbose", "-v", action="store_true", help="Show caption/score")
    p.add_argument("--stats", action="store_true", help="Print index stats and exit")
    p.add_argument("--json", action="store_true", help="Print one structured JSON result")
    p.add_argument(
        "--host",
        choices=("path", "codex", "hermes"),
        default="path",
        help="Format one picked result for the target host",
    )
    p.add_argument("--no-vector", action="store_true", help="Force local FTS/tag search")
    args = p.parse_args(argv)

    pack_dir = Path(args.pack).expanduser() if args.pack else mdb.default_pack_dir()
    db_file = mdb.db_path_for_pack(pack_dir)
    if not db_file.is_file():
        print(
            f"ERROR: index not found: {db_file}\n"
            f"Run: python3 {_SCRIPTS}/index-memes.py --sync-only",
            file=sys.stderr,
        )
        return 1

    conn = mdb.connect(pack_dir)
    if args.stats:
        st = mdb.stats(conn)
        print(f"total={st['total']} captioned={st['captioned']}")
        for tag, c in st["by_tag"].items():
            print(f"{tag}\t{c}")
        conn.close()
        return 0

    if not (args.query or "").strip() and not (args.tag or "").strip():
        conn.close()
        print("ERROR: query or --tag required", file=sys.stderr)
        return 2

    conn.close()
    hits, mode = core.search_auto(
        pack_dir,
        args.query or "",
        tag=(args.tag or None),
        limit=max(args.limit, args.random_among),
        prefer_vector=not args.no_vector,
    )
    if not hits:
        # Fallback: if tag given, pick random from tag via filesystem via DB
        if args.tag:
            hits, mode = core.search_auto(
                pack_dir, "", tag=args.tag, limit=max(20, args.limit), prefer_vector=False
            )
            if hits:
                random.shuffle(hits)
                hits = hits[: args.limit]
        if not hits:
            print("ERROR: no matches", file=sys.stderr)
            return 1

    if args.pick or args.json or args.host != "path":
        pool = hits[: max(1, args.random_among)]
        chosen = pool[0] if mode == "vector" else random.choice(pool)
        payload = asset_payload(chosen, mode)
        if not payload["exists"]:
            print("ERROR: selected file is missing", file=sys.stderr)
            return 1
        if args.verbose:
            print(
                f"{chosen['path']}\t{chosen['tag']}\t{chosen['score']}\t{chosen['caption']}",
                file=sys.stderr,
            )
        if args.json:
            print(json.dumps(payload, ensure_ascii=False))
        elif args.host == "codex":
            alt = payload["caption"] or payload["tag"] or "本地表情包"
            print(f"![{alt}](<{payload['path']}>)")
        elif args.host == "hermes":
            print(f"MEDIA:{payload['path']}")
        else:
            print(payload["path"])
        return 0

    for h in hits[: args.limit]:
        if args.verbose:
            print(f"{h['path']}\t{h['tag']}\t{h['score']}\t{h['caption']}")
        else:
            # machine-friendly: path first, then tag + caption for the model
            print(f"{h['path']}\t{h['tag']}\t{h['caption']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
