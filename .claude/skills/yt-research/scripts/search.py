#!/usr/bin/env python3
"""YouTube search via yt-dlp. Emits JSON to stdout and persists to --output."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from yt_dlp import YoutubeDL
except ImportError:
    sys.stderr.write(
        "yt-dlp is not installed. Run: pip install --upgrade yt-dlp\n"
    )
    sys.exit(2)


SORT_PREFIX = {
    "relevance": "ytsearch",
    "date": "ytsearchdate",
    "views": "ytsearch",
}


def search(query: str, count: int, sort: str, min_duration: int) -> list[dict]:
    prefix = SORT_PREFIX.get(sort, "ytsearch")
    target = f"{prefix}{count * 3}:{query}" if sort == "views" else f"{prefix}{count}:{query}"

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "ignoreerrors": True,
    }

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(target, download=False) or {}

    entries = [e for e in (info.get("entries") or []) if e]
    videos = []
    for e in entries:
        duration = int(e.get("duration") or 0)
        if duration and duration < min_duration:
            continue
        upload_date = e.get("upload_date")
        if upload_date and len(upload_date) == 8:
            upload_date = f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        videos.append(
            {
                "title": e.get("title"),
                "channel": e.get("channel") or e.get("uploader"),
                "duration_seconds": duration,
                "view_count": int(e.get("view_count") or 0),
                "upload_date": upload_date,
                "url": e.get("url") or e.get("webpage_url"),
            }
        )

    if sort == "views":
        videos.sort(key=lambda v: v["view_count"], reverse=True)

    return videos[:count]


def merge_runs(output_dir: Path) -> dict:
    runs = sorted(output_dir.glob("run_*.json"))
    seen: dict[str, dict] = {}
    queries: list[str] = []
    for run in runs:
        data = json.loads(run.read_text())
        queries.append(data.get("query", ""))
        for v in data.get("videos", []):
            if v["url"] and v["url"] not in seen:
                seen[v["url"]] = v
    return {
        "query": " | ".join(q for q in queries if q),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(seen),
        "videos": list(seen.values()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query")
    ap.add_argument("--count", type=int, default=25)
    ap.add_argument("--sort", choices=list(SORT_PREFIX), default="relevance")
    ap.add_argument("--min-duration", type=int, default=0)
    ap.add_argument(
        "--output",
        default=".claude/skills/yt-research/output/last_search.json",
    )
    ap.add_argument("--merge", action="store_true", help="Merge prior run_*.json into last_search.json")
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.merge:
        payload = merge_runs(out_path.parent)
    else:
        if not args.query:
            sys.stderr.write("--query is required unless --merge is used\n")
            return 2
        videos = search(args.query, args.count, args.sort, args.min_duration)
        payload = {
            "query": args.query,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(videos),
            "videos": videos,
        }
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        (out_path.parent / f"run_{ts}.json").write_text(json.dumps(payload, indent=2))

    out_path.write_text(json.dumps(payload, indent=2))
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
