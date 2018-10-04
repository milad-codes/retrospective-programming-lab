"""A stack, and a FIFO queue built from two stacks with amortised O(1) operations."""

from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, value: T) -> None:
        self._items.append(value)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)


class TwoStackQueue(Generic[T]):
    """Enqueue onto `inbox`; dequeue from `outbox`, refilling it only when empty. Each item moves once."""

    def __init__(self) -> None:
        self._inbox: Stack[T] = Stack()
        self._outbox: Stack[T] = Stack()

    def enqueue(self, value: T) -> None:
        self._inbox.push(value)

    def dequeue(self) -> T:
        if not len(self._outbox):
            while len(self._inbox):
                self._outbox.push(self._inbox.pop())
        if not len(self._outbox):
            raise IndexError("dequeue from an empty queue")
        return self._outbox.pop()

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)


def balanced(text: str) -> bool:
    """Checks (), [] and {} nesting with a stack; other characters are ignored."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: Stack[str] = Stack()
    for char in text:
        if char in "([{":
            stack.push(char)
        elif char in pairs:
            if not len(stack) or stack.pop() != pairs[char]:
                return False
    return not len(stack)
