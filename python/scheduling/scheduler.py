"""Simulates single-CPU scheduling and reports per-process waiting and turnaround times.

Each algorithm returns a Schedule: the timeline as (pid, start, end) slices, plus metrics. Time is in integer units
and context switches are free, as in most textbook exercises.
"""

from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int = 0  # lower number = more important

    def __post_init__(self) -> None:
        if self.arrival < 0 or self.burst <= 0:
            raise ValueError(f"{self.pid}: arrival must be >= 0 and burst > 0")


@dataclass
class Schedule:
    timeline: list[tuple[str, int, int]] = field(default_factory=list)
    finish: dict[str, int] = field(default_factory=dict)

    def run(self, pid: str, start: int, end: int) -> None:
        # merge with the previous slice when the same process simply keeps the CPU
        if self.timeline and self.timeline[-1][0] == pid and self.timeline[-1][2] == start:
            self.timeline[-1] = (pid, self.timeline[-1][1], end)
        else:
            self.timeline.append((pid, start, end))

    def metrics(self, processes: list[Process]) -> dict[str, dict[str, int]]:
        result = {}
        for p in processes:
            turnaround = self.finish[p.pid] - p.arrival
            result[p.pid] = {"turnaround": turnaround, "waiting": turnaround - p.burst}
        return result

    def average_waiting(self, processes: list[Process]) -> float:
        return sum(m["waiting"] for m in self.metrics(processes).values()) / len(processes)


def fcfs(processes: list[Process]) -> Schedule:
    """First come, first served."""
    schedule, clock = Schedule(), 0
    for p in sorted(processes, key=lambda p: (p.arrival, p.pid)):
        clock = max(clock, p.arrival)
        schedule.run(p.pid, clock, clock + p.burst)
        clock += p.burst
        schedule.finish[p.pid] = clock
    return schedule


def _non_preemptive(processes: list[Process], choose) -> Schedule:
    pending = sorted(processes, key=lambda p: (p.arrival, p.pid))
    schedule, clock = Schedule(), 0
    while pending:
        ready = [p for p in pending if p.arrival <= clock] or [pending[0]]
        p = min(ready, key=choose)
        clock = max(clock, p.arrival)
        schedule.run(p.pid, clock, clock + p.burst)
        clock += p.burst
        schedule.finish[p.pid] = clock
        pending.remove(p)
    return schedule


def sjf(processes: list[Process]) -> Schedule:
    """Shortest job first, non-preemptive: among arrived processes, the shortest burst runs to completion."""
    return _non_preemptive(processes, lambda p: (p.burst, p.arrival, p.pid))


def priority(processes: list[Process]) -> Schedule:
    """Non-preemptive priority scheduling."""
    return _non_preemptive(processes, lambda p: (p.priority, p.arrival, p.pid))


def srtf(processes: list[Process]) -> Schedule:
    """Shortest remaining time first: preemptive SJF, re-evaluated at every time unit."""
    remaining = {p.pid: p.burst for p in processes}
    by_pid = {p.pid: p for p in processes}
    schedule, clock = Schedule(), 0
    while remaining:
        ready = [pid for pid in remaining if by_pid[pid].arrival <= clock]
        if not ready:
            clock = min(by_pid[pid].arrival for pid in remaining)
            continue
        pid = min(ready, key=lambda q: (remaining[q], by_pid[q].arrival, q))
        schedule.run(pid, clock, clock + 1)
        clock += 1
        remaining[pid] -= 1
        if remaining[pid] == 0:
            del remaining[pid]
            schedule.finish[pid] = clock
    return schedule


def round_robin(processes: list[Process], quantum: int) -> Schedule:
    """Each process runs for at most `quantum` units, then goes to the back of the queue.

    Processes arriving during a slice are queued before the preempted process, the usual textbook convention.
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    arrivals = deque(sorted(processes, key=lambda p: (p.arrival, p.pid)))
    remaining = {p.pid: p.burst for p in processes}
    queue: deque[str] = deque()
    schedule, clock = Schedule(), 0

    def admit(until: int) -> None:
        while arrivals and arrivals[0].arrival <= until:
            queue.append(arrivals.popleft().pid)

    while arrivals or queue:
        admit(clock)
        if not queue:
            clock = arrivals[0].arrival
            continue
        pid = queue.popleft()
        run = min(quantum, remaining[pid])
        schedule.run(pid, clock, clock + run)
        clock += run
        remaining[pid] -= run
        admit(clock)
        if remaining[pid]:
            queue.append(pid)
        else:
            schedule.finish[pid] = clock
    return schedule
