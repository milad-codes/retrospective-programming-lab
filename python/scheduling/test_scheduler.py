import random
import unittest

from scheduling.scheduler import Process, fcfs, priority, round_robin, sjf, srtf

TEXTBOOK = [Process("P1", 0, 8), Process("P2", 1, 4), Process("P3", 2, 9), Process("P4", 3, 5)]


class SchedulerTest(unittest.TestCase):
    def test_fcfs(self):
        schedule = fcfs(TEXTBOOK)
        self.assertEqual(schedule.timeline, [("P1", 0, 8), ("P2", 8, 12), ("P3", 12, 21), ("P4", 21, 26)])
        self.assertEqual(schedule.average_waiting(TEXTBOOK), (0 + 7 + 10 + 18) / 4)

    def test_srtf_preempts_for_a_shorter_job(self):
        schedule = srtf(TEXTBOOK)
        self.assertEqual(schedule.timeline, [("P1", 0, 1), ("P2", 1, 5), ("P4", 5, 10), ("P1", 10, 17), ("P3", 17, 26)])
        self.assertEqual(schedule.average_waiting(TEXTBOOK), 6.5)

    def test_sjf_does_not_preempt(self):
        self.assertEqual([pid for pid, _, _ in sjf(TEXTBOOK).timeline], ["P1", "P2", "P4", "P3"])

    def test_round_robin(self):
        processes = [Process("A", 0, 5), Process("B", 1, 3), Process("C", 2, 1)]
        schedule = round_robin(processes, quantum=2)
        self.assertEqual(
            schedule.timeline,
            [("A", 0, 2), ("B", 2, 4), ("C", 4, 5), ("A", 5, 7), ("B", 7, 8), ("A", 8, 9)],
        )
        self.assertEqual(schedule.finish, {"C": 5, "B": 8, "A": 9})

    def test_priority_and_idle_cpu(self):
        processes = [Process("low", 0, 2, priority=5), Process("high", 5, 1, priority=1), Process("mid", 5, 1, priority=3)]
        self.assertEqual(priority(processes).timeline, [("low", 0, 2), ("high", 5, 6), ("mid", 6, 7)])

    def test_invariants_for_random_workloads(self):
        rng = random.Random(14)
        for _ in range(50):
            processes = [Process(f"P{i}", rng.randint(0, 20), rng.randint(1, 8), rng.randint(0, 3)) for i in range(6)]
            total = sum(p.burst for p in processes)
            for schedule in (fcfs(processes), sjf(processes), srtf(processes), priority(processes),
                             round_robin(processes, 3)):
                ran = {p.pid: 0 for p in processes}
                for pid, start, end in schedule.timeline:
                    ran[pid] += end - start
                self.assertEqual(ran, {p.pid: p.burst for p in processes})
                self.assertEqual(sum(ran.values()), total)
                slices = sorted(schedule.timeline, key=lambda s: s[1])
                for (_, _, end), (_, start, _) in zip(slices, slices[1:]):
                    self.assertLessEqual(end, start)  # the CPU never runs two processes at once
                for p in processes:
                    first_start = min(s for pid, s, _ in schedule.timeline if pid == p.pid)
                    self.assertGreaterEqual(first_start, p.arrival)

    def test_srtf_never_waits_longer_on_average_than_sjf(self):
        rng = random.Random(15)
        for _ in range(100):
            processes = [Process(f"P{i}", rng.randint(0, 10), rng.randint(1, 10)) for i in range(5)]
            self.assertLessEqual(srtf(processes).average_waiting(processes), sjf(processes).average_waiting(processes))

    def test_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            Process("x", 0, 0)
        with self.assertRaises(ValueError):
            round_robin(TEXTBOOK, 0)


if __name__ == "__main__":
    unittest.main()
