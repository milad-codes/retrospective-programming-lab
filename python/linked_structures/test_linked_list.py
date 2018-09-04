import unittest

from linked_structures.linked_list import LinkedList


class LinkedListTest(unittest.TestCase):
    def test_append_prepend_and_iterate(self):
        items = LinkedList([2, 3])
        items.prepend(1)
        items.append(4)
        self.assertEqual(list(items), [1, 2, 3, 4])
        self.assertEqual(len(items), 4)

    def test_remove_keeps_the_tail_correct(self):
        items = LinkedList([1, 2, 3])
        self.assertTrue(items.remove(3))
        items.append(9)  # would be lost if the tail still pointed at the removed node
        self.assertEqual(list(items), [1, 2, 9])
        self.assertFalse(items.remove(42))

    def test_remove_head_and_only_element(self):
        items = LinkedList([7])
        self.assertTrue(items.remove(7))
        self.assertEqual(list(items), [])
        items.append(8)
        self.assertEqual(list(items), [8])

    def test_reverse(self):
        for values in ([], [1], [1, 2], list(range(10))):
            items = LinkedList(values)
            items.reverse()
            self.assertEqual(list(items), values[::-1])
            items.append("end")
            self.assertEqual(list(items)[-1], "end")

    def test_pop_front(self):
        items = LinkedList("ab")
        self.assertEqual(items.pop_front(), "a")
        self.assertEqual(items.pop_front(), "b")
        with self.assertRaises(IndexError):
            items.pop_front()


if __name__ == "__main__":
    unittest.main()
