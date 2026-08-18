#!/usr/bin/env bash
# git-snapshot.sh — snapshot wiki content into a dedicated git repo for
# audit/backup, replacing obsidian-git when the vault lives on iCloud (no .git).
#
#   SRC  = this vault (auto-detected from script location: .dsh/scripts -> .dsh -> root)
#   DEST = $WIKI_REPO, else ~/wiki-repo
#
# Usage: sh .dsh/scripts/git-snapshot.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST="${WIKI_REPO:-$HOME/wiki-repo}"

[ -d "$SRC/.dsh" ] || { echo "error: not a wiki vault: $SRC"; exit 1; }

mkdir -p "$DEST"
echo "snapshot: $SRC -> $DEST"
rsync -a --delete --exclude=.git "$SRC/" "$DEST/"

cd "$DEST"
[ -d .git ] || git init -b main -q

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "snapshot $(date +%Y-%m-%dT%H:%M:%S)"
  echo "committed: $(date +%Y-%m-%dT%H:%M:%S)"
else
  echo "no changes since last snapshot"
fi

if git remote >/dev/null 2>&1 && [ -n "$(git remote)" ]; then
  git push -q && echo "pushed to $(git remote | head -1)"
else
  echo "no git remote — snapshot kept locally (set one: cd $DEST && git remote add origin <url>)"
fi
