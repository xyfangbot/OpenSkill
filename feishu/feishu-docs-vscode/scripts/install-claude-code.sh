#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills/claude-code/feishu-docs-vscode"
DEST="${CLAUDE_HOME:-$HOME/.claude}/skills/feishu-docs-vscode"

if [[ -e "$DEST" && "${1:-}" != "--force" ]]; then
  echo "Destination already exists: $DEST"
  echo "Run with --force to replace it."
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

echo "Installed Claude Code skill to $DEST"
echo "If Claude Code was already running before this directory existed, restart it."
