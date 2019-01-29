"""Counts words in text or files: `python3 -m text_tools.word_count --top 5 FILE...` (reads stdin without files)."""

import argparse
import re
import sys
from collections import Counter
from collections.abc import Iterable

# letters (any script), digits and inner apostrophes or hyphens: "don't", "state-of-the-art", "Müller"
WORD = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*")


def words(text: str) -> list[str]:
    return [match.group().casefold() for match in WORD.finditer(text)]


def top_words(lines: Iterable[str], n: int, ignore: set[str] = frozenset()) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for line in lines:
        counts.update(word for word in words(line) if word not in ignore)
    # ties are broken alphabetically so the output is deterministic
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print the most frequent words.")
    parser.add_argument("files", nargs="*", type=argparse.FileType("r", encoding="utf-8"), default=[sys.stdin])
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--ignore", default="", help="comma-separated words to skip")
    args = parser.parse_args(argv)
    ignore = {word.casefold() for word in args.ignore.split(",") if word}
    lines = (line for handle in args.files for line in handle)
    for word, count in top_words(lines, args.top, ignore):
        print(f"{count:7d} {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
