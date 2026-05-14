# Claudecode — YouTube → NotebookLM research pipeline

Two Claude Code skills that turn a topic into a synthesized research brief built from 25 expert YouTube videos.

## What's here

- `.claude/skills/yt-research/` — scrapes YouTube via `yt-dlp` and writes a JSON list of videos.
- `.claude/skills/notebooklm/` — drives NotebookLM via the unofficial `notebooklm-py` client to create a notebook, upload sources, and request deliverables (briefing, mind map, infographic, audio overview).

Both are auto-discovered by Claude Code from their `SKILL.md` frontmatter.

## One-time setup

1. Install Python deps:

   ```bash
   pip install -r requirements.txt
   ```

2. Authenticate with NotebookLM in a **fresh** terminal (not inside Claude Code):

   ```bash
   notebooklm login
   ```

   A browser opens; sign in with Google. Token caches locally.

## Use it

In Claude Code:

> Use the yt-research skill to find the 25 latest trending videos on **[YOUR TOPIC]**. Send them to NotebookLM via the notebooklm skill, give me a synthesis of the top findings, then have NotebookLM generate an infographic in a handwritten / chalkboard style.

Claude will:
1. Run `python .claude/skills/yt-research/scripts/search.py --query "<topic>" --count 25` → writes `output/last_search.json`.
2. Run `python .claude/skills/notebooklm/scripts/run.py --from .claude/skills/yt-research/output/last_search.json --deliverables briefing,infographic --infographic-style "handwritten chalkboard"`.
3. Print the local artifact paths and the NotebookLM share URL.

## Caveats

- `notebooklm-py` is **unofficial**. Google can break it without warning. Re-run `notebooklm login` if you see auth errors.
- NotebookLM throttles artifact generation. If a deliverable fails, wait ~5 min and retry with only the missing ones.
- The `output/` folders are gitignored — artifacts and search dumps stay local.
