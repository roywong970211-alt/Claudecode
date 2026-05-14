#!/usr/bin/env python3
"""Drive NotebookLM via the unofficial notebooklm-py client.

Layout chosen so failures localize: source loading, client init, upload,
deliverable generation, and download are independent stages with their
own error surfaces.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    import notebooklm  # type: ignore
except ImportError:
    sys.stderr.write(
        "notebooklm-py is not installed. Run: "
        "pip install git+https://github.com/teng-lin/notebooklm-py.git\n"
    )
    sys.exit(2)


DELIVERABLE_ALIASES = {
    "briefing": "briefing_doc",
    "briefing_doc": "briefing_doc",
    "mind_map": "mind_map",
    "mindmap": "mind_map",
    "faq": "faq",
    "study_guide": "study_guide",
    "timeline": "timeline",
    "audio_overview": "audio_overview",
    "infographic": "infographic",
}


def load_urls(args: argparse.Namespace) -> list[str]:
    if args.urls:
        return [u.strip() for u in args.urls.split(",") if u.strip()]
    if not args.from_:
        sys.stderr.write("Pass --from FILE or --urls 'u1,u2,...'\n")
        sys.exit(2)
    data = json.loads(Path(args.from_).read_text())
    return [v["url"] for v in data.get("videos", []) if v.get("url")]


def get_client() -> "notebooklm.Client":
    try:
        return notebooklm.Client()
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(
            f"Failed to init notebooklm client ({e}). "
            "Have you run `notebooklm login` in a fresh terminal?\n"
        )
        sys.exit(3)


def upload_sources(client, notebook, urls: Iterable[str]) -> tuple[list[str], list[tuple[str, str]]]:
    accepted, rejected = [], []
    for url in urls:
        try:
            client.add_source(notebook=notebook, url=url)
            accepted.append(url)
        except Exception as e:  # noqa: BLE001
            rejected.append((url, str(e)))
    return accepted, rejected


def generate_deliverable(client, notebook, kind: str, prompt: str | None, style: str | None):
    if kind == "infographic":
        return client.generate_infographic(notebook=notebook, style_hint=style or "")
    if kind == "audio_overview":
        return client.generate_audio_overview(notebook=notebook, prompt=prompt or "")
    if kind == "briefing_doc":
        return client.generate_briefing(notebook=notebook, prompt=prompt or "")
    return client.generate_artifact(notebook=notebook, kind=kind, prompt=prompt or "")


def wait_until_ready(client, artifact, timeout_s: int = 600, poll_s: int = 5):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status = client.get_artifact_status(artifact)
        if status in ("ready", "completed", "done"):
            return artifact
        if status in ("failed", "error"):
            raise RuntimeError(f"Artifact {artifact} failed: {status}")
        time.sleep(poll_s)
    raise TimeoutError(f"Artifact {artifact} did not finish within {timeout_s}s")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--urls")
    ap.add_argument("--title", default=f"Research {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--deliverables", default="briefing")
    ap.add_argument("--infographic-style", default="")
    ap.add_argument("--output-dir", default="")
    args = ap.parse_args()

    urls = load_urls(args)
    if not urls:
        sys.stderr.write("No source URLs provided.\n")
        return 2

    raw_kinds = [d.strip() for d in args.deliverables.split(",") if d.strip()]
    kinds = []
    for k in raw_kinds:
        if k not in DELIVERABLE_ALIASES:
            sys.stderr.write(f"Unknown deliverable '{k}'. Valid: {sorted(DELIVERABLE_ALIASES)}\n")
            return 2
        kinds.append(DELIVERABLE_ALIASES[k])

    out_dir = Path(
        args.output_dir
        or f".claude/skills/notebooklm/output/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    client = get_client()
    notebook = client.create_notebook(title=args.title)
    print(f"Created notebook: {args.title}")

    accepted, rejected = upload_sources(client, notebook, urls)
    print(f"Uploaded {len(accepted)}/{len(urls)} sources.")
    if rejected:
        print("Rejected sources:")
        for url, err in rejected:
            print(f"  - {url}: {err}")

    artifacts = []
    for kind in kinds:
        try:
            print(f"Generating {kind}...")
            art = generate_deliverable(client, notebook, kind, args.prompt, args.infographic_style)
            art = wait_until_ready(client, art)
            local = out_dir / f"{kind}{client.guess_extension(art) or ''}"
            client.download_artifact(art, dest=str(local))
            artifacts.append((kind, str(local)))
        except Exception as e:  # noqa: BLE001
            print(f"  ! {kind} failed: {e}")

    share_url = ""
    try:
        share_url = client.get_share_url(notebook)
    except Exception:  # noqa: BLE001
        pass

    summary = {
        "notebook_title": args.title,
        "share_url": share_url,
        "sources_uploaded": accepted,
        "sources_rejected": [u for u, _ in rejected],
        "artifacts": [{"kind": k, "path": p} for k, p in artifacts],
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    print("\n=== Summary ===")
    for k, p in artifacts:
        print(f"  {k}: {p}")
    if share_url:
        print(f"  notebook: {share_url}")
    print(f"  summary:  {out_dir / 'summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
