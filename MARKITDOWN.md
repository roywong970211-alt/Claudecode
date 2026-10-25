# MarkItDown in Claude Code

[MarkItDown](https://github.com/microsoft/markitdown) (by Microsoft) converts
PDF, Office documents (Word/PowerPoint/Excel), images, audio, HTML, CSV/JSON/XML,
ZIPs, EPubs, YouTube URLs and more into clean Markdown — ideal for feeding files
to an LLM.

This repo wires it into Claude Code two ways, both committed so they work in
local Claude Code **and** Claude Code on the web / cowork sessions.

## What's configured

| File | Purpose |
|------|---------|
| `.mcp.json` | Registers the **MarkItDown MCP server** so Claude gets a native `convert_to_markdown` tool. Runs via `uvx markitdown-mcp` (no manual install needed if `uv` is present). |
| `.claude/settings.json` | A `SessionStart` hook that installs `markitdown-mcp` and the `markitdown` CLI (`markitdown[all]`) into fresh/ephemeral web containers. |

## Using it

**As an MCP tool (inside Claude Code):** Claude can call the `convert_to_markdown`
tool from the `markitdown` server on any local path or URI (`file:`, `http:`,
`https:`, `data:`). In the terminal CLI, run `/mcp` to confirm the `markitdown`
server shows up as connected.

**As a CLI (in a shell):**
```bash
markitdown path/to/file.pdf > output.md     # convert a file
markitdown path/to/file.pdf -o output.md    # or write directly
cat file.docx | markitdown                  # via stdin
```

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) must be installed (it provides `uvx`).
  Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Local setup (your own machine)

The project-scoped `.mcp.json` is picked up automatically when you open this repo
in Claude Code — approve it when prompted (`claude mcp list` to verify). To make
MarkItDown available in **every** project, register it at the user level instead:

```bash
claude mcp add markitdown --scope user -- uvx markitdown-mcp
```

## Optional dependencies

`.claude/settings.json` installs `markitdown[all]` (all converters). To trim it,
install only the extras you need, e.g. `uv tool install 'markitdown[pdf,docx,pptx]'`.
Note: audio transcription also needs `ffmpeg` on the system.
