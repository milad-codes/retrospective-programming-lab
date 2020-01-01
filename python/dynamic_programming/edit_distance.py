"""Levenshtein distance with the list of edits that achieves it."""


def edit_distance(a: str, b: str) -> int:
    """O(len(a) * len(b)) time, O(min) memory: only two rows of the table are kept."""
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (char_a != char_b)))
        previous = current
    return previous[-1]


def edit_script(a: str, b: str) -> list[str]:
    """Edits turning a into b, e.g. ["keep k", "replace i→e", "insert s"]. Keeps the full table to walk back."""
    rows, cols = len(a) + 1, len(b) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        table[i][0] = i
    for j in range(cols):
        table[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            table[i][j] = min(table[i - 1][j] + 1, table[i][j - 1] + 1, table[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    edits, i, j = [], len(a), len(b)
    while i or j:
        if i and j and table[i][j] == table[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            edits.append(f"keep {a[i - 1]}" if a[i - 1] == b[j - 1] else f"replace {a[i - 1]}→{b[j - 1]}")
            i, j = i - 1, j - 1
        elif i and table[i][j] == table[i - 1][j] + 1:
            edits.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            edits.append(f"insert {b[j - 1]}")
            j -= 1
    return edits[::-1]
