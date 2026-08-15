#!/usr/bin/env python3
"""Generate .wiki/index.json for the wiki vault at ~/wiki.

Scans notes/, mocs/, inbox/ for *.md (excluding README.md), parses
frontmatter (title/aliases/tags/status/mocs/updated), extracts the summary
line (first "> " blockquote after frontmatter, else first paragraph), and
writes a JSON index used by wiki-maintain and L2 retrieval.

Usage: python3 ~/wiki/.dsh/scripts/gen-index.py
"""

import json
import os
import sys
from pathlib import Path

import yaml

VAULT = Path(os.environ.get("WIKI_VAULT", str(Path.home() / "wiki")))
INDEX = VAULT / ".wiki" / "index.json"
SECTIONS = ["notes", "mocs", "inbox"]
EXCLUDE = {"README.md"}


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        fm = yaml.safe_load(parts[1])
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError as exc:
        print(f"  [warn] bad frontmatter: {exc}", file=sys.stderr)
        return {}


def extract_summary(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("> "):
            return line[2:].strip()
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "---")):
            return line[:120]
    return ""


def main() -> int:
    entries = []
    for section in SECTIONS:
        root = VAULT / section
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if path.name in EXCLUDE:
                continue
            rel = path.relative_to(VAULT).as_posix()
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            body = text.split("---", 2)[2] if text.startswith("---") else text
            entries.append({
                "slug": path.stem,
                "path": rel,
                "section": section,
                "title": fm.get("title", path.stem),
                "aliases": fm.get("aliases", []),
                "tags": fm.get("tags", []),
                "status": fm.get("status", ""),
                "mocs": fm.get("mocs", []),
                "updated": str(fm.get("updated", "")),
                "summary": extract_summary(body),
            })
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(
        json.dumps({"generated": True, "count": len(entries), "entries": entries},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"indexed {len(entries)} notes -> {INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
