#!/usr/bin/env python3
"""End-to-end NotebookLM pipeline: create notebook, add sources, ask, generate.

Reads a JSON spec from --spec PATH (or stdin). Spec shape:

  {
    "title": "Trending claude-code videos 2026-05-16",
    "sources": ["https://www.youtube.com/watch?v=...", ...],
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

Authentication: the caller must have run `notebooklm login` once in a
separate terminal so storage state exists at ~/.notebooklm/.

Prints a JSON report to stdout describing each step's outcome.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {shlex.join(cmd)}\n"
            f"stderr: {proc.stderr.strip()}"
        )
    return proc


def create_notebook(title: str) -> str:
    proc = run(["notebooklm", "create", title, "--use", "--json"])
    data = json.loads(proc.stdout)
    nb_id = data.get("id") or data.get("notebook_id") or data.get("notebookId")
    if not nb_id:
        raise RuntimeError(f"create returned no id: {proc.stdout}")
    return nb_id


def add_source(notebook_id: str, content: str) -> dict[str, Any]:
    proc = run(
        ["notebooklm", "source", "add", content, "-n", notebook_id, "--json"],
        check=False,
    )
    if proc.returncode != 0:
        return {"ok": False, "content": content, "error": proc.stderr.strip()}
    try:
        return {"ok": True, "content": content, "result": json.loads(proc.stdout)}
    except json.JSONDecodeError:
        return {"ok": True, "content": content, "raw": proc.stdout.strip()}


def ask(notebook_id: str, question: str) -> dict[str, Any]:
    proc = run(
        ["notebooklm", "ask", question, "-n", notebook_id, "--new", "--json"],
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"raw": proc.stdout}


def generate(notebook_id: str, artifact: dict[str, Any]) -> dict[str, Any]:
    a_type = artifact["type"]
    cmd = ["notebooklm", "generate", a_type, "-n", notebook_id, "--wait", "--json"]
    if "prompt" in artifact and artifact["prompt"]:
        cmd.append(artifact["prompt"])
    for flag in ("style", "orientation", "detail", "language"):
        if artifact.get(flag):
            cmd.extend([f"--{flag}", str(artifact[flag])])
    if artifact.get("timeout"):
        cmd.extend(["--timeout", str(artifact["timeout"])])

    proc = run(cmd)
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result = {"raw": proc.stdout}

    download_to = artifact.get("download_to")
    if download_to:
        dl_cmd = ["notebooklm", "download", a_type, download_to,
                  "-n", notebook_id, "--latest", "--force", "--json"]
        dl_proc = run(dl_cmd, check=False)
        result["download"] = {
            "path": download_to,
            "ok": dl_proc.returncode == 0,
            "stdout": dl_proc.stdout.strip(),
            "stderr": dl_proc.stderr.strip(),
        }
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--spec", default="-",
                   help="Path to JSON spec, or '-' for stdin (default).")
    args = p.parse_args()

    raw = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text()
    spec = json.loads(raw)

    report: dict[str, Any] = {"title": spec["title"]}
    nb_id = create_notebook(spec["title"])
    report["notebook_id"] = nb_id

    report["sources"] = [add_source(nb_id, s) for s in spec.get("sources", [])]

    if spec.get("ask"):
        report["ask"] = ask(nb_id, spec["ask"])

    report["artifacts"] = [generate(nb_id, a) for a in spec.get("artifacts", [])]

    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
