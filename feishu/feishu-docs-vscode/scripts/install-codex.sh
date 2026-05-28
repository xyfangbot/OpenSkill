#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills/codex/feishu-docs-vscode"
DEST="${CODEX_HOME:-$HOME/.codex}/skills/feishu-docs-vscode"

if [[ -e "$DEST" && "${1:-}" != "--force" ]]; then
  echo "Destination already exists: $DEST"
  echo "Run with --force to replace it."
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

echo "Installed Codex skill to $DEST"
echo "Restart Codex to pick up the new skill."
