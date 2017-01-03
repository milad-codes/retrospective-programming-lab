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
The final commits add the generator, the plan and a provenance manifest that maps every commit to its real
generation time.
