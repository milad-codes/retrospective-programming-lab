# Dynamic programming

Each solver fills a table bottom-up and then walks back through it to recover an actual solution, not just its size.

| File | Problem | Table |
| --- | --- | --- |
| `edit_distance.py` | Levenshtein distance and the edit script | (len a + 1) × (len b + 1); the distance alone needs two rows |
| `lcs.py` | longest common subsequence | (len a + 1) × (len b + 1) |
| `knapsack.py` | 0/1 knapsack with the chosen items | (n + 1) × (capacity + 1): pseudo-polynomial |
| `coin_change.py` | fewest coins and number of ways to pay | one row per amount |

The tests compare against exhaustive search on small random inputs (all subsets, all subsequences). A known case shows
why greedy coin change is wrong for some coin systems: 6 with coins 1, 3 and 4.

```bash
python3 -m unittest discover -s dynamic_programming -t .
```
