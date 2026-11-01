#!/usr/bin/env python3
"""Checks the provenance manifest against this repository's git history.

  python3 simulation/verify.py

For every manifest entry, the commit must be in the history with the assigned author date. A simulation record must
change exactly its line file under simulation/records/, and a substantive increment must change only the files it lists
and never touch simulation/records/. It prints the range of real committer dates. Standard library only.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = "simulation/records/"
SHOWN = 20  # problems printed in full; the rest are counted


def instant(text: str) -> dt.datetime:
    """Parses an ISO 8601 date. Recent git versions print UTC as "Z" in %aI, older ones as "+00:00"."""
    return dt.datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def report(problems: list[str]) -> None:
    """Prints the first problems, and in GitHub Actions also turns them into error annotations."""
    for problem in problems[:SHOWN]:
        print(problem)
    if len(problems) > SHOWN:
        print(f"... and {len(problems) - SHOWN} more")
    if os.environ.get("GITHUB_ACTIONS") == "true":
        for problem in problems[:10]:
            text = problem.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::error title=Provenance check::{text}")


def history() -> dict[str, tuple[str, str, list[str]]]:
    """Maps each commit hash to its author date, committer date and changed files."""
    out = git("log", "--no-renames", "--name-only", "--format=%x00%H %aI %cI")
    commits = {}
    for chunk in out.split("\0")[1:]:
        header, _, names = chunk.partition("\n")
        sha, author_date, committer_date = header.split()
        commits[sha] = (author_date, committer_date, [n for n in names.splitlines() if n])
    return commits


def main() -> int:
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        report(["the clone is shallow: fetch the whole history first (actions/checkout: fetch-depth: 0)"])
        return 1
    entries = [json.loads(line) for line in (ROOT / "simulation" / "provenance.jsonl").read_text().splitlines()]
    commits = history()
    print(f"{git('--version').strip()}; {len(commits)} commits in the history, {len(entries)} manifest entries")
    problems = []
    for entry in entries:
        where = f"seq {entry['seq']} ({entry['commit'][:12]})"
        if entry["commit"] not in commits:
            problems.append(f"{where}: not in the history")
            continue
        author_date, _, changed = commits[entry["commit"]]
        if instant(author_date) != instant(entry["assignedAuthorDate"]):
            problems.append(f"{where}: author date {author_date}, manifest says {entry['assignedAuthorDate']}")
        if entry["kind"] == "record":
            if changed != entry["files"] or not all(name.startswith(RECORDS) for name in changed):
                problems.append(f"{where}: a simulation record changed {changed}")
        elif any(name.startswith(RECORDS) for name in changed) or not set(changed) <= set(entry["files"]):
            problems.append(f"{where}: an increment changed {changed}")
    report(problems)
    if problems:
        print(f"{len(problems)} problem(s) in {len(entries)} manifest entries")
        return 1
    committed = sorted(instant(commits[e["commit"]][1]).astimezone(dt.timezone.utc) for e in entries)
    kinds = {kind: sum(1 for e in entries if e["kind"] == kind) for kind in ("increment", "record")}
    print(f"{len(entries)} manifest entries match the history: {kinds['increment']} substantive increments, "
          f"{kinds['record']} simulation records. Real committer dates: {committed[0]:%Y-%m-%d %H:%M:%S} to "
          f"{committed[-1]:%Y-%m-%d %H:%M:%S} UTC.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
