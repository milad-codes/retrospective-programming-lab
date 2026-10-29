# Simulation plan

Seed `retrospective-programming-lab-2026`, dates from 2017-01-01 to 2026-10-28 (UTC). Author dates are simulated;
committer dates are the real creation times.

| Year | Active days | Commits | Substantive increments | Simulation records | Most in one day |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2017 | 92 | 223 | 6 | 217 | 6 |
| 2018 | 129 | 327 | 9 | 318 | 6 |
| 2019 | 132 | 307 | 9 | 298 | 6 |
| 2020 | 142 | 354 | 10 | 344 | 6 |
| 2021 | 119 | 296 | 4 | 292 | 6 |
| 2022 | 47 | 90 | 2 | 88 | 5 |
| 2023 | 43 | 78 | 0 | 78 | 4 |
| 2024 | 54 | 108 | 4 | 104 | 5 |
| 2025 | 50 | 106 | 3 | 103 | 5 |
| 2026 | 36 | 66 | 3 | 63 | 5 |
| **Total** | **844** | **1955** | **50** | **1905** | |

## How the density was chosen

- 34% of days are active from 2017 to 2021 and 13% from 2022 on. The rate is lower
  from 2022 because those years already have real activity on the profile.
- Weekends, two quieter months per year, late December and two or three breaks of 6-18 days per year make
  some weeks and months clearly quieter. An active day makes the next one more likely, so activity comes in
  streaks with gaps between them.
- An active day has one to six commits, mostly one to three (one to five from 2022). No day reaches a fixed
  maximum, and most squares stay light.
- The 50 substantive increments arrive module by module across the timeline. Every other commit is a
  simulation record that touches only `simulation/records/`.
