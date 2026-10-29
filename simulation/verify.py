#!/usr/bin/env python3
"""Checks the provenance manifest against this repository's git history.

  python3 simulation/verify.py

For every manifest entry, the commit must be in the history with the assigned author date. A simulation record must
change exactly its line file under simulation/records/, and a substantive increment must change only the files it lists
and never touch simulation/records/. It prints the range of real committer dates. Standard library only.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = "simulation/records/"


def history() -> dict[str, tuple[str, str, list[str]]]:
    """Maps each commit hash to its author date, committer date and changed files."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--no-renames", "--name-only", "--format=%x00%H %aI %cI"],
        check=True, capture_output=True, text=True,
    ).stdout
    commits = {}
    for chunk in out.split("\0")[1:]:
        header, _, names = chunk.partition("\n")
        sha, author_date, committer_date = header.split()
        commits[sha] = (author_date, committer_date, [n for n in names.splitlines() if n])
    return commits


def main() -> int:
    entries = [json.loads(line) for line in (ROOT / "simulation" / "provenance.jsonl").read_text().splitlines()]
    commits = history()
    problems = []
    for entry in entries:
        where = f"seq {entry['seq']} ({entry['commit'][:12]})"
        if entry["commit"] not in commits:
            problems.append(f"{where}: not in the history")
            continue
        author_date, _, changed = commits[entry["commit"]]
        if author_date != entry["assignedAuthorDate"]:
            problems.append(f"{where}: author date {author_date}, manifest says {entry['assignedAuthorDate']}")
        if entry["kind"] == "record":
            if changed != entry["files"] or not all(name.startswith(RECORDS) for name in changed):
                problems.append(f"{where}: a simulation record changed {changed}")
        elif any(name.startswith(RECORDS) for name in changed) or not set(changed) <= set(entry["files"]):
            problems.append(f"{where}: an increment changed {changed}")
    for problem in problems:
        print(problem)
    if problems:
        print(f"{len(problems)} problem(s) in {len(entries)} manifest entries")
        return 1
    committed = sorted(commits[e["commit"]][1] for e in entries)
    kinds = {kind: sum(1 for e in entries if e["kind"] == kind) for kind in ("increment", "record")}
    print(f"{len(entries)} manifest entries match the history: {kinds['increment']} substantive increments, "
          f"{kinds['record']} simulation records. Real committer dates: {committed[0]} to {committed[-1]}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
