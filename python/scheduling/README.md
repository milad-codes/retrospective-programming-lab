# CPU scheduling

A small simulator for the scheduling algorithms taught in operating-systems courses. Each run returns the timeline as
`(process, start, end)` slices together with per-process waiting and turnaround times.

| Function | Algorithm | Preemptive |
| --- | --- | --- |
| `fcfs` | first come, first served | no |
| `sjf` | shortest job first | no |
| `srtf` | shortest remaining time first | yes, re-evaluated every time unit |
| `priority` | lowest priority number first | no |
| `round_robin(quantum)` | fixed time slices in arrival order | yes |

The textbook example (P1–P4) checks exact timelines. Random workloads check the invariants every scheduler must keep:

- each process runs exactly its burst time
- the CPU never runs two processes at once
- nothing starts before it arrives
- SRTF never has a higher average waiting time than SJF

```bash
python3 -m unittest discover -s scheduling -t .
```
