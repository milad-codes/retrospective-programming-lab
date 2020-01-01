import random
import unittest

from dynamic_programming.edit_distance import edit_distance, edit_script


def apply(a: str, edits: list[str]) -> str:
    out, i = [], 0
    for edit in edits:
        op, arg = edit.split(" ", 1)
        if op == "keep":
            out.append(a[i])
            i += 1
        elif op == "replace":
            out.append(arg.split("→")[1])
            i += 1
        elif op == "delete":
            i += 1
        else:
            out.append(arg)
    return "".join(out)


class EditDistanceTest(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("flaw", "lawn"), 2)

    def test_script_reproduces_the_target_with_the_minimal_number_of_edits(self):
        rng = random.Random(11)
        for _ in range(300):
            a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            script = edit_script(a, b)
            self.assertEqual(apply(a, script), b)
            self.assertEqual(sum(not e.startswith("keep") for e in script), edit_distance(a, b))


if __name__ == "__main__":
    unittest.main()
