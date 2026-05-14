---
name: notebooklm
description: Drive NotebookLM via the unofficial notebooklm-py library — create a notebook, upload YouTube/web sources, request a synthesis (briefing doc, mind map, FAQ, audio overview), and optionally generate an infographic. Use whenever the user asks to "synthesize", "summarize a batch of sources", "feed these to NotebookLM", or follows up a `yt-research` run.
---

# notebooklm

Wraps the unofficial Python client for NotebookLM (https://github.com/teng-lin/notebooklm-py). The library is **unofficial** — Google has not blessed it and may change the underlying interface at any time. Treat failures as "the API drifted" rather than "the user did something wrong".

## Prerequisites

The user must have authenticated **once** in a fresh terminal:

```bash
notebooklm login
```

This opens a browser, the user signs in with Google, and a cookie/token is cached. If a call returns an auth error, ask the user to re-run `notebooklm login` — do NOT try to do it for them inside Claude Code.

## When to use

- "Send those videos to NotebookLM and give me the analysis"
- "Create a briefing doc / mind map / FAQ / audio overview from these sources"
- "Make an infographic in [style] from the synthesis"
- Any follow-up after the `yt-research` skill has populated `output/last_search.json`.

## How to invoke

```bash
python .claude/skills/notebooklm/scripts/run.py \
  --from .claude/skills/yt-research/output/last_search.json \
  --title "Cholesterol — expert synthesis" \
  --deliverables briefing,mind_map,infographic \
  --infographic-style "handwritten chalkboard" \
  --prompt "Synthesize agreements, disagreements, and concrete protocols across these experts."
```

### Arguments

| Flag | Notes |
|------|-------|
| `--from FILE` | JSON file from `yt-research` (or any file with a `videos[].url` list). |
| `--urls "u1,u2,..."` | Alternative to `--from` for ad-hoc URL lists. |
| `--title` | Notebook title shown in the NotebookLM UI. |
| `--prompt` | Instruction passed to NotebookLM for the briefing/analysis step. |
| `--deliverables` | Comma list of: `briefing`, `mind_map`, `faq`, `study_guide`, `timeline`, `audio_overview`, `infographic`. |
| `--infographic-style` | Free-text style hint (e.g. "handwritten chalkboard", "minimal flat", "magazine editorial"). |
| `--output-dir` | Where to save generated artifacts. Defaults to `.claude/skills/notebooklm/output/<timestamp>/`. |

## What the script does

1. Loads sources (from `--from` JSON or `--urls`).
2. Creates a new NotebookLM notebook with `--title`.
3. Uploads each URL as a source. Reports any that NotebookLM rejected (private/age-gated/unavailable).
4. Triggers each deliverable in `--deliverables`. Polls until ready.
5. Downloads artifacts into `--output-dir` and prints a summary table (artifact name → local path).
6. Prints the notebook share URL so the user can open it in the browser.

## Failure modes to surface clearly

- **Auth expired** → "Run `notebooklm login` in a fresh terminal, then re-run me."
- **Rate limit on artifacts** → "NotebookLM throttled artifact generation. Wait ~5 min and re-run with `--deliverables` set to only the missing ones."
- **Upstream API drift** (notebooklm-py raises an unexpected error) → Show the raw error and remind the user this is an unofficial client.
- **Some sources rejected** → Continue with the rest; list the rejected URLs at the end.

## Etiquette

- Don't auto-generate every deliverable. Default to `briefing` only; add `infographic` etc. when the user asks.
- Don't open the browser yourself; just print the share URL.
- Never log cookies or auth tokens.
