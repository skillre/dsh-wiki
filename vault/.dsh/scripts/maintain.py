#!/usr/bin/env python3
"""Wiki health check: broken links, orphans, duplicate candidates, stale
notes, MOC balance, pending drafts. Writes reports to ~/wiki/.wiki/reports/.

Usage: python3 ~/wiki/.dsh/scripts/maintain.py [--stale-months N]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

VAULT = Path(os.environ.get("WIKI_VAULT", str(Path.home() / "wiki")))
REPORTS = VAULT / ".wiki" / "reports"
INDEX = VAULT / ".wiki" / "index.json"
SECTIONS = ["notes", "mocs", "inbox"]
EXCLUDE = {"README.md"}
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
TEMPLATE_PLACEHOLDERS = {"MOC-XX", "MOC-主题", "note-a", "note-b", "page",
                         "相关笔记1", "相关笔记2", "wikilink", "双向链接",
                         "wiki-conventions"}


def load_index():
    if not INDEX.exists():
        print(f"error: {INDEX} missing; run gen-index.py first", file=sys.stderr)
        sys.exit(1)
    return json.loads(INDEX.read_text(encoding="utf-8"))["entries"]


def all_md():
    for section in SECTIONS:
        root = VAULT / section
        if root.is_dir():
            for p in sorted(root.rglob("*.md")):
                if p.name not in EXCLUDE:
                    yield section, p


def parse_date(s: str):
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(str(s)[:16], fmt).date()
        except ValueError:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-months", type=int, default=6)
    args = ap.parse_args()

    index = load_index()
    by_slug = {e["slug"]: e for e in index}

    # Collect every wikilink target and every file's inlinks.
    links = defaultdict(list)      # slug -> [targets]
    inlinks = defaultdict(int)     # target slug -> count
    for section, path in all_md():
        text = path.read_text(encoding="utf-8")
        targets = []
        for m in WIKILINK.finditer(text):
            t = m.group(1).strip()
            if t in TEMPLATE_PLACEHOLDERS:
                continue
            targets.append(t)
            inlinks[t] += 1
        links[path.stem] = targets

    broken = []
    for src, targets in links.items():
        for t in targets:
            if t not in by_slug:
                broken.append((src, t))

    orphans = [s for s, e in by_slug.items()
               if e["section"] in ("notes", "mocs") and inlinks.get(s, 0) == 0]

    today = date.today()
    stale = []
    for s, e in by_slug.items():
        if e["status"] not in ("published", "evergreen"):
            continue
        d = parse_date(e.get("updated", ""))
        if d and (today - d).days > args.stale_months * 30:
            stale.append((s, str(d)))

    mocs = defaultdict(int)
    for s, e in by_slug.items():
        for m in e.get("mocs", []):
            m = re.sub(r"^\[\[|\]\]$", "", str(m))
            mocs[m] += 1

    drafts = [e for e in by_slug.values() if e["section"] == "inbox"]

    # Duplicate candidates: same normalized title stem or heavy tag overlap.
    # Pairs already linked to each other are parent/child or sibling notes,
    # not duplicates.
    tag_sets = {s: set(e.get("tags", [])) for s, e in by_slug.items()}
    slugs = list(by_slug)
    dupes = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            a, b = slugs[i], slugs[j]
            if by_slug[a]["section"] == by_slug[b]["section"] == "inbox":
                continue
            if b in links[a] or a in links[b]:
                continue
            shared = tag_sets[a] & tag_sets[b]
            if len(shared) >= 3 or (len(shared) >= 2 and a.split("-")[0] == b.split("-")[0]):
                dupes.append((a, b, sorted(shared)))

    REPORTS.mkdir(parents=True, exist_ok=True)

    def write(name, lines):
        (REPORTS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")

    write("links.md", ["# 断链报告",
                       f"共 {len(broken)} 处断链",
                       "",
                       *[f"- [[{s}]] → [[{t}]]（目标不存在）" for s, t in broken]])
    write("orphans.md", ["# 孤儿笔记（无入链）",
                         f"共 {len(orphans)} 篇",
                         "",
                         *[f"- [[{s}]]" for s in orphans]])
    write("duplicates.md", ["# 重复候选",
                             f"共 {len(dupes)} 组",
                             "",
                             *[f"- [[{a}]] ↔ [[{b}]]（共同标签: {', '.join(t)}）"
                               for a, b, t in dupes]])
    write("stale.md", ["# 过期内容（updated 超 %d 个月）" % args.stale_months,
                       f"共 {len(stale)} 篇",
                       "",
                       *[f"- [[{s}]]（{d}）" for s, d in stale]])
    write("mocs.md", ["# MOC 挂载统计",
                       "",
                       *[f"- {m}: {n} 篇" + ("（>30，建议拆分）" if n > 30 else
                                           "（空 MOC，建议废弃）" if n == 0 else "")
                         for m, n in sorted(mocs.items(), key=lambda x: -x[1])]])
    write("inbox.md", ["# 待审草稿",
                       f"共 {len(drafts)} 篇",
                       "",
                       *[f"- [[{d['slug']}]]（{d.get('updated', '')}）" for d in drafts]])

    summary = [
        "# Wiki 巡检汇总 — %s" % today.isoformat(),
        "",
        "| 指标 | 数量 |",
        "|---|---|",
        f"| 笔记总数 | {len(by_slug)} |",
        f"| 断链 | {len(broken)} |",
        f"| 孤儿笔记 | {len(orphans)} |",
        f"| 重复候选 | {len(dupes)} |",
        f"| 过期内容 | {len(stale)} |",
        f"| 待审草稿 | {len(drafts)} |",
        "",
        "## 优先行动项",
    ]
    actions = []
    if broken:
        actions.append(f"1. 修复 {len(broken)} 处断链（见 links.md）")
    if orphans:
        actions.append(f"{len(actions) + 1}. 为 {len(orphans)} 篇孤儿笔记补链（见 orphans.md）")
    if dupes:
        actions.append(f"{len(actions) + 1}. 评估 {len(dupes)} 组重复候选（见 duplicates.md）")
    if stale:
        actions.append(f"{len(actions) + 1}. 回顾 {len(stale)} 篇过期内容（见 stale.md）")
    if drafts:
        actions.append(f"{len(actions) + 1}. 审核 {len(drafts)} 篇待审草稿（见 inbox.md）")
    if not actions:
        actions.append("1. 无待办，保持现状")
    summary += actions
    write("SUMMARY.md", summary)

    print(summary[0])
    for line in summary[4:]:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
