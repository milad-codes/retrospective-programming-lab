import random
import unittest
from collections import deque

from linked_structures.stack_queue import Stack, TwoStackQueue, balanced


class StackQueueTest(unittest.TestCase):
    def test_stack_is_lifo(self):
        stack = Stack()
        for n in range(3):
            stack.push(n)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [2, 1, 0])
        with self.assertRaises(IndexError):
            stack.pop()

    def test_queue_matches_deque_under_random_operations(self):
        rng = random.Random(5)
        queue, reference = TwoStackQueue(), deque()
        for step in range(5000):
            if reference and rng.random() < 0.45:
                self.assertEqual(queue.dequeue(), reference.popleft())
            else:
                queue.enqueue(step)
                reference.append(step)
            self.assertEqual(len(queue), len(reference))

    def test_balanced_brackets(self):
        self.assertTrue(balanced("f(a[1], {b: (2)})"))
        self.assertTrue(balanced(""))
        self.assertFalse(balanced("(]"))
        self.assertFalse(balanced("(()"))
        self.assertFalse(balanced(")("))


if __name__ == "__main__":
    unittest.main()
