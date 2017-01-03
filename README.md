# Retrospective programming lab

> **Created in 2026 as a retrospective programming collection. Historical commit author dates are simulated and do not represent the original dates of development.**

This repository is a set of original, runnable programming exercises and small projects. It was created in October
2026 for Milad Akbari, with substantial help from an AI assistant (Claude by Anthropic), which wrote most of the code,
tests and documentation.

Its commit history places the work on a timeline from 2017 to 2026. The timeline is simulated:

- **Author dates** are assigned by a script.
- **Committer dates** are the real creation times. `git log --format='%h %ad | %cd'` shows both.
- **Most commits are simulation records.** They only append a line under `simulation/records/` and contain no
  programming work. Exercises arrive in separate commits that never touch that folder.
- **Provenance:** the final commits add the generator, its plan and a manifest. The manifest maps every commit to its
  assigned author date, its real generation time and what it contains.

It is **not** recovered work. It's not a record of past employment, of collaboration with anyone, or of experience in
the years its dates show.

## The collection

| Folder | Language | Topics |
| --- | --- | --- |
| `python/number_theory` | Python | gcd and modular inverse, sieve, fast modular power, Miller–Rabin |
| `python/sorting` | Python | insertion, merge, quick (three-way) and heap sort |
| `python/linked_structures` | Python | linked list, two-stack queue, O(1) LRU cache |
| `python/text_tools` | Python | word counter CLI, Caesar and Vigenère ciphers, run-length encoding |
| `python/graphs` | Python | BFS and DFS, Dijkstra, topological sort, Kruskal with union-find |
| `python/dynamic_programming` | Python | edit distance with script, LCS, 0/1 knapsack, coin change |
| `python/library_sql` | Python + SQL | SQLite schema with constraints, a race-free loan, window-function reports |
| `python/scheduling` | Python | CPU scheduling simulator: FCFS, SJF, SRTF, priority, round robin |
| `typescript/expression-evaluator` | TypeScript | tokenizer, Pratt parser, evaluator, minimal-parentheses printer |
| `typescript/json-parser` | TypeScript | RFC 8259 parser with line and column errors |
| `typescript/async-utils` | TypeScript | concurrency-limited map, retry with backoff, debounce and throttle |
| `typescript/rate-limiter` | TypeScript | token bucket and sliding-window log |
| `typescript/http-router` | TypeScript | router with 404/405, middleware and a `node:http` adapter |

Each folder has its own README that explains the approach and the trade-offs. Where possible, the tests compare
against a reference: the standard library, brute force or a model implementation. Hand-picked examples alone miss
too much.

## Run the tests

You need Python 3.10 or newer and Node 22.18 or newer. Node runs TypeScript directly, so nothing has to be installed.

```bash
./scripts/test-all.sh
cd typescript && npm ci && npm run typecheck   # optional: type-check the TypeScript exercises
```

## Licence

MIT. See [LICENSE](LICENSE).
