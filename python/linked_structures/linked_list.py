"""A singly linked list with a tail pointer, so appending is O(1)."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    value: T
    next: "_Node[T] | None" = None


class LinkedList(Generic[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        self._head: _Node[T] | None = None
        self._tail: _Node[T] | None = None
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"LinkedList({list(self)!r})"

    def append(self, value: T) -> None:
        node = _Node(value)
        if self._tail:
            self._tail.next = node
        else:
            self._head = node
        self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        self._head = _Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def pop_front(self) -> T:
        if self._head is None:
            raise IndexError("pop from an empty list")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def remove(self, value: T) -> bool:
        """Removes the first occurrence; returns whether something was removed."""
        previous, node = None, self._head
        while node:
            if node.value == value:
                if previous:
                    previous.next = node.next
                else:
                    self._head = node.next
                if node is self._tail:
                    self._tail = previous
                self._size -= 1
                return True
            previous, node = node, node.next
        return False

    def reverse(self) -> None:
        """Reverses in place by turning every next pointer around: O(n) time, O(1) space."""
        previous, node = None, self._head
        self._tail = node
        while node:
            node.next, previous, node = previous, node, node.next
        self._head = previous
