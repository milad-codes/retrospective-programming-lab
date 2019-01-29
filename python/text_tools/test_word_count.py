import io
import unittest
from contextlib import redirect_stdout

from text_tools.word_count import main, top_words, words


class WordCountTest(unittest.TestCase):
    def test_splits_words_across_scripts_and_keeps_contractions(self):
        self.assertEqual(
            words("Don't panic — Müller's state-of-the-art café, 3 times!"),
            ["don't", "panic", "müller's", "state-of-the-art", "café", "3", "times"],
        )

    def test_counts_case_insensitively_and_breaks_ties_alphabetically(self):
        lines = ["The cat and the hat.", "A cat, a bat."]
        self.assertEqual(top_words(lines, 3), [("a", 2), ("cat", 2), ("the", 2)])
        self.assertEqual(top_words(lines, 2, ignore={"a", "the"}), [("cat", 2), ("and", 1)])

    def test_command_line(self):
        out = io.StringIO()
        with redirect_stdout(out):
            main(["--top", "1", "/dev/null"])
        self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
