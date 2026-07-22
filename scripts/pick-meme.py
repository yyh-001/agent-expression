#!/usr/bin/env python3
"""Pick a random local meme image from an installed meme pack."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def default_pack_dir() -> Path:
    override = os.environ.get("HERMES_MEME_PACK", "").strip()
    if override:
        return Path(override).expanduser()
    home = Path(os.environ.get("HERMES_HOME", "~/.hermes")).expanduser()
    pack_id = os.environ.get("HERMES_MEME_PACK_ID", "official-001").strip() or "official-001"
    return home / "meme-packs" / pack_id


def load_manifest(pack_dir: Path) -> dict:
    manifest_path = pack_dir / "manifest.json"
    if not manifest_path.is_file():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8-sig"))


def list_images(category_dir: Path) -> list[Path]:
    if not category_dir.is_dir():
        return []
    return sorted(
        path
        for path in category_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    )


def cmd_list(pack_dir: Path) -> int:
    if not pack_dir.is_dir():
        print(f"ERROR: pack directory not found: {pack_dir}", file=sys.stderr)
        return 1

    manifest = load_manifest(pack_dir)
    categories = manifest.get("categories", {})
    memes_root = pack_dir / "memes"
    names = sorted(categories.keys()) if categories else sorted(
        p.name for p in memes_root.iterdir() if p.is_dir()
    )
    for name in names:
        meta = categories.get(name, {})
        desc = meta.get("description", "") if isinstance(meta, dict) else str(meta)
        count = len(list_images(memes_root / name))
        print(f"{name}\t{count}\t{desc}")
    return 0


def cmd_pick(pack_dir: Path, tag: str) -> int:
    tag = tag.strip()
    if not tag:
        print("ERROR: tag is required", file=sys.stderr)
        return 1
    if not pack_dir.is_dir():
        print(f"ERROR: pack directory not found: {pack_dir}", file=sys.stderr)
        return 1

    category_dir = pack_dir / "memes" / tag
    images = list_images(category_dir)
    if not images:
        print(f"ERROR: no images for tag '{tag}' under {category_dir}", file=sys.stderr)
        return 1

    print(images[random.randrange(len(images))].resolve())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List or pick local meme pack images.")
    parser.add_argument(
        "--pack",
        help="Meme pack root (default: $HERMES_MEME_PACK or ~/.hermes/meme-packs/official-001)",
    )
    parser.add_argument("--list", action="store_true", help="List available tags.")
    parser.add_argument("tag", nargs="?", help="Category tag to pick from, e.g. happy.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pack_dir = Path(args.pack).expanduser() if args.pack else default_pack_dir()

    if args.list:
        return cmd_list(pack_dir)
    if args.tag:
        return cmd_pick(pack_dir, args.tag)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
