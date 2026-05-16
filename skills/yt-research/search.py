#!/usr/bin/env python3
"""Search YouTube and return structured metadata.

Usage:
    search.py "query terms" [--limit N] [--sort latest|trending|relevance]

Outputs JSON to stdout: a list of {title, url, channel, duration_seconds,
duration, views, upload_date, video_id} objects.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from yt_dlp import YoutubeDL


SORT_TO_QUERY = {
    "relevance": "ytsearch{n}:{q}",
    "latest": "https://www.youtube.com/results?search_query={q}&sp=CAI%253D",
    "trending": "https://www.youtube.com/results?search_query={q}&sp=CAMSAhAB",
}


def _fmt_duration(seconds: int | float | None) -> str | None:
    if not seconds:
        return None
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def search(query: str, limit: int, sort: str) -> list[dict[str, Any]]:
    if sort == "relevance":
        target = SORT_TO_QUERY[sort].format(n=limit, q=query)
    else:
        target = SORT_TO_QUERY[sort].format(q=query.replace(" ", "+"))

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "playlistend": limit,
        "nocheckcertificate": os.environ.get("YT_RESEARCH_INSECURE") == "1",
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(target, download=False)

    entries = (info or {}).get("entries") or []
    results: list[dict[str, Any]] = []
    for e in entries[:limit]:
        if not e or e.get("_type") not in (None, "url", "video"):
            continue
        vid = e.get("id")
        results.append(
            {
                "video_id": vid,
                "title": e.get("title"),
                "url": e.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else None),
                "channel": e.get("channel") or e.get("uploader"),
                "duration_seconds": e.get("duration"),
                "duration": _fmt_duration(e.get("duration")),
                "views": e.get("view_count"),
                "upload_date": e.get("upload_date"),
            }
        )
    return results


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--sort", choices=list(SORT_TO_QUERY), default="trending")
    args = p.parse_args()

    try:
        results = search(args.query, args.limit, args.sort)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
