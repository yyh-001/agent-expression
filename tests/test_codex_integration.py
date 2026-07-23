from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "search-meme.py"
PACK = ROOT / "packs" / "official-001"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--pack", str(PACK), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_codex_output_is_renderable_local_markdown():
    result = run_cli("无语", "--pick", "--host", "codex", "--no-vector")
    assert result.returncode == 0, result.stderr
    line = result.stdout.strip()
    assert line.startswith("![")
    assert "](<" in line and line.endswith(">)")
    path = Path(line.rsplit("(<", 1)[1][:-2])
    assert path.is_absolute() and path.is_file()


def test_json_contract_contains_existing_asset():
    result = run_cli("开心", "--pick", "--json", "--no-vector")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["exists"] is True
    assert Path(payload["path"]).is_file()
    assert payload["retrieval_mode"] == "fts"
    assert payload["mime_type"].startswith("image/")


def test_missing_query_is_a_safe_failure():
    result = run_cli("--pick")
    assert result.returncode == 2
    assert "query or --tag required" in result.stderr
