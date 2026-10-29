#!/usr/bin/env python3
"""Builds the simulated timeline of this repository, then replays it as commits.

  generate.py plan --increments increments.json --out plan.json --summary PLAN.md --preview preview.html
  generate.py run  --plan plan.json --content DIR --repo DIR --manifest provenance.jsonl --expect-email EMAIL
                   [--count N]

`plan` is deterministic for a given seed and end date. It draws which days have activity, how many commits each day
gets, and on which days the substantive increments land. It writes the plan, a per-year summary and an HTML preview of
the yearly calendars.

`run` appends the next N planned commits to a repository:

- A substantive increment copies its files from the content folder.
- A simulation record appends one line to simulation/records/<year>.tsv and changes nothing else.

Only the author date is set (GIT_AUTHOR_DATE). The committer date stays the real time of creation. Every commit is
recorded in the provenance manifest with its assigned date, its real generation time and its hash.

It never rewrites, amends or pushes. It stops if the repository has commits the manifest doesn't know, if the working
tree is dirty, if the local commit email isn't the expected one, or if a planned date lies in the future.
Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import random
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

UTC = dt.timezone.utc
TRAILERS = (
    "Author-Date-Simulated: true\n"
    "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
    "Claude-Session: https://claude.ai/code/session_01NAFbn2QurZm4MC8VV2iUJQ"
)

# Share of days with activity, before weekday, month and streak adjustments. Lower from 2022, when real activity
# exists on the profile, so the simulation doesn't dominate those years.
YEAR_LEVEL = {2017: 0.40, 2018: 0.47, 2019: 0.50, 2020: 0.45, 2021: 0.42,
              2022: 0.18, 2023: 0.17, 2024: 0.18, 2025: 0.20, 2026: 0.20}
WEEKDAY_FACTOR = (1.0, 1.0, 1.0, 1.0, 0.9, 0.7, 0.55)  # Monday .. Sunday
COMMITS_PER_DAY = {  # commits on an active day: mostly one to three, occasionally up to six
    "busy": ((1, 2, 3, 4, 5, 6), (0.34, 0.27, 0.18, 0.11, 0.06, 0.04)),
    "light": ((1, 2, 3, 4, 5), (0.46, 0.29, 0.14, 0.08, 0.03)),
}


def daterange(start: dt.date, end: dt.date):
    day = start
    while day <= end:
        yield day
        day += dt.timedelta(days=1)


def build_plan(increments: list[dict], seed: str, start: dt.date, end: dt.date) -> dict:
    rng = random.Random(seed)
    years = range(start.year, end.year + 1)

    # two or three breaks per year (holidays, exams, moves) and two quieter months
    breaks: set[dt.date] = set()
    quiet_months: dict[int, set[int]] = {}
    for year in years:
        quiet_months[year] = set(rng.sample(range(1, 13), 2))
        for _ in range(rng.randint(2, 3)):
            begin = dt.date(year, 1, 1) + dt.timedelta(days=rng.randrange(365))
            breaks.update(begin + dt.timedelta(days=k) for k in range(rng.randint(6, 18)))

    counts: dict[dt.date, int] = {}
    previous_active = False
    for day in daterange(start, end):
        if day in breaks:
            count = 0
        else:
            p = YEAR_LEVEL.get(day.year, 0.2) * WEEKDAY_FACTOR[day.weekday()]
            p *= 0.4 if day.month in quiet_months[day.year] else 1.0
            p *= 0.35 if (day.month == 12 and day.day >= 22) else 1.0
            p *= 1.3 if previous_active else 0.85  # activity clusters into streaks and gaps
            if rng.random() < min(p, 0.9):
                values, weights = COMMITS_PER_DAY["busy" if day.year <= 2021 else "light"]
                count = rng.choices(values, weights)[0]
            else:
                count = 0
        counts[day] = count
        previous_active = count > 0

    active_days = [day for day, count in counts.items() if count]
    # increments arrive module by module: each module starts at an evenly spaced point of the timeline and its
    # increments land on the following active days, a few days apart
    modules: list[list[dict]] = []
    for increment in increments:
        key = "/".join(increment["files"][0].split("/")[:2]) if increment["id"] != "start" else "start"
        if modules and modules[-1][0]["_module"] == key:
            modules[-1].append({**increment, "_module": key})
        else:
            modules.append([{**increment, "_module": key}])
    placed: dict[dt.date, dict] = {}
    cursor = 0
    for index, module in enumerate(modules):
        # the last module starts about 20 active days before the end, so increments reach the final year too
        cursor = max(cursor, round(index * (len(active_days) - 20) / max(len(modules) - 1, 1)))
        for increment in module:
            placed[active_days[cursor]] = increment
            cursor += 1 + rng.randint(0, 3)
    if len(placed) != len(increments):
        raise SystemExit("not enough active days to place every increment")

    commits = []
    for day in active_days:
        seconds = sorted(rng.sample(range(9 * 3600, 22 * 3600), counts[day]))
        for position, second in enumerate(seconds):
            moment = dt.datetime.combine(day, dt.time(), UTC) + dt.timedelta(seconds=second)
            entry = {"seq": len(commits) + 1, "date": moment.isoformat()}
            if position == 0 and day in placed:
                increment = placed[day]
                entry.update(kind="increment", id=increment["id"], message=increment["message"],
                             files=increment["files"])
            else:
                entry.update(kind="record")
            commits.append(entry)
    return {
        "seed": seed,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "parameters": {"yearLevel": YEAR_LEVEL, "weekdayFactor": WEEKDAY_FACTOR, "commitsPerDay": COMMITS_PER_DAY},
        "commits": commits,
    }


def summarise(plan: dict) -> list[dict]:
    per_year: dict[int, Counter] = defaultdict(Counter)
    days: dict[int, set] = defaultdict(set)
    for commit in plan["commits"]:
        year = int(commit["date"][:4])
        per_year[year][commit["kind"]] += 1
        days[year].add(commit["date"][:10])
    rows = []
    for year in sorted(per_year):
        counts = Counter(c["date"][:10] for c in plan["commits"] if c["date"].startswith(str(year)))
        rows.append({
            "year": year,
            "activeDays": len(days[year]),
            "commits": sum(per_year[year].values()),
            "increments": per_year[year]["increment"],
            "records": per_year[year]["record"],
            "maxPerDay": max(counts.values()),
        })
    return rows


def write_summary(plan: dict, path: Path) -> None:
    rows = summarise(plan)
    total = {k: sum(r[k] for r in rows) for k in ("activeDays", "commits", "increments", "records")}

    def share(years: list[dict]) -> int:
        days = sum((dt.date(min(r["year"], int(plan["end"][:4])), 12, 31) if r["year"] < int(plan["end"][:4])
                    else dt.date.fromisoformat(plan["end"])).timetuple().tm_yday for r in years)
        return round(100 * sum(r["activeDays"] for r in years) / days) if days else 0

    early_share = share([r for r in rows if r["year"] <= 2021])
    late_share = share([r for r in rows if r["year"] >= 2022])
    lines = [
        "# Simulation plan",
        "",
        f"Seed `{plan['seed']}`, dates from {plan['start']} to {plan['end']} (UTC). Author dates are simulated;",
        "committer dates are the real creation times.",
        "",
        "| Year | Active days | Commits | Substantive increments | Simulation records | Most in one day |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        *(f"| {r['year']} | {r['activeDays']} | {r['commits']} | {r['increments']} | {r['records']} | {r['maxPerDay']} |"
          for r in rows),
        f"| **Total** | **{total['activeDays']}** | **{total['commits']}** | **{total['increments']}** | "
        f"**{total['records']}** | |",
        "",
        "## How the density was chosen",
        "",
        f"- {early_share}% of days are active from 2017 to 2021 and {late_share}% from 2022 on. The rate is lower",
        "  from 2022 because those years already have real activity on the profile.",
        "- Weekends, two quieter months per year, late December and two or three breaks of 6-18 days per year make",
        "  some weeks and months clearly quieter. An active day makes the next one more likely, so activity comes in",
        "  streaks with gaps between them.",
        "- An active day has one to six commits, mostly one to three (one to five from 2022). No day reaches a fixed",
        "  maximum, and most squares stay light.",
        "- The 50 substantive increments arrive module by module across the timeline. Every other commit is a",
        "  simulation record that touches only `simulation/records/`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(plan: dict, path: Path) -> None:
    """One GitHub-style calendar per year: 53 week columns x 7 weekday rows, four shades by commits per day."""
    counts = Counter(c["date"][:10] for c in plan["commits"])
    increments = {c["date"][:10] for c in plan["commits"] if c["kind"] == "increment"}
    shades = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    rows = {r["year"]: r for r in summarise(plan)}
    parts = []
    for year in range(int(plan["start"][:4]), int(plan["end"][:4]) + 1):
        first = dt.date(year, 1, 1)
        offset = (first.weekday() + 1) % 7  # GitHub columns start on Sunday
        cells = []
        for day in daterange(first, dt.date(year, 12, 31)):
            index = (day - first).days + offset
            n = counts.get(day.isoformat(), 0)
            level = 0 if n == 0 else 1 if n == 1 else 2 if n == 2 else 3 if n <= 4 else 4
            future = day.isoformat() > plan["end"]
            stroke = ' stroke="#8250df" stroke-width="1.5"' if day.isoformat() in increments else ""
            cells.append(
                f'<rect x="{(index // 7) * 13}" y="{(index % 7) * 13}" width="11" height="11" rx="2" '
                f'fill="{"#ffffff" if future else shades[level]}"{stroke}>'
                f"<title>{day.isoformat()}: {n} commit(s)</title></rect>"
            )
        r = rows.get(year, {"activeDays": 0, "commits": 0, "increments": 0, "records": 0})
        parts.append(
            f"<h2>{year}</h2><p>{r['commits']} commits on {r['activeDays']} days: {r['increments']} substantive "
            f"increments (outlined), {r['records']} simulation records</p>"
            f'<svg width="{54 * 13}" height="{7 * 13}" role="img" aria-label="{year} calendar">{"".join(cells)}</svg>'
        )
    path.write_text(
        "<!doctype html><meta charset='utf-8'><title>Simulation preview</title>"
        "<style>body{font:14px system-ui,sans-serif;margin:24px;max-width:760px}h2{margin:20px 0 4px}"
        "p{margin:0 0 6px;color:#555}</style>"
        f"<h1>Simulated calendar preview</h1><p>{html.escape(plan['start'])} to {html.escape(plan['end'])}, seed "
        f"{html.escape(plan['seed'])}. Shades: 1, 2, 3-4, 5+ commits per day. Purple outline: a substantive increment.</p>"
        + "".join(parts),
        encoding="utf-8",
    )


def git(repo: Path, *args: str, env: dict | None = None) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
                          env=env).stdout.strip()


def run(plan: dict, content: Path, repo: Path, manifest: Path, expect_email: str, count: int | None) -> None:
    if git(repo, "config", "--local", "user.email") != expect_email:
        raise SystemExit(f"refusing: the repository's local user.email is not {expect_email}")
    if git(repo, "status", "--porcelain"):
        raise SystemExit("refusing: the working tree has uncommitted changes")
    done = [json.loads(line) for line in manifest.read_text().splitlines()] if manifest.exists() else []
    head = git(repo, "rev-parse", "--verify", "-q", "HEAD") if done else ""
    if done and head != done[-1]["commit"]:
        raise SystemExit("refusing: HEAD is not the last commit in the manifest (history changed outside this tool)")
    if not done and subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "-q", "HEAD"],
                                   capture_output=True).returncode == 0:
        raise SystemExit("refusing: the repository already has commits but the manifest is empty")

    pending = plan["commits"][len(done):]
    if count is not None:
        pending = pending[:count]
    now = dt.datetime.now(UTC)
    if any(dt.datetime.fromisoformat(c["date"]) > now for c in pending):
        raise SystemExit("refusing: the plan contains a date in the future")

    env = {k: v for k, v in os.environ.items() if k not in ("GIT_COMMITTER_DATE", "GIT_AUTHOR_DATE")}
    with manifest.open("a", encoding="utf-8") as out:
        for commit in pending:
            if commit["kind"] == "increment":
                for name in commit["files"]:
                    target = repo / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(content / name, target)
                git(repo, "add", "--", *commit["files"])
                message = commit["message"]
                changed = commit["files"]
            else:
                year = commit["date"][:4]
                record = repo / "simulation" / "records" / f"{year}.tsv"
                record.parent.mkdir(parents=True, exist_ok=True)
                with record.open("a", encoding="utf-8") as handle:
                    handle.write(f"{commit['seq']}\t{commit['date']}\tsimulation record\n")
                git(repo, "add", "--", str(record.relative_to(repo)))
                message = f"simulation: record for {commit['date'][:10]} (no code change)"
                changed = [str(record.relative_to(repo))]
            git(repo, "commit", "-q", "-m", f"{message}\n\n{TRAILERS}", env={**env, "GIT_AUTHOR_DATE": commit["date"]})
            entry = {
                "seq": commit["seq"],
                "kind": commit["kind"],
                "id": commit.get("id"),
                "assignedAuthorDate": commit["date"],
                "generatedAt": dt.datetime.now(UTC).isoformat(timespec="seconds"),
                "files": changed,
                "commit": git(repo, "rev-parse", "HEAD"),
            }
            out.write(json.dumps(entry) + "\n")
            out.flush()
    print(f"generated {len(pending)} commit(s); {len(done) + len(pending)} of {len(plan['commits'])} planned")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--increments", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    p.add_argument("--preview", type=Path, required=True)
    p.add_argument("--seed", default="retrospective-programming-lab-2026")
    p.add_argument("--start", default="2017-01-01")
    p.add_argument("--end", help="last simulated day (default: yesterday, UTC); never in the future")
    r = sub.add_parser("run")
    r.add_argument("--plan", type=Path, required=True)
    r.add_argument("--content", type=Path, required=True)
    r.add_argument("--repo", type=Path, required=True)
    r.add_argument("--manifest", type=Path, required=True)
    r.add_argument("--expect-email", required=True)
    r.add_argument("--count", type=int)
    args = parser.parse_args(argv)

    if args.command == "plan":
        yesterday = dt.datetime.now(UTC).date() - dt.timedelta(days=1)
        end = dt.date.fromisoformat(args.end) if args.end else yesterday
        if end > yesterday:
            raise SystemExit("the end date must be in the past")
        plan = build_plan(json.loads(args.increments.read_text()), args.seed, dt.date.fromisoformat(args.start), end)
        args.out.write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
        write_summary(plan, args.summary)
        write_preview(plan, args.preview)
        for row in summarise(plan):
            print(row)
    else:
        run(json.loads(args.plan.read_text()), args.content, args.repo, args.manifest, args.expect_email, args.count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
