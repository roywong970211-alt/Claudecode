---
name: notebooklm
description: Drive Google NotebookLM through the unofficial notebooklm-py CLI. Create notebooks, upload URLs (including YouTube) as sources, ask analytical questions, and generate deliverables (infographic, slide-deck, flashcards, mind-map, quiz, report, audio, video). Use whenever the user says "send to NotebookLM", "make a NotebookLM notebook", "generate an infographic/slides/flashcards from these sources", or pipes research output into NotebookLM.
---

# notebooklm

Wrapper around the `notebooklm` CLI (from `notebooklm-py`, PyPI). The CLI is already installed system-wide; the user must have run `notebooklm login` in a separate terminal at least once so that `~/.notebooklm/profiles/default/storage_state.json` exists.

## Tools

- `~/.claude/skills/notebooklm/run.sh <args...>` — passthrough to the `notebooklm` CLI for ad-hoc commands.
- `~/.claude/skills/notebooklm/pipeline.py --spec <json|->` — one-shot pipeline: create notebook → add sources → ask → generate artifacts.

### Pipeline spec

```json
{
  "title": "Trending claude-code videos — 2026-05-16",
  "sources": ["https://www.youtube.com/watch?v=..."],
  "ask": "Summarize the top findings across these videos.",
  "artifacts": [
    {
      "type": "infographic",
      "prompt": "Top findings, handwritten / chalkboard style.",
      "style": "sketch-note",
      "orientation": "landscape",
      "detail": "detailed",
      "download_to": "./infographic.png"
    }
  ]
}
```

`type` is any of: `infographic`, `slide-deck`, `flashcards`, `mind-map`, `quiz`, `report`, `data-table`, `audio`, `video`, `cinematic-video`.

`style` (infographic only): `auto | sketch-note | professional | bento-grid | editorial | instructional | bricks | clay | anime | kawaii | scientific`. **For "handwritten / chalkboard", use `sketch-note`** — it's the closest first-party style.

## Common one-liners

```bash
notebooklm login                                            # one-time, in a separate terminal
notebooklm list --json                                      # list notebooks
notebooklm create "My Notebook" --use --json                # create + set active
notebooklm source add "<url>" -n <nb_id> --json             # add YouTube URL (auto-detected)
notebooklm ask "What are the top findings?" -n <nb_id> --json
notebooklm generate infographic "..." --style sketch-note --wait -n <nb_id> --json
notebooklm download infographic ./out.png -n <nb_id> --latest --force
```

## Pipeline recipe

1. Build the spec dict (title + list of YouTube URLs + ask prompt + artifact prompts).
2. `echo "$SPEC_JSON" | python3 ~/.claude/skills/notebooklm/pipeline.py --spec -`
3. The script prints a JSON report with the notebook id, per-source upload status, the ask response, and per-artifact generation + download status.

## Pairing with `yt-research`

```bash
URLS_JSON=$(YT_RESEARCH_INSECURE=0 python3 ~/.claude/skills/yt-research/search.py "TOPIC" --limit 25 --sort trending)
SPEC=$(python3 -c '
import json, sys
videos = json.load(sys.stdin)
spec = {
  "title": "Trending TOPIC — research",
  "sources": [v["url"] for v in videos if v.get("url")],
  "ask": "Summarize the top findings across these videos.",
  "artifacts": [{
    "type": "infographic",
    "prompt": "Top findings depicted in a handwritten / chalkboard style.",
    "style": "sketch-note",
    "orientation": "landscape",
    "detail": "detailed",
    "download_to": "./infographic.png"
  }]
}
print(json.dumps(spec))
' <<<"$URLS_JSON")
echo "$SPEC" | python3 ~/.claude/skills/notebooklm/pipeline.py --spec -
```

## Authentication reminder

If any CLI call returns an auth error (`Not authenticated`, `storage_state.json missing`, 401/403), stop the pipeline and tell the user:

> Open a separate terminal and run `notebooklm login` to authenticate with your Google account. Re-run the command once that finishes.

## Topic clarification

If the user asks for the full research pipeline without specifying a topic, **ask** what topic to research before invoking either skill.
