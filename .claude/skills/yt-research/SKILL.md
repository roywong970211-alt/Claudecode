---
name: yt-research
description: Search YouTube for the top videos on a topic and return structured metadata (title, channel, duration, views, URL). Use whenever the user asks to "find videos", "research a topic on YouTube", or wants source URLs to feed into NotebookLM.
---

# yt-research

Scrapes YouTube search results via `yt-dlp` and returns a clean list of videos with metadata. Designed to feed the `notebooklm` skill, but can be used standalone.

## When to use

- "Find the 25 latest trending videos on [topic]"
- "Pull videos from [creator] about [topic]"
- "Get YouTube sources for [topic] so we can analyze them"

If the user asks for research without specifying a topic, ASK FIRST.

## How to invoke

Run the script via Bash. It writes JSON to stdout and also to `output/last_search.json` so the `notebooklm` skill can pick it up.

```bash
python .claude/skills/yt-research/scripts/search.py \
  --query "<search query>" \
  --count 25 \
  --sort relevance
```

### Arguments

| Flag        | Default     | Notes |
|-------------|-------------|-------|
| `--query`   | (required)  | Search string. For multi-creator topics, run once per creator and merge. |
| `--count`   | `25`        | Max results. |
| `--sort`    | `relevance` | One of `relevance`, `date`, `views`. `date` maps to yt-dlp `ytsearchdate`. |
| `--min-duration` | `0`    | Skip Shorts / clips by setting e.g. `300` (5 min). |
| `--output`  | `output/last_search.json` | Where to persist results. |

### Multi-creator pattern

When the user names several experts ("Huberman, Bryan Johnson, Peter Attia…"), run one search per creator and merge:

```bash
for name in "Andrew Huberman cholesterol" "Bryan Johnson cholesterol" "Peter Attia cholesterol"; do
  python .claude/skills/yt-research/scripts/search.py --query "$name" --count 8
done
python .claude/skills/yt-research/scripts/search.py --merge
```

## Output schema

```json
{
  "query": "cholesterol Peter Attia",
  "fetched_at": "2026-05-14T20:20:00Z",
  "count": 25,
  "videos": [
    {
      "title": "...",
      "channel": "...",
      "duration_seconds": 4123,
      "view_count": 482000,
      "upload_date": "2025-11-04",
      "url": "https://www.youtube.com/watch?v=..."
    }
  ]
}
```

## Handoff to notebooklm

After a successful search, suggest the next step:

> "Found 25 videos. Want me to send them to NotebookLM and generate a synthesis + infographic?"

Then invoke the `notebooklm` skill with `--from output/last_search.json`.
