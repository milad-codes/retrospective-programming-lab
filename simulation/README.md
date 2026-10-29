# Simulation records

Most commits in this repository are **simulation records**, not programming work. Each one appends a line to
`records/<year>.tsv` and changes nothing else. They exist only to place the collection's activity on the dates of the
retrospective timeline. The commits that add or change exercises are the **substantive increments**, and they never
touch this folder.

A record line has three fields:

- the sequence number in the plan;
- the simulated author date;
- the label `simulation record`.

Every commit keeps its real creation time as the committer date, so `git log --format='%ad | %cd'` shows both dates.

## Files

| File | What it is |
| --- | --- |
| `generate.py` | Builds the plan, then replays it as commits. Standard library only; it sets only the author date. |
| `increments.json` | The 50 substantive increments in order, with the files each one adds. |
| `plan.json`, `PLAN.md` | Every planned commit with its simulated author date, and a per-year summary with the density rules. |
| `preview.html` | The planned calendar for each year, drawn before any commit was made. |
| `provenance.jsonl` | One line per generated commit: sequence number, kind, assigned author date, real generation time, files and hash. |
| `verify.py` | Checks the manifest against the history. CI runs it on every push. |

To check the manifest yourself, clone the full history and run `python3 simulation/verify.py`.

## Creation record

Real times, in UTC:

- **29 October 2026:** the exercises, tests and documentation were written with Claude (Anthropic's AI assistant),
  which wrote most of the code. The plan was generated next: 1,955 commits from 1 January 2017 to 28 October 2026,
  with 50 substantive increments and 1,905 simulation records.
- **14:25:** a first five-commit pilot was generated locally. It was discarded without being pushed so that the
  disclosure in the main README could sit on a single line.
- **16:39 to 16:40:** the five-commit pilot (January 2017) was generated and pushed. It appeared on the public
  contribution calendar within about five minutes.
- **16:44 to 16:51:** the other 1,950 planned commits were generated and pushed, one push per simulated year.
- The commit that adds the files listed above has real author and committer dates.
