import random
import unittest

from text_tools.rle import decode, encode


class RunLengthTest(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(encode("aaabcc"), "3a1b2c")
        self.assertEqual(encode(""), "")
        self.assertEqual(decode("12x1y"), "xxxxxxxxxxxxy")

    def test_round_trip(self):
        rng = random.Random(8)
        for _ in range(500):
            text = "".join(rng.choice("ab c!") * rng.randint(1, 4) for _ in range(rng.randint(0, 10)))
            self.assertEqual(decode(encode(text)), text)

    def test_rejects_ambiguous_or_malformed_input(self):
        with self.assertRaises(ValueError):
            encode("a1")
        with self.assertRaises(ValueError):
            decode("3a2")
        with self.assertRaises(ValueError):
            decode("ab")


if __name__ == "__main__":
    unittest.main()
