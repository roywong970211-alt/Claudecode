---
name: yt-research
description: Search YouTube and return structured metadata (title, URL, channel, duration, views, upload date) for a query. Use whenever the user asks to find, list, scrape, or research YouTube videos — for example "find the 25 latest trending videos on X", "get top YouTube videos about Y", or any request that needs a batch of YouTube URLs feeding into another tool.
---

# yt-research

Search YouTube via `yt-dlp` and emit a JSON list of video metadata. Built to feed the `notebooklm` skill (or any downstream pipeline).

## Tool

`~/.claude/skills/yt-research/search.py "<query>" [--limit N] [--sort latest|trending|relevance]`

- `--limit` defaults to 25.
- `--sort` defaults to `trending`. Use `latest` for newest-first, `relevance` for YouTube's default ranking.
- Output: JSON array on stdout. Each entry has `video_id`, `title`, `url`, `channel`, `duration_seconds`, `duration` (h:mm:ss or m:ss), `views`, `upload_date` (YYYYMMDD).

## When to use

- "Find the N latest/trending/top videos on TOPIC"
- "Scrape YouTube for videos about X"
- Any pipeline step that needs YouTube URLs.

If the user requests YouTube research without naming a topic, **ask** what topic before invoking the tool.

## Recipe — research command

1. Run `python3 ~/.claude/skills/yt-research/search.py "<topic>" --limit 25 --sort trending`.
2. Parse the JSON; keep the `url` field for sources.
3. Hand the URL list to the `notebooklm` skill.

## Notes

- `yt-dlp` is already installed system-wide.
- The script is read-only (no downloads). It only scrapes search-result metadata.
- For age-restricted or geo-blocked videos, some fields may be `null`; the URL will still work for NotebookLM ingestion.
