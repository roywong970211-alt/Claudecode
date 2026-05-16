#!/usr/bin/env bash
# Thin wrapper around the `notebooklm` CLI so the skill can be invoked
# uniformly. Exits with the CLI's status code and forwards all arguments.
set -euo pipefail
exec notebooklm "$@"
