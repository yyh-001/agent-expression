---
name: agent-expression
description: Search and display real local meme or sticker files. Use when the user asks for a meme, reaction image, sticker, 表情包, 斗图, or when a light celebratory or playful response would benefit from one. Prefer no image for serious, sensitive, medical, legal, safety, or genuinely distressed contexts.
---

# Agent Expression

Use the bundled CLI to select a real file. Never invent a path and never choose files with `find`, `ls`, or random shell pipelines.

## Codex workflow

1. Resolve the skill root as the directory containing this `SKILL.md`.
2. Convert the intended reaction into a short Chinese mood or scene query.
3. Run:

```bash
python3 <skill-root>/scripts/search-meme.py "<query>" --pick --host codex
```

4. If the command succeeds, place its single Markdown image line after a concise textual reply. Do not wrap it in a code block.
5. If it fails or the client does not render the local image, reply with text only; do not claim an image was displayed.

For machine-readable output, run:

```bash
python3 <skill-root>/scripts/search-meme.py "<query>" --pick --json
```

The JSON result includes `path`, `mime_type`, `animated`, `tag`, `caption`, `retrieval_mode`, and `exists`.

## Selection rules

- Send for explicit requests, casual conversation, celebration, playful teasing, or light frustration.
- Do not send for serious help, conflict, grief, medical/legal/safety topics, or when confidence is low.
- Avoid sending another meme immediately after one was just used.
- Use only a result whose `exists` field is true.

## Other hosts

- Hermes: add `--host hermes` and paste the returned `MEDIA:` line.
- Path-only clients: use the default `--pick` output and pass the path to the host attachment API.
- Read [references/hosts.md](references/hosts.md) only when adapting another host.
