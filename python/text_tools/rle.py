"""Run-length encoding: "aaabcc" ↔ "3a1b2c". Digits in the input would be ambiguous, so they are rejected."""

import re


def encode(text: str) -> str:
    if any(c.isdigit() for c in text):
        raise ValueError("digits cannot be run-length encoded in this format")
    result, i = [], 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1
        result.append(f"{j - i}{text[i]}")
        i = j
    return "".join(result)


def decode(encoded: str) -> str:
    parts = re.findall(r"(\d+)(\D)", encoded)
    if "".join(count + char for count, char in parts) != encoded:
        raise ValueError(f"not valid run-length data: {encoded!r}")
    return "".join(char * int(count) for count, char in parts)
