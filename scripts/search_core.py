#!/usr/bin/env python3
"""One search entry point shared by CLI and agent adapters."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def search_auto(
    pack_dir: Path,
    query: str,
    *,
    tag: str | None = None,
    limit: int = 5,
    prefer_vector: bool = True,
) -> tuple[list[dict[str, Any]], str]:
    """Return hits and retrieval mode; vector failures always degrade to FTS."""
    mdb = _load("agent_expression_meme_db", "meme_db.py")
    conn = mdb.connect(pack_dir)
    try:
        if prefer_vector and query.strip():
            try:
                emb = _load("agent_expression_meme_embed", "meme_embed.py")
                emb.ensure_embed_schema(conn)
                stats = emb.embed_stats(conn)
                if stats.get("embedded", 0) > 0 and emb.embed_config().get("api_key"):
                    hits = emb.search_vector(
                        conn,
                        query,
                        tag=tag or None,
                        limit=limit,
                    )
                    if hits:
                        return hits, "vector"
            except (ImportError, ModuleNotFoundError, RuntimeError, OSError, ValueError):
                pass

        hits = mdb.search(conn, query, tag=tag or None, limit=limit)
        return hits, "fts" if query.strip() else "tag"
    finally:
        conn.close()
