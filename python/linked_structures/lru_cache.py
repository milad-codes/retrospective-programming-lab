"""An LRU cache with O(1) get and put: a dict for lookup plus a doubly linked list for recency."""

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Entry(Generic[K, V]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key, self.value = key, value
        self.prev: _Entry[K, V] | None = None
        self.next: _Entry[K, V] | None = None


class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._entries: dict[K, _Entry[K, V]] = {}
        # sentinels: head.next is the most recently used entry, tail.prev the least
        self._head: _Entry = _Entry(None, None)
        self._tail: _Entry = _Entry(None, None)
        self._head.next, self._tail.prev = self._tail, self._head

    def get(self, key: K, default: V | None = None) -> V | None:
        entry = self._entries.get(key)
        if entry is None:
            return default
        self._move_to_front(entry)
        return entry.value

    def put(self, key: K, value: V) -> None:
        entry = self._entries.get(key)
        if entry:
            entry.value = value
            self._move_to_front(entry)
            return
        if len(self._entries) == self.capacity:
            oldest = self._tail.prev
            self._unlink(oldest)
            del self._entries[oldest.key]
        entry = _Entry(key, value)
        self._entries[key] = entry
        self._link_front(entry)

    def __len__(self) -> int:
        return len(self._entries)

    def keys(self) -> list[K]:
        """Keys from most to least recently used."""
        result, node = [], self._head.next
        while node is not self._tail:
            result.append(node.key)
            node = node.next
        return result

    def _move_to_front(self, entry: _Entry) -> None:
        self._unlink(entry)
        self._link_front(entry)

    def _unlink(self, entry: _Entry) -> None:
        entry.prev.next, entry.next.prev = entry.next, entry.prev

    def _link_front(self, entry: _Entry) -> None:
        entry.prev, entry.next = self._head, self._head.next
        self._head.next.prev = entry
        self._head.next = entry
